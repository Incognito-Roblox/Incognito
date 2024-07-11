local bridge_parent = game:GetService("RobloxReplicatedStorage")
local http_service = game:GetService("HttpService")

local data_maxlen = 199998
local PAYLOAD_MATCH = "^%x+"
local PAYLOAD_TEMPLATE = "%08X|%s"

local step_sim = game:GetService("RunService").PreSimulation
local sending_value_whitelist = { "string", "number", "Instance", "boolean", "table" } -- ! table must be JSONEncodeable

local channel_template
do
    channel_template = Instance.new("Folder")

    local peer0_container = Instance.new("Folder") -- roblox container
    peer0_container.Name = "Peer0"
    peer0_container.Parent = channel_template

    local peer1_container = Instance.new("Folder") -- external container
    peer1_container.Name = "Peer1"
    peer1_container.Parent = channel_template

    local instance_refs = Instance.new("Folder")
    instance_refs.Name = "InstanceRefs"
    instance_refs.Parent = channel_template

    local channel_states = Instance.new("NumberValue")
    channel_states.Name = "States"
    channel_states.Parent = channel_template

    -- precreation of StringValues
    -- roughly 16mb+ when combined

    for idx = 0, 8 do
        local peer0_str = Instance.new("StringValue", peer0_container)
        local peer1_str = Instance.new("StringValue", peer1_container)

        peer0_str.Name, peer1_str.Name = idx, idx
        peer0_str.Value = string.rep("\128", 20)
        peer1_str.Value = string.rep("\128", data_maxlen) -- peer1 (external peer) stringvalue is preallocated
    end
end

local bridge = {
    main_container = Instance.new("Folder"),

    module_holder = Instance.new("ObjectValue"),
    executing_script = nil,

    channels_container = Instance.new("Folder"),

    sessions = {},
    queued_datas = {},

    recieved_actions_list = {},
    action_callbacks = {},
}

local function encode_channel_states(
    channel_states: NumberValue,
    is_used: boolean,
    responding: boolean,
    responded: boolean,
    sender: number
)
    local result = bit32.band((if is_used then 1 else 0), 0b0001)
    result += bit32.band(bit32.lshift((if responding then 1 else 0), 1), 0b0010)
    result += bit32.band(bit32.lshift((if responded then 1 else 0), 2), 0b0100)
    result += bit32.band(bit32.lshift(sender, 3), 0b1000)

    channel_states.Value = result
end

local function decode_channel_states(channel_states: NumberValue): (boolean, boolean, boolean, number?)
    local packed_states = channel_states.Value

    local is_used = bit32.extract(packed_states, 0, 1) == 1
    local responding = bit32.extract(packed_states, 1, 1) == 1
    local responded = bit32.extract(packed_states, 2, 1) == 1
    local sender = bit32.extract(packed_states, 3, 1) -- 0 = roblox | 1 = external
    return is_used, responding, responded, (if is_used then sender else nil)
end

local function get_available_channel(): Folder?
    for _, channel in bridge.channels_container:GetChildren() do
        local is_used = decode_channel_states(channel.States)
        if is_used then
            continue
        end

        return channel
    end
    return nil
end

