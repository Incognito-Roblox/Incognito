local _loaded_modules = {}

local function load_module(module_name)
    local module_result = _loaded_modules[module_name]
    if module_result then
        return module_result
    end

    local path = string.split(module_name, "/")

    if #path == 2 then
        local group_name, submodule_name = unpack(path)

        local module_group = embedded_modules[group_name]
        if not group_name then
            return error(`Cannot find module group '{group_name}'.`, 2)
        end
        if not module_group[submodule_name] then
            return error(`Cannot find module '{submodule_name}' of group '{group_name}'.`, 2)
        end

        module_result = module_group[submodule_name](load_module)
    else
        module_result = embedded_modules[module_name](load_module)
    end

    _loaded_modules[module_name] = module_result
    return module_result
end

task.spawn(load_module, "init") -- loads main init script
-- loads miscellanous shenanigans based on the hooked script name
if script.Name == "PolicyService" then
    --[[
        Filename: PolicyService.lua
        Written by: ben
        Description: Handles all policy service calls in lua for core scripts
    --]]

    local PlayersService = game:GetService('Players')

    local isSubjectToChinaPolicies = true
    local policyTable
    local initialized = false
    local initAsyncCalledOnce = false

    local initializedEvent = Instance.new("BindableEvent")

    --[[ Classes ]]--
    local PolicyService = {}

    function PolicyService:InitAsync()
        if _G.__TESTEZ_RUNNING_TEST__ then
            isSubjectToChinaPolicies = false
            -- Return here in the case of unit tests
            return
        end

        if initialized then return end
        if initAsyncCalledOnce then
            initializedEvent.Event:Wait()
            return
        end
        initAsyncCalledOnce = true

        local localPlayer = PlayersService.LocalPlayer
        while not localPlayer do
            PlayersService.PlayerAdded:Wait()
            localPlayer = PlayersService.LocalPlayer
        end
        assert(localPlayer, "")

        pcall(function() policyTable = game:GetService("PolicyService"):GetPolicyInfoForPlayerAsync(localPlayer) end)
        if policyTable then
            isSubjectToChinaPolicies = policyTable["IsSubjectToChinaPolicies"]
        end

        initialized = true
        initializedEvent:Fire()
    end

    function PolicyService:IsSubjectToChinaPolicies()
        self:InitAsync()

        return isSubjectToChinaPolicies
    end

    return PolicyService
elseif script.Name == "JestGlobals" then
    local input_manager = Instance.new("VirtualInputManager")

    input_manager:SendKeyEvent(true, Enum.KeyCode.Escape, false, game)
    input_manager:SendKeyEvent(false, Enum.KeyCode.Escape, false, game)
    input_manager:Destroy()

    return {HideTemp = function() end}
end