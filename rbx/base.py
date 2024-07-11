import string, random
import win32api, win32gui, win32con, win32process
from memopy.api import Memopy

Window = None
Process = Memopy(0)

def RBXString(Address: int):
    string_pointer = Address
    string_check = Process.read_long(
        string_pointer + 0x18
    )

    if string_check > 15:
        string_pointer = Process.read_longlong(
            string_pointer
        )

    return Process.read_string(string_pointer)

def fetch_roblox_pid():
    global Window, Process

    Window = win32gui.FindWindow(None, "Roblox")
    ProcessId = win32process.GetWindowThreadProcessId(Window)[1]

    return ProcessId

def random_string(length: int = 5) -> str:
    result = "".join((random.choice(string.ascii_lowercase) for x in range(length)))
    return result

def initialize():
    ProcessId = fetch_roblox_pid()
    Process.update_pid(ProcessId)

    if not Process.process_handle:
        return False, "Roblox not found :(", -1
    
    return True, "Roblox found :D", ProcessId

def initialize_script_hook():
    def switch_to_roblox():
        try:
            win32gui.SetForegroundWindow(Window)
        except:
            switch_to_roblox()

    switch_to_roblox()

    while True:
        if win32gui.GetForegroundWindow() == Window:
            win32api.keybd_event(
                0, 
                win32api.MapVirtualKey(win32con.VK_ESCAPE, 0), 
                win32con.KEYEVENTF_SCANCODE, 
                0
            )
            win32api.keybd_event(
                0, 
                win32api.MapVirtualKey(win32con.VK_ESCAPE, 0), 
                win32con.KEYEVENTF_SCANCODE | win32con.KEYEVENTF_KEYUP,
                0
            )

            break
    