local function combine_buffers(container: Folder): string?
    local children_count = #container:GetChildren()
    local result = ""

    for idx = 0, (children_count - 1) do
        local buffer = container:FindFirstChild(tostring(idx))
        result ..= string.sub(buffer.Value, 1, data_maxlen) -- ensures that there is no \0 included at the end
    end

    if #result < 1 then
        return nil
    end

    local buffer_size = string.match(result, PAYLOAD_MATCH, 1)
    local buffer_match_len = (if buffer_size then #buffer_size else -1)
    buffer_size = (if buffer_size then tonumber(string.sub(buffer_size, 1, 8), 16) else nil)
    if not buffer_size then
        warn(`Failed to get buffer size of '{result}'`)
        return nil
    end

    return string.sub(
        result,
        (buffer_match_len + 2),
        (buffer_size + buffer_match_len) + ((buffer_size // data_maxlen) + 1)
    )
end

local function process_sending_data(channel: Folder, action: string, session: number, args: { any }): string
    local instance_refs: Folder = channel.InstanceRefs
    local current_reference_count = 0
    local raw_data do
        raw_data = {
            action,
            session,
            {},
        }

        for _, value in args do
            local value_type = typeof(value)
            if not (table.find(sending_value_whitelist, value_type)) then
                continue
            end

            if value_type == "Instance" then
                local current_referencer = instance_refs:FindFirstChild(current_reference_count)
                if not current_referencer then
                    current_referencer = Instance.new("ObjectValue", instance_refs)
                    current_referencer.Name = current_reference_count
                end

                current_referencer.Value = value
                table.insert(raw_data[3], { value_type, current_reference_count })
                current_reference_count += 1
                continue
            elseif value_type == "table" then
                value = http_service:JSONEncode(value)
            end

            table.insert(raw_data[3], { value_type, value })
        end
    end

    local encoded_data = http_service:JSONEncode(raw_data)
    local payload_len = utf8.len(encoded_data)
    encoded_data = string.format(PAYLOAD_TEMPLATE, payload_len, encoded_data)

    for buffer_pos = 1, payload_len, data_maxlen do
        local buffer_idx = buffer_pos // data_maxlen

        local current_buffer = channel.Peer0:FindFirstChild(buffer_idx)
        if not current_buffer then
            current_buffer = Instance.new("StringValue", channel.Peer0)
            current_buffer.Name = buffer_idx
        end

        current_buffer.Value = string.sub(encoded_data, buffer_pos, buffer_pos + data_maxlen)
    end
    encode_channel_states(channel.States, true, false, false, 0) -- sending data to external
end

local function process_recieving_data(channel: Folder, responded: boolean)
    encode_channel_states(channel.States, false, false, false, 0)
    local raw_data = combine_buffers(channel.Peer1)
    if not (raw_data and #raw_data > 0) then
        return
    end

    local success, recieved_data = pcall(http_service.JSONDecode, http_service, raw_data)
    if not success then
        warn(`Failed to decode recieved data of channel '{channel.Name}', data: {raw_data}`)
        return
    end

    local action, session, args = unpack(recieved_data)

    if responded then
        local recieved_actions = bridge.recieved_actions_list[action]
        if not recieved_actions then
            recieved_actions = {}
            bridge.recieved_actions_list[action] = recieved_actions
        end

        recieved_actions[session] = args
    else
        local action_func = bridge.action_callbacks[action]

        if action_func then
            task.spawn(action_func, args)
        end
    end
end

bridge.send = function(self, action, ...)
    if not action then
        return
    end

    local session = self.sessions[action] or 0
    self.sessions[action] = session + 1

    table.insert(self.queued_datas, { action, session, { ... } })

    local actions_list = bridge.recieved_actions_list[action]
    if not actions_list then
        actions_list = {}
        bridge.recieved_actions_list[action] = actions_list
    end

    local action_data
    repeat
        action_data = actions_list[session]
        step_sim:Wait()
    until action_data
    return unpack(action_data)
end

bridge.wait = function(self, action, timeout)
    timeout = timeout or 5
    local current_session = self.sessions[action] or 0

    local recieved_actions = bridge.recieved_actions_list[action]
    if not recieved_actions then
        recieved_actions = {}
        bridge.recieved_actions_list[action] = recieved_actions
    end

    local start_time = os.clock()
    local action_data

    repeat
        action_data = recieved_actions[current_session]
        step_sim:Wait()
    until action_data or (os.clock() - start_time) > timeout
    return unpack(action_data)
end

bridge.register_callback = function(self, callback_name, func)
    self.action_callbacks[callback_name] = func
end

bridge.queue_scheduler = step_sim:Connect(function()
    if #bridge.queued_datas < 1 then
        return
    end

    local channel = get_available_channel()
    if not channel then
        return
    end

    local passing_data = table.remove(bridge.queued_datas, 1)
    task.defer(process_sending_data, channel, unpack(passing_data))
end)

bridge.listener = step_sim:Connect(function()
    for _, channel in bridge.channels_container:GetChildren() do
        local is_used, responding, responded, sender = decode_channel_states(channel.States)
        if (sender == 1 and responding) or sender == 0 or not is_used then
            continue
        end

        task.defer(process_recieving_data, channel, responded)
    end
end)

for channel_idx = 0, 7 do
    local channel = channel_template:Clone()
    channel.Name = channel_idx
    channel.Parent = bridge.channels_container
end

bridge.module_holder.Name = "ModuleHolder"
bridge.module_holder.Parent = bridge.main_container

bridge.channels_container.Name = "Channels"
bridge.channels_container.Parent = bridge.main_container

bridge.main_container.Name = "Bridge"
bridge.main_container.RobloxLocked = true
bridge.main_container.Parent = bridge_parent

return bridge
