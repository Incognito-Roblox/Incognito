local bridge = load_module("bridge")
local utils = load_module("utils")
local env_builtins = load_module("env_builtins")

local main_script = script

local env_modules = {
    "bit",
    "cache",
    "closure",
    "crypt",
    "debug",
    "drawing",
    "filesystem",
    "input",
    "instances",
    "misc",
    "scripts",
}
local setfenv = setfenv

local function fetch_builtin_env() -- clones current environment
    local cloned_env = {}
    local current_env = getfenv()

    for builtin_name in env_builtins do
        local env_value = current_env[builtin_name]
        if not env_value then
            continue
        end

        cloned_env[builtin_name] = (
            if type(env_value) == "table" then table.freeze(table.clone(env_value)) else env_value
        )
    end
    return cloned_env
end

local function initialize_env_modules()
    local roblox_env = fetch_builtin_env() -- do not write on this
    local new_env = setmetatable({}, {
        __index = roblox_env,
    })

    -- loads env modules
    for _, module_name in env_modules do
        local module = load_module(`environment/{module_name}`)
        local env_defs, defined_aliases = module(new_env)

        for index, value in env_defs do
            new_env[index] = value
        end

        if type(defined_aliases) ~= "table" then
            continue
        end
        for global_name, alias_list in defined_aliases do
            local moduleIndexed = env_defs

            for _, name in string.split(global_name, ".") do
                moduleIndexed = moduleIndexed[name]
            end
            if not moduleIndexed then
                continue
            end

            for _, alias in alias_list do
                local currentIndex = new_env
                local aliasSplits = string.split(alias, ".")
                local lastAlias = aliasSplits[#aliasSplits]

                for index, name in aliasSplits do
                    if index == #aliasSplits then
                        break
                    end
                    currentIndex = currentIndex[name]
                end
                currentIndex[lastAlias] = moduleIndexed
            end
        end
    end

    -- init
    for index, value in new_env do
        if type(value) ~= "table" or table.isfrozen(value) then
            continue
        end
        table.freeze(value)
    end

    return {
        global = new_env,
        roblox = roblox_env,
    }
end

-- we dont want the main thread environment to be modified
local function _apply_env(func, env)
    setfenv(0, env)
    setfenv(1, env)

    return setfenv(func, env)
end

local sandbox = {
    environment = nil,
    hidden_env = nil,
}

function sandbox:apply<T>(func: T): T
    local new_env = self:new_environment(Instance.new("LocalScript"))
    local _success, result = coroutine.resume(coroutine.create(_apply_env), func, new_env)

    return result
end

function sandbox:new_environment(script: LuaSourceContainer): { [any]: any }
    local plugin_env = {}
    local sandboxed_env = setmetatable({
        script = script,
    }, {
        __index = function(env, index)
            return plugin_env[index] or self.hidden_env[index] or self.environment.global[index]
        end,
        __newindex = function(env, index, value)
            if index ~= "script" then
                rawset(self.environment.global, index, value)
            end
            rawset(env, index, value)
        end,
    })

    plugin_env.getfenv = function(value)
        local success, result = pcall(getfenv, value)

        if success then
            if rawget(result, "script") == main_script then
                result = sandboxed_env
            end
            return result
        end
        return error(result, 2)
    end

    return sandboxed_env
end

function sandbox:initialize()
    local hidden_env = {
        game = newproxy(true),
    }
    local environment = initialize_env_modules()

    local _game_meta = getmetatable(hidden_env.game)
    _game_meta.__index = function(self, index)
        local _, game_index = pcall(function()
            return game[index]
        end)

        if index == "HttpGet" or index == "HttpGetAsync" then
            return function(self, ...)
                return environment.global["httpget"](...)
            end
        elseif index == "HttpPost" or index == "HttpPostAsync" then
            -- ficello will do it!!
            return function(self, ...)
                return environment.global["httppost"](...)
            end
        elseif index == "GetObjects" then
            return function(self, ...)
                return environment.global["getobjects"](...)
            end
        elseif game_index and type(game_index) == "function" then
            return function(self, ...)
                return game_index(game, ...)
            end
        else
            --TODO Add automatic .GetService
            --TODO Use Instance.new if FindService doesn't find the service (to avoid detections like VirtualInputManager), if Instance.new fails then fall back to GetService
            return game[index]
        end
    end
    _game_meta.__metatable = getmetatable(game)

    local cloned_environment

    environment.global._G = {}
    environment.global.shared = {}

    environment.global.getgenv = function()
        return cloned_environment.global
    end

    environment.global.getrenv = function()
        return environment.roblox
    end

    environment.roblox.loadstring = function(source, chunk_name)
        assert(type(source) == "string", "arg #1 must be type string")
        local current_script = utils.fetch_stubmodule():Clone()
        current_script.Name = chunk_name or "incognito"

        local set_success, compile_err = bridge:send("load_source", current_script, source)

        if not set_success then
            -- TODO: make this return compiler error if compilation didn't succeed
            return nil, compile_err
        end

        local success, func = pcall(require, current_script) -- TODO: This still causes "ModuleScript:1: Incomplete statement: expected assignment or a function call"-like errors despite pcall because it's a compiler error inside the ModuleScript, we need to redirect it somehow as stated above
        --task.spawn(bridge.send, bridge, "reset_module_bytecode", current_script)
        current_script:Destroy()

        if not success then
            return nil, "Failed to load script"
        end

        return self:apply(func)
    end

    cloned_environment = table.clone(environment)
    for env_name, env in environment do
        cloned_environment[env_name] = table.clone(env) -- * We don't need to do a deep clone as long as every table in the genv (global) environment is frozen
    end

    self.environment = cloned_environment -- Disconnects user's environment from our init module's environment so that users cannot mess with custom functions that other custom functions rely on
    self.hidden_env = hidden_env
end

return sandbox
