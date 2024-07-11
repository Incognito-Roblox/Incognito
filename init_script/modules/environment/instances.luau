local bridge = load_module("bridge")

-- objects
local hidden_ui_container = Instance.new("Folder")
hidden_ui_container.Name = "\0incognito-hui"
hidden_ui_container.RobloxLocked = true
hidden_ui_container.Parent = game:FindService("CoreGui"):FindFirstChild("RobloxGui")

-- variables
local script_env
local instances_reg = setmetatable({ [game] = true }, { __mode = "ks" })
local touchers_reg = setmetatable({}, { __mode = "ks" })

-- functions
local _loaded_saveinstance

local function addToInstancesReg(descendant: Instance)
    if instances_reg[descendant] then
        return
    end
    instances_reg[descendant] = true
end

local function filterAllInstances(filter)
    local result = {}
    local idx = 1

    for instance in instances_reg do
        if not (filter(instance)) then
            continue
        end
        result[idx] = instance
        idx += 1
    end
    return result
end

-- init
game.DescendantAdded:Connect(addToInstancesReg)
game.DescendantRemoving:Connect(addToInstancesReg)

for _, instance in game:GetDescendants() do
    addToInstancesReg(instance)
end

-- main
local instances = {}

-- * general instance functions

function instances.getinstances()
    return filterAllInstances(function()
        return true
    end)
end

function instances.getnilinstances()
    return filterAllInstances(function(instance)
        return instance.Parent == nil
    end)
end

function instances.getscripts()
    return filterAllInstances(function(instance)
        return instance:IsA("LocalScript") or instance:IsA("ModuleScript")
    end)
end

function instances.getmodules()
    return filterAllInstances(function(instance)
        return instance:IsA("ModuleScript")
    end)
end

-- * other instance functions

function instances.gethui()
    return hidden_ui_container
end

function instances.spoofinstance(spoofing, new_instance)
    assert(typeof(spoofing) == "Instance", `arg #1 must be type Instance`)
    assert(typeof(new_instance) == "Instance" or type(new_instance) == "number", `arg #2 must be type Instance`) -- ? or number ?

    task.spawn(bridge.send, bridge, "spoof_instance", spoofing, new_instance)
end

function instances.getinstanceaddress(instance)
    assert(typeof(instance) == "Instance", `arg #1 must be type Instance`)

    return bridge:send("get_instance_address", instance)
end

function instances.firetouchinterest(toucher: BasePart, to_touch: BasePart, touch_value: number)
    assert(typeof(toucher) == "Instance" and toucher:IsA("BasePart"), `arg #1 must be BasePart`)
    assert(typeof(to_touch) == "Instance" and to_touch:IsA("BasePart"), `arg #2 must be BasePart`)
    assert(type(touch_value) == "number", "arg #3 must be type number")

    if not touchers_reg[toucher] then
        touchers_reg[toucher] = {}
    end

    local part_address = script_env.getinstanceaddress(to_touch)

    if touch_value == 0 then
        if touchers_reg[toucher][part_address] then
            return
        end
        local fake_part = Instance.new("Part", to_touch)
        fake_part.CanCollide = false
        fake_part.CanTouch = true
        fake_part.Anchored = true
        fake_part.Transparency = 1

        script_env.spoofinstance(fake_part, to_touch)
        touchers_reg[toucher][part_address] = task.spawn(function()
            while true do
                fake_part.CFrame = toucher.CFrame
                task.wait()
            end
        end)
    elseif touch_value == 1 then
        if not touchers_reg[toucher][part_address] then
            return
        end
        script_env.spoofinstance(to_touch, part_address)
        local toucher_thread = table.remove(touchers_reg[toucher], part_address)
        task.cancel(toucher_thread)
    end
end

function instances.fireclickdetector(clickdetector, distance)
    -- TODO: do distance
    assert(typeof(clickdetector) == "Instance" and clickdetector:IsA("ClickDetector"), `arg #1 must be ClickDetector`)
    if distance ~= nil then
        assert(type(distance) == "number", `arg #2 must be type number`)
    end
    local oldCDMaxActivationDistance = clickdetector.MaxActivationDistance
    local oldCDParent = clickdetector.Parent
    local tmpPart = Instance.new("Part")
    tmpPart.Parent = workspace
    tmpPart.CanCollide = false
    tmpPart.Anchored = true
    tmpPart.Transparency = 1
    tmpPart.Size = Vector3.new(30, 30, 30)
    clickdetector.Parent = tmpPart
    --script_env.spoofinstance(tmpPart, clickdetector.Parent) could use it
    clickdetector.MaxActivationDistance = 9e9

    local hb
    -- credits to quiving for that one
    hb = game:GetService("RunService").Heartbeat:Connect(function()
        tmpPart.CFrame = workspace.Camera.CFrame
            * CFrame.new(0, 0, -20)
            * CFrame.new(
                workspace.Camera.CFrame.LookVector.X,
                workspace.Camera.CFrame.LookVector.Y,
                workspace.Camera.CFrame.LookVector.Z
            )
        game:GetService("VirtualUser")
            :ClickButton1(Vector2.new(20, 20), workspace:FindFirstChildOfClass("Camera").CFrame)
    end)

    clickdetector.MouseClick:Once(function()
        hb:Disconnect()
        clickdetector.MaxActivationDistance = oldCDMaxActivationDistance
        clickdetector.Parent = oldCDParent
        tmpPart:Destroy()
    end)
