local debug_lib = table.clone(debug)

debug_lib.getinfo = function(f, options)
    if type(options) == "string" then
        options = string.lower(options) -- if someone adds "L" for activelines and "l" for currentline then thats on them (it will just slow down this function because duplicate debug.infos)
    else
        options = "sflnu"
    end

    local result = {}

    for index = 1, #options do
        local option = string.sub(options, index, index)
        if "s" == option then
            local short_src = debug.info(f, "s")

            result.short_src = short_src
            result.source = "@" .. short_src
            result.what = if short_src == "[C]" then "C" else "Lua"
        elseif "f" == option then
            result.func = debug.info(f, "f")
        elseif "l" == option then
            result.currentline = debug.info(f, "l")
        elseif "n" == option then
            result.name = debug.info(f, "n")
        elseif "u" == option or option == "a" then
            local numparams, is_vararg = debug.info(f, "a")
            result.numparams = numparams
            result.is_vararg = if is_vararg then 1 else 0

            if "u" == option then
                result.nups = -1 --#debug.getupvalues(f)
            end
        end
    end

    return result
end

debug_lib.getmetatable = function(table_or_userdata)
    local result = getmetatable(table_or_userdata)

    if result == nil then -- No meta
        return
    end

    if type(result) == "table" and pcall(setmetatable, table_or_userdata, result) then -- This checks if it's real without overwriting
        return result --* We dont cache this as it will be the same always anyways
    end
    -- Metamethod bruteforcing
    -- For Full (except __gc & __tostring) Metamethod list Refer to - https://github.com/luau-lang/luau/blob/master/VM/src/ltm.cpp#L34

    -- Todo: Look into more ways of making metamethods error (like https://github.com/luau-lang/luau/blob/master/VM%2Fsrc%2Flvmutils.cpp#L174)

    --TODO We can also rebuild many non-dynamic things like len or arithmetic  metamethods since we know what arguments to expect in those usually

    local real_metamethods = {}

    xpcall(function()
        return table_or_userdata._
    end, function()
        real_metamethods.__index = debug.info(2, "f")
    end)

    xpcall(function()
        table_or_userdata._ = table_or_userdata
    end, function()
        real_metamethods.__newindex = debug.info(2, "f")
    end)

    -- xpcall(function()
    -- -- !MAKE __mode ERROR SOMEHOW..
    -- end, function()
    -- 	newTable.__mode = debug.info(2, "f")
    -- end)

    xpcall(function()
        return table_or_userdata:___() -- Make sure this doesn't exist in the table_or_userdata
    end, function()
        real_metamethods.__namecall = debug.info(2, "f")
    end)

    xpcall(function()
        table_or_userdata() -- ! This might not error on tables with __call defined
    end, function()
        real_metamethods.__call = debug.info(2, "f")
    end)

    xpcall(function() -- * LUAU
        for _ in table_or_userdata do -- ! This will never error on tables
        end
    end, function()
        real_metamethods.__iter = debug.info(2, "f")
    end)

    xpcall(function()
        return #table_or_userdata -- ! This will never error on tables, with userdata the issue is same as __concat - is it even a defined metamethod in that case?
    end, function()
        real_metamethods.__len = debug.info(2, "f")
    end)

    -- * Make sure type_check_semibypass lacks any metamethods
    local type_check_semibypass = {} -- bypass typechecks (which will return error instead of actual metamethod)

    xpcall(function() -- ! This will never error (it calls __eq but we need it to error); ~= can also be used
        return table_or_userdata == table_or_userdata -- ? Luau only calls _eq if objects have same metatable
    end, function()
        real_metamethods.__eq = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata + type_check_semibypass
    end, function()
        real_metamethods.__add = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata - type_check_semibypass
    end, function()
        real_metamethods.__sub = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata * type_check_semibypass
    end, function()
        real_metamethods.__mul = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata / type_check_semibypass
    end, function()
        real_metamethods.__div = debug.info(2, "f")
    end)

    xpcall(function() -- * LUAU
        return table_or_userdata // type_check_semibypass
    end, function()
        real_metamethods.__idiv = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata % type_check_semibypass
    end, function()
        real_metamethods.__mod = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata ^ type_check_semibypass
    end, function()
        real_metamethods.__pow = debug.info(2, "f")
    end)

    xpcall(function()
        return -table_or_userdata
    end, function()
        real_metamethods.__unm = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata < type_check_semibypass
    end, function()
        real_metamethods.__lt = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata <= type_check_semibypass
    end, function()
        real_metamethods.__le = debug.info(2, "f")
    end)

    xpcall(function()
        return table_or_userdata .. type_check_semibypass -- TODO Not sure if this would work on userdata.. (do they even have __concat defined? would it be called?)
    end, function()
        real_metamethods.__concat = debug.info(2, "f")
    end)

    -- xpcall(function()
    -- -- !MAKE __type ERROR SOMEHOW..
    -- end, function()
    -- 	newTable.__type = debug.info(2, "f")
    -- end)
    -- FAKE __type INBOUND
    real_metamethods.__type = typeof(table_or_userdata)

    real_metamethods.__metatable = getmetatable(game) -- "The metatable is locked"

    -- xpcall(function()
    -- -- !MAKE __tostring  ERROR SOMEHOW..
    -- end, function()
    -- 	newTable.__tostring = debug.info(2, "f")
    -- end)

    -- FAKE __tostring INBOUND (We wrap it because 1. No rawtostring & 2. In case Table_or_Userdata Name changes)
    real_metamethods.__tostring = function()
        return tostring(table_or_userdata)
    end

    -- xpcall(function()
    -- -- !MAKE __gc ERROR SOMEHOW..
    -- end, function()
    -- 	newTable.__gc = debug.info(2, "f")
    -- end)

    -- table.freeze(real_metamethods) -- Not using for compatibility -- We can't check readonly state of an actual metatable sadly (or can we?)
    return real_metamethods
end

debug_lib.setmetatable = setmetatable -- should be setrawmetatable

return function()
    return {
        ["debug"] = debug_lib,
    }, {
        ["debug.getmetatable"] = { "getrawmetatable" },
        ["debug.setmetatable"] = { "setrawmetatable" },
    }
end
