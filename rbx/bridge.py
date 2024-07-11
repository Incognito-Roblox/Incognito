from rbx.instance import Instance, Process
from typing import Callable

import json, psutil, time, threading, re

data_maxlen = 199998
PAYLOAD_MATCH = "^[A-Fa-f0-9]{8}"
PEER_TYPE = {
    "Roblox": 0,
    "External": 1,
}
SENDER_TYPE = {
    "R2E": 0, # roblox to external
    "E2R": 1, # external to roblox
}

def extract_bits(value, field, width=1):
    return (value >> field) & width

class BridgeChannel:
    Name: str = None

    States: Instance = None
    Peer0: Instance = None
    Peer1: Instance = None
    InstanceRefs: Instance = None

    BuffersCaches: dict[int, dict[int, Instance]] = None

    def __init__(self):
        # initialize buffer cache storage
        self.BuffersCaches = {} # should be initialized here, otherwise things will get messy
        self.BuffersCaches[0] = {}
        self.BuffersCaches[1] = {}

    def __repr__(self) -> str:
        return f"(BridgeChannel - '{self.Name}')"

    def Initialize(self, channel_container: Instance):
        self.Name = channel_container.Name

        self.States = channel_container.FindFirstChild("States")
        self.Peer0 = channel_container.FindFirstChild("Peer0")
        self.Peer1 = channel_container.FindFirstChild("Peer1")
        self.InstanceRefs = channel_container.FindFirstChild("InstanceRefs")

        print(self.States, self.Peer0, self.Peer1, self.InstanceRefs)

    def GetChannelStates(self) -> tuple[bool, bool, bool, int | None]:
        if not (self.States and self.States.Value):
            return False, False, False, None

        packed_value = int(self.States.Value)

        is_used = extract_bits(packed_value, 0) == 1
        responding = extract_bits(packed_value, 1) == 1
        responded = extract_bits(packed_value, 2) == 1
        sender = extract_bits(packed_value, 3)

        return is_used, responding, responded, (sender if is_used else None)

    def SetChannelStates(self, is_used: bool, responding: bool, responded: bool, sender: int):
        if not self.States:
            return

        result = (1 if is_used else 0) & 0b0001
        result += ((1 if responding else 0) << 1) & 0b0010
        result += ((1 if responded else 0) << 2) & 0b0100
        result += (sender << 3) & 0b1000

        self.States.Value = result

    def GetBufferData(self, container_type: int) -> str:
        container: Instance = (self.Peer0 if container_type == 0 else self.Peer1 if container_type == 1 else None)
        buffers_cache = self.BuffersCaches[container_type]
        children_count = container.GetChildrenCount()
        result = ""

        for buffer_idx in range(children_count):
            if buffer_idx in buffers_cache:
                buffer_obj = buffers_cache[buffer_idx]
            else:
                buffer_obj = container.FindFirstChild(str(buffer_idx))

                if buffer_obj.Address > 1000:
                    buffers_cache[buffer_idx] = buffer_obj

            result += (buffer_obj.Value or "")

        if len(result) > 0:
            buffer_size = re.match(PAYLOAD_MATCH, result)
            if buffer_size:
                match_len = len(buffer_size[0])
                buffer_size = int(buffer_size[0], 16)

                return result[(match_len + 1):(buffer_size + match_len + ((buffer_size // data_maxlen) + 1))]
            else:
                print(f"Failed to get buffer size of '{result}'")
                return ""

    def SetBufferData(self, new_data: str) -> bool:
        buffers_cache = self.BuffersCaches[PEER_TYPE["External"]]

        for buffer_pos in range(1, len(new_data) + 1, data_maxlen):
            buffer_idx = buffer_pos // data_maxlen

            if buffer_idx in buffers_cache:
                buffer_obj = buffers_cache[buffer_idx]
            else:
                buffer_obj = self.Peer1.FindFirstChild(str(buffer_idx))

                if buffer_obj.Address > 1000:
                    buffers_cache[buffer_idx] = buffer_obj
                else:
                    print(f"Failed to send data '{new_data[0:128]}...' to roblox")
                    return False

            buffer_obj.Value = new_data[buffer_pos - 1: buffer_pos + data_maxlen - 1]

        return True

class Bridge:
    Channels: list[BridgeChannel] = None
    Sessions: dict[str, int] = None

    QueuedDatas: list[str] = None
    CallbacksRegistry: dict[str, Callable[[int, list[any]], None]] = None

    RobloxTerminated = True

    MainContainer: Instance = None
    ModuleHolder: Instance = None

    ListenerThread = None
    QueueSchedThread = None

    def __init__(self):
        self.Channels = []
        self.Sessions = {}
        self.QueuedDatas = []
        self.CallbacksRegistry = {}

        self.ListenerThread = threading.Thread(target=bridge_listener, args=(self,), daemon=True)
        self.ListenerThread.start()

        self.QueueSchedThread = threading.Thread(target=bridge_queue_sched, args=(self,), daemon=True)
        self.QueueSchedThread.start()

    def Start(self, new_pid: int, MainContainer: Instance):
        Process.update_pid(new_pid)
        self.MainContainer = MainContainer
        self.ModuleHolder = self.MainContainer.WaitForChild("ModuleHolder", 5)

        channels = self.MainContainer.WaitForChild("Channels", 5)
        print(channels, self.ModuleHolder)

        # post init
        self.Channels.clear()
        self.Sessions.clear()
        self.QueuedDatas.clear()
        self.CallbacksRegistry.clear()

        # initializes channels (why don't I just reuse the BridgeChannel objs?)
        for channel_idx in range(8): # 8 channels (hardcoded becus crappy children counting)
            channel_container = channels.FindFirstChild(str(channel_idx))
            if channel_container.Address < 1000:
                print(f"Cannot fetch BridgeChannel '{channel_idx}'")
                continue

            channel_obj = BridgeChannel()
            channel_obj.Initialize(channel_container)
            print(f"Channel '{channel_idx}' initialized!", channel_container)
            self.Channels.insert(channel_idx, channel_obj)
            time.sleep(.05)

        self.RobloxTerminated = False
        _process_handler_thread = threading.Thread(target=process_handler, args=(self, new_pid,), daemon=True)
        _process_handler_thread.start()
        time.sleep(1)

    def Send(self, action, args: list[any]=[]):
        if self.RobloxTerminated:
            return

        if not (action in self.Sessions):
            self.Sessions[action] = 0

        try:
            payload = process_data(action, self.Sessions[action], args)

            self.QueuedDatas.append(payload)
            self.Sessions[action] += 1

        except:
            print(f"error sending action ({action}, {self.Sessions[action]}) with args {args}")

    def RegisterCallback(self, callback: Callable[[int, list[any]], tuple[any]]):
        self.CallbacksRegistry[callback.__name__] = callback

def process_handler(self: Bridge, pid: int):
    process = psutil.Process(pid)
    process.wait()
    self.RobloxTerminated = True

def process_data(action: str, session: str, args: list[any]) -> str:
    result = json.dumps([action, session, args])

    data_len_hex = f"{len(result):#0{10}x}"[2:]
    return f"{data_len_hex}|{result}"

def handle_callback(channel: BridgeChannel, callback: Callable[[int, list[any]], list[any]], session: int, args: list[any]):
    returned_args = callback(session, args) or []

    set_success = channel.SetBufferData(process_data(callback.__name__, session, returned_args))
    channel.SetChannelStates(set_success, False, True, SENDER_TYPE["E2R"])

def get_available_channel(self: Bridge):
    for channel in self.Channels:
        is_used, _responding, _responded, _sender = channel.GetChannelStates()
        if is_used:
            continue

        return channel

def bridge_queue_sched(self: Bridge):
    while True:
        time.sleep(0.05)
        if self.RobloxTerminated or len(self.QueuedDatas) < 1:
            continue

        channel = get_available_channel(self)
        if not channel:
            continue

        payload = self.QueuedDatas.pop(0)

        set_success = channel.SetBufferData(payload)
        channel.SetChannelStates(set_success, False, False, SENDER_TYPE["E2R"])

def bridge_listener(self: Bridge):
    while True:
        time.sleep(0.05)
        if self.RobloxTerminated:
            continue

        for channel in self.Channels:
            try:
                is_used, responding, responded, sender = channel.GetChannelStates()
                if sender == SENDER_TYPE["E2R"] or (not is_used):
                    continue

                raw_data = channel.GetBufferData(PEER_TYPE["Roblox"])
                if not (raw_data and len(raw_data) > 0):
                    channel.SetChannelStates(False, False, False, SENDER_TYPE["E2R"])
                    continue

                recieved_data = json.loads(raw_data)
                action, session, raw_args = recieved_data[0], recieved_data[1], recieved_data[2]

                if action in self.CallbacksRegistry:
                    action_callback = self.CallbacksRegistry.get(action)
                    action_args = []

                    for value_info in raw_args:
                        value_type = value_info[0]
                        value = value_info[1]

                        if value_type == "Instance":
                            referenced_instance = channel.InstanceRefs.FindFirstChild(str(value))
                            value = referenced_instance.Value
                        elif value_type == "table":
                            value = json.loads(value)

                        action_args.append(value)

                    handler_thread = threading.Thread(
                        target=handle_callback,
                        args=(channel, action_callback, session, action_args,),
                        daemon=True
                    )
                    handler_thread.start()
                    channel.SetChannelStates(True, True, False, SENDER_TYPE["E2R"])
                else:
                    channel.SetChannelStates(False, False, False, SENDER_TYPE["E2R"])
            except Exception as bruhmoment:
                print(f"Failed to decode data of channel {channel}")
                print(bruhmoment)
                channel.SetChannelStates(False, False, False, SENDER_TYPE["E2R"])
