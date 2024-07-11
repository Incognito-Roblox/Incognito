local script_env

-- main
local closure = {}

function closure.iscclosure(func)
    assert(type(func) == "function", `arg #1 must be type function`)
    return debug.info(func, "s") == "[C]"
end

function closure.islclosure(func)
    assert(type(func) == "function", `arg #1 must be type function`)
    return debug.info(func, "s") ~= "[C]"
end

function closure.getcallingscript(stackCount: number)
    stackCount = stackCount or 3

    for stackLvl = stackCount, 0, -1 do
        local func = debug.info(stackLvl, "f")
        stackLvl -= 1
        if not func then
            continue
        end

        local script = rawget(getfenv(func), "script")

        if typeof(script) == "Instance" and script:IsA("BaseScript") then
            return script
        end
    end
end

local function newWrappedCClosure(func)
    if script_env.iscclosure(func) then
        return func
    end

    return coroutine.wrap(function(...)
        local args = { ... }

        while true do
            args = { coroutine.yield(func(unpack(args))) }
        end
    end)
end

function closure.newcclosure(func)
    assert(type(func) == "function", `arg #1 must be type function`)
    return newWrappedCClosure(func)
end

function closure.newlclosure(func)
    return function(...)
        return func(...)
    end
end

function closure.isexecutorclosure(func)
    if script_env.iscclosure(func) then
        return debug.info(func, "n") == "" -- * Hopefully there aren't any false positives
    end
    local f_env = getfenv(func)
    return f_env.script.Parent == nil or f_env == getfenv(0) -- TODO The second part can be fooled if isexecutorclosure(HijackedModule.Function)
end

function closure.checkcaller()
    return 3 <= script_env.getthreadidentity()
end

function closure.clonefunction(func)
    return if script_env.iscclosure(func) then script_env.newcclosure(func) else script_env.newlclosure(func)
end

function closure.securecall(func, scriptOrEnv, ...): ...any
    assert(type(func) == "function", `arg #1 must be type function`)

    local type_scriptOrEnv = typeof(scriptOrEnv)
    local virtual_env
    do
        if type_scriptOrEnv == "Instance" and scriptOrEnv:IsA("LuaScriptContainer") then
            virtual_env = setmetatable({}, { __index = script_env.getrenv() })
            virtual_env.script = scriptOrEnv
        elseif type_scriptOrEnv == "table" then
            virtual_env = scriptOrEnv
        else
            return error(`invalid argument #2 (LuaSourceContainer | table expected, got {type_scriptOrEnv})`, 2)
        end
    end

    return coroutine.wrap(function(...)
        setfenv(0, virtual_env)
        setfenv(1, virtual_env)

        return func(...)
    end)(...)
end

closure.getthread = coroutine.running

return function(_script_env)
    script_env = _script_env

    return closure, { ["isexecutorclosure"] = { "checkclosure", "isourclosure" } }
end
