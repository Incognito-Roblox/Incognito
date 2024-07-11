local logService = game:GetService("LogService")
local bridge = load_module("bridge")
local sandbox = load_module("sandbox")
local utils = load_module("utils")

sandbox:initialize()

bridge:register_callback("load_script", function(args)
    local current_script = bridge.module_holder.Value
    current_script.Name = "incognito"

    local success, func = pcall(require, current_script)

    if success then
        task.defer(sandbox:apply(func))
    end

    local new_module = utils.fetch_stubmodule():Clone()
    bridge.module_holder.Value = new_module
    bridge.executing_script = new_module

    --bridge:send("reset_module_bytecode", current_script)
    current_script:Destroy()
end)

bridge.executing_script = utils.fetch_stubmodule():Clone()
bridge.module_holder.Value = bridge.executing_script

local function onMessageOut(message, messageType)
	bridge:send("error_redirect", message, tostring(messageType))
end

logService.MessageOut:Connect(onMessageOut)