end

function instances.fireproximityprompt(proximityprompt, amount, skip)
    assert(
        typeof(proximityprompt) == "Instance" and proximityprompt:IsA("ProximityPrompt"),
        `arg #1 must be ProximityPrompt`
    )

    if amount ~= nil then
        assert(type(amount) == "number", `arg #2 must be type number`)
        if skip ~= nil then
            assert(type(skip) == "boolean", `arg #3 must be type boolean`)
        end
    end

    local oldHoldDuration = proximityprompt.HoldDuration
    local oldMaxDistance = proximityprompt.MaxActivationDistance

    proximityprompt.MaxActivationDistance = 9e9 -- client replicated only
    proximityprompt:InputHoldBegin()

    for i = 1, amount or 1 do -- or 1 cuz number can be nil
        if skip then
            proximityprompt.HoldDuration = 0
        else
            task.wait(proximityprompt.HoldDuration + 0.01) -- better than wait()
        end
    end

    proximityprompt:InputHoldEnd()
    proximityprompt.MaxActivationDistance = oldMaxDistance
    proximityprompt.HoldDuration = oldHoldDuration
end

function instances.isnetworkowner(part)
    assert(typeof(part) == "Instance" and part:IsA("BasePart"), `arg #1 must be BasePart`)
    if part.Anchored then
        return false
    end
    return part.ReceiveAge == 0
end

function instances.setsimulationradius(newRadius, newMaxRadius)
    assert(newRadius, `arg #1 is missing`)
    assert(type(newRadius) == "number", `arg #1 must be type number`)

    local LocalPlayer = game:GetService("Players").LocalPlayer
    if LocalPlayer then
        LocalPlayer.SimulationRadius = newRadius
        LocalPlayer.MaximumSimulationRadius = newMaxRadius or newRadius
    end
end

function instances.saveinstance(...)
    if not _loaded_saveinstance then
        local params = {
            RepoURL = "https://raw.githubusercontent.com/luau/SynSaveInstance/main/",
            SSI = "saveinstance",
        }

        local content = script_env.httpget(params.RepoURL .. params.SSI .. ".luau", true)
        _loaded_saveinstance = script_env.loadstring(content, params.SSI)()
    end

    return _loaded_saveinstance(...)
end

function instances.isscriptable(instance, property_name)
    local ok, Result = xpcall(instance.GetPropertyChangedSignal, function(result)
        return result
    end, instance, property_name)

    return ok or not string.find(Result, "scriptable", nil, true)
end

function instances.setscriptable(instance, property_name, scriptable)
    assert(typeof(instance) == "Instance", `arg #1 must be type Instance`)
    assert(type(property_name) == "string", `arg #2 must be type string`)
    assert(type(scriptable) == "boolean", `arg #3 must be type bolean`)
    if script_env.isscriptable(instance, property_name) then
        return false
    end

    return bridge:send("set_scriptable", instance, property_name, scriptable)
end

function instances.getproperties(instance)
    assert(typeof(instance) == "Instance", `arg #1 must be type Instance`)

    return bridge:send("get_properties", instance) -- * All, including hidden (Should be {[property_name]=value} Format)
end

function instances.gethiddenproperties(instance)
    assert(typeof(instance) == "Instance", `arg #1 must be type Instance`)

    local hidden_properties = {}

    -- TODO Edit below once getproperties returns prop-value pairs instead of array of names
    -- for _, property_name in script_env.getproperties(instance) do
    --     if not script_env.isscriptable(instance, property_name) then
    --         hidden_properties[property_name] = "STUB_VALUE"
    --     end
    -- end

    return hidden_properties
end

function instances.gethiddenproperty(instance, property_name)
    assert(typeof(instance) == "Instance", `arg #1 must be type Instance`)
    assert(type(property_name) == "string", `arg #2 must be type string`)
    if script_env.isscriptable(instance, property_name) then
        return instance[property_name] -- * This will error if it's an invalid property but that should intended
    end

    return script_env.gethiddenproperties(instance)[property_name]

    -- local was_scriptable = script_env.setscriptable(instance, property_name, true)
    -- local o, value = pcall(function()
    --     return instance[property_name]
    -- end)
    -- if not was_scriptable then
    --     script_env.setscriptable(instance, property_name, was_scriptable)
    -- end
    -- if o then
    --     return value, was_scriptable
    -- else
    --     error(value, 2)
    -- end
end

function instances.sethiddenproperty(instance, property_name, value)
    assert(typeof(instance) == "Instance", `arg #1 must be type Instance`)
    assert(type(property_name) == "string", `arg #2 must be type string`)

    -- TODO If we can't figure out how to setscriptable and access property in lua without crashing then just bridge this function entirely

    -- local was_scriptable = script_env.setscriptable(instance, property_name, true)
    -- local o, err = pcall(function()
    --     instance[property_name] = value
    -- end)
    -- if not was_scriptable then
    --     script_env.setscriptable(instance, property_name, was_scriptable)
    -- end
    -- if o then
    --     return was_scriptable
    -- else
    --     error(err, 2)
    -- end
end

return function(_script_env)
    script_env = _script_env

    return instances,
        {
            ["getscripts"] = { "getrunningscripts" },
            ["getmodules"] = { "getloadedmodules", "getrunningmodules" },

            ["gethui"] = { "gethiddenui", "get_hidden_hui", "get_hui" },

            ["saveinstance"] = { "saveplace" },
        }
end
