-- imports
local bridge = load_module("bridge")
local goodsignal = load_module("lib/goodsignal")

local script_env

local httpContentTypeToHeader
do
    -- * Keep this updated https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/roblox/LuaPackages/Packages/_Index/HttpServiceMock/HttpServiceMock/httpContentTypeToHeader.lua
    -- * https://create.roblox.com/docs/reference/engine/enums/HttpContentType
    local httpContentTypeToHeaderLookup = {
        [Enum.HttpContentType.ApplicationJson] = "application/json",
        [Enum.HttpContentType.ApplicationUrlEncoded] = "application/x-www-form-urlencoded",
        [Enum.HttpContentType.ApplicationXml] = "application/xml",
        [Enum.HttpContentType.TextPlain] = "text/plain",
        [Enum.HttpContentType.TextXml] = "text/xml",
    }

    httpContentTypeToHeader = function(httpContentType: Enum.HttpContentType): string
        local value = httpContentTypeToHeaderLookup[httpContentType]
        assert(value, "Unable to map Enum.HttpContentType to Content-Type. Use a Content-Type string instead")
        return value
    end
end

-- main
local misc = {}

misc.isreadonly = table.isfrozen

function misc.setreadonly(t, lock)
    if table.isfrozen(t) then
        if lock then
            return
        end
        -- unlock code here
    else
        if not lock then
            return
        end
        table.freeze(t)
    end
end

function misc.identifyexecutor()
    return "incognito", "${VERSION_AUTOMATIC}"
end

function misc.gethwid()
    local success, response = bridge:send("get_hwid")
    if not success then
        error("Failed to get HWID", 2)
    end
    return response
end

function misc.request(options)
    assert(type(options) == "table", "arg #1 must be type table")
    local Url = options.Url
    assert(type(Url) == "string", "Url must be type string")

    local HttpService = game:GetService("HttpService")

    -- * Hex decode (do we need this with bridged request?)
    -- Url = string.gsub(Url, "%%(%x%x)", function(hex)
    --     return string.char(tonumber(hex, 16))
    -- end)

    local Method = options.Method
    if Method then
        Method = string.upper(Method)
        if
            not (
                { --https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/04ab62513d220b3074c6433941864a705e0833f5/LuaPackages/Packages/_Index/RobloxRequests/RobloxRequests/src/session.lua#L160
                    -- Others are: TRACE, CONNECT (need testing)
                    GET = true,
                    POST = true,
                    HEAD = true,
                    OPTIONS = true,
                    PUT = true,
                    DELETE = true,
                    PATCH = true,
                }
            )[Method]
        then
            error("Invalid Method", 2)
        end
    else
        Method = "GET"
    end

    local Headers = options.Headers
    -- if Headers then -- ? Should it really be our problem if someone uses a different case on the header (e.g. all lowercase)
    -- local function normalizeHeaderName(header: string): string
    --     return string.lower(header)
    -- end
    -- local function normalizeHeaders(headers)
    --     local newHeaders = {}
    --     for name, value in headers do
    --         local lowercaseName = normalizeHeaderName(name)
    --         newHeaders[lowercaseName] = value
    --     end
    --     return newHeaders
    -- end
    -- else
    if not Headers then
        Headers = {}
    end

    local Body = options.Body
    if Method == "GET" or Method == "POST" then -- ! Important for Luarmor support
        -- Headers.Playercount = tostring(#game:GetService("Players"):GetPlayers())
        -- Headers.Requester = script_env.getexecutioncontext()
        local PlaceId = game.PlaceId
        local GameId = game.JobId -- ! Not sure, things that this could be are: (RbxAnalyticsService/game).GetPlaySessionId or RbxAnalyticsService.GetSessionId

        Headers["User-Agent"] = "Roblox/WinInet"

        Headers["Roblox-Place-Id"] = tostring(PlaceId)
        Headers["Roblox-Game-Id"] = GameId
        Headers["Roblox-Session-Id"] = HttpService:JSONEncode({
            -- Age = workspace.DistributedGameTime,
            -- BlockedPlayerIds = {},
            -- BrowserTrackerId = 0,
            -- ClientIpAddress = "1.1.1.1",
            -- CountryId = 0,
            GameId = GameId,
            -- GameJoinMetadata = { JoinSource = 0, RequestType = 0 },
            -- IsUserVoiceChatEnabled = game:GetService("VoiceChatService"):IsVoiceEnabledForUserIdAsync(game:GetService("Players").LocalPlayer.UserId),
            -- JoinType = "Specific",
            -- LanguageId = 0,
            -- Latitude = 0,
            -- Longitude = 0,
            -- MatchmakingDecisionId=null,
            PlaceId = PlaceId,
            -- PlatformTypeId = 0,
            -- PlaySessionFlags = 0,
            -- PlayerSignals = {},
            -- PolicyCountryId=null,
            -- RandomSeed2 = "",
            -- SessionId = "",
            -- SessionStarted = DateTime.fromUnixTimestamp(os.time() - workspace.DistributedGameTime):ToIsoDate(), --"1994-01-18T17: 11: 44.3095184Z",
            -- SourcePlaceId=null,
            -- SupportedLanguageId = 0,
            -- UserScoreObfuscated = 0,
            -- UserScorePublicKey = 0,
        })
    else
        Headers["User-Agent"] = table.concat({ script_env.identifyexecutor() }, "/")
    end
    if Method == "POST" or Method == "PATCH" then -- https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/master/LuaPackages/Packages/_Index/roblox_http-request/http-request/RequestFunctions/Util/getHeaders.lua
        if not Headers["Content-Type"] then
            Headers["Content-Type"] = "application/json"
        end

        if Body and type(Body) == "table" then
            Body = HttpService:JSONEncode(Body)
        end
    end

    local HWID = script_env.gethwid() --game:GetService("RbxAnalyticsService"):GetClientId() -- TODO Find something better

    Headers["Incognito-Fingerprint"] = HWID
    Headers["Incognito-User-Identifier"] = HWID

    local params =
        { -- https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/master/LuaPackages/Packages/_Index/HttpRequest/HttpRequest/RequestFunctions/RequestInternal.lua#L6
            Url = Url,
            Method = Method, -- GET, POST, PATCH, PUT (DEFAULT: GET)

            Body = Body,
            Headers = Headers,
            Cookies = options.Cookies, -- Does this even work
        }
    local success, response = bridge:send("http_request", params)

    if not success then
        return error(`Failed to fetch URL '{Url}'`, 2)
    end

    return response
end

function misc.httpget(url, arg2, arg3) -- Must be compatible with params from HttpGet, HttpGetAsync, HttpService.GetAsync
    assert(type(url) == "string", `arg #1 must be type string`)
    assert(url ~= "", `arg #1 cannot be empty`)

    local args = {
        Method = "GET", -- Unneccessary, GET is DEFAULT
        Url = url,
    }

    local arg3_type = typeof(arg3)

    if arg3_type == "table" then -- HttpService.GetAsync
        args.Headers = arg3 --? In docs they are Variant though what other types does that imply ?
    elseif arg3_type == "EnumItem" and arg3.EnumType == Enum.HttpRequestType then -- HttpGet
        arg2 = arg3 -- because arg2 likely means 'synchronous' in this case and we don't need it
    end

    local arg2_type = typeof(arg2)

    if arg2_type == "boolean" then
        if arg2 then
            local Headers = args.Headers
            if not Headers then
                Headers = {}
                args.Headers = Headers
            end

            -- ! Roblox forces this anyway (regardless of this); So CachePolicy might be a good alternative if we figure out how it works
            Headers["Cache-Control"] = "no-cache" -- https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/2719f6e1b2efba579994c0c5d762c6eed2cd5db0/LuaPackages/Packages/_Index/HttpServiceMock/HttpServiceMock/HttpServiceMock.lua#L97
        end
    end

    return misc.request(args).Body
end

function misc.httppost(url, data, arg3, arg4, arg5) -- Must be compatible with params from HttpPost, HttpPostAsync, HttpService.PostAsync
    assert(type(url) == "string", `arg #1 must be type string`)
    assert(url ~= "", `arg #1 cannot be empty`)

    local args = {
        Method = "POST",
        Url = url,
        Body = data,
    }

    if type(arg3) == "boolean" then -- HttpGet
        arg3, arg4, arg5 = arg4, arg5, nil -- because arg3 likely means 'synchronous' in this case and we don't need it
    end

    if arg5 then -- HttpService.PostAsync
        args.Headers = arg3 --? In docs they are Variant though what other types does that imply ?
    end

    if arg3 then
        local Headers = args.Headers
        if not Headers then
            Headers = {}
            args.Headers = Headers
        end

        Headers["Content-Type"] = if type(arg3) == "string" then arg3 else httpContentTypeToHeader(arg3) -- https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/2719f6e1b2efba579994c0c5d762c6eed2cd5db0/LuaPackages/Packages/_Index/HttpServiceMock/HttpServiceMock/HttpServiceMock.lua#L151
    end

    local arg4_type = typeof(arg4)

    if arg4_type == "boolean" then -- HttpService.PostAsync
        if arg4 then -- compress
            local Headers = args.Headers
            if not Headers then
                Headers = {}
                args.Headers = Headers
            end

            Headers["Content-Encoding"] = "gzip" -- https://github.com/MaximumADHD/Roblox-Client-Tracker/blob/2719f6e1b2efba579994c0c5d762c6eed2cd5db0/LuaPackages/Packages/_Index/HttpServiceMock/HttpServiceMock/HttpServiceMock.lua#L147
        end
    end

    return misc.request(args).Body
end

function misc.getobjects(assetid)
    if type(assetid) == "number" then
        assetid = "rbxassetid://" .. assetid
    end
    return { game:GetService("InsertService"):LoadLocalAsset(assetid) }
end

function misc.getcustomasset(path)
    assert(path ~= "", `arg #1 cannot be empty`)
    assert(type(path) == "string", `arg #1 must be type string`)

    local success, asset_url = bridge:send("get_custom_asset", path)

    if not success then
        return error(`Failed to get asset URL of '{path}'`, 2)
    end
    return asset_url
end

function misc.messagebox(text, caption, flags)
    assert(type(text) == "string", `arg #1 must be type string`)
    assert(text ~= "", `arg #1 cannot be empty`)
    assert(type(caption) == "string", `arg #2 must be type string`)
    assert(caption ~= "", `arg #2 cannot be empty`)
    if flags ~= nil then
        assert(type(flags) == "number", `arg #3 should be a number`)
    end

    local _success, result = bridge:send("messagebox", text, caption, flags or 1)

    return result
end

function misc.setclipboard(to_copy)
    assert(type(to_copy) == "string", `arg #1 must be type string`)
    assert(to_copy ~= "", `arg #1 cannot be empty`)

    local clipboard_success = bridge:send("set_clipboard", to_copy)

    if not clipboard_success then
        return error("Can't set to clipboard", 2)
    end
    return clipboard_success
end

function misc.getfflag(flag)
    assert(type(flag) == "string", "arg #1 must be type string")
    assert(flag ~= "", `arg #1 cannot be empty`)

    for container, methods in
        { [game] = { "GetFastFlag", "GetFastString", "GetFastInt" }, [settings()] = { "GetFFlag", "GetFVariable" } }
    do
        for _, method in methods do
            local s, r = pcall(container[method], container, flag)
            if s then
                return r
            end
        end
    end
end

do -- TODO Should be able to uncap
    local RunService = game:GetService("RunService")
    local Capped, FractionOfASecond
    local Heartbeat = RunService.Heartbeat
    function misc.setfpscap(fps_cap)
        if fps_cap == 0 or fps_cap == nil or 1e4 <= fps_cap then -- ~7k fps is the highest people have gotten; --?maybe compare to getfpsmax instead? (but we have to ensure getfpsmax is accurate first)
            if Capped then
                task.cancel(Capped)
                Capped = nil
                FractionOfASecond = nil
            end
            return
        end

        FractionOfASecond = 1 / fps_cap
        if Capped then
            return
        end
        local function Capper()
            -- * Modified version of https://github.com/MaximumADHD/Super-Nostalgia-Zone/blob/540221bc945a8fc3a45baf51b40e02272a21329d/Client/FpsCap.client.lua#
            local t0 = os.clock()
            Heartbeat:Wait()
            -- repeat until t0 + t1 < tick()
            -- local count = 0
            while os.clock() <= t0 + FractionOfASecond do -- * not using repeat to avoid unreasonable extra iterations
                -- count+=1
            end
            -- task.spawn(print,count)
        end
        Capper() -- Yield until it kicks in basically
        Capped = task.spawn(function()
            -- capping = true -- * this works too
            while true do
                Capper()
            end
        end)
    end
end

do -- Websockets
    local WebSocket = { connect = nil }

    local websocket_mt = {
        __index = function(self, index)
            if not rawget(self, "__OBJECT_ACTIVE") then
                error("WebSocket is closed.")
            end

            if index == "OnMessage" then
                if not rawget(self, "__OBJECT_ACTIVE") then
                    error("WebSocket is closed.")
                end

                return rawget(self, "__OBJECT_MESSAGE")
            end

            if index == "OnClose" then
                if not rawget(self, "__OBJECT_ACTIVE") then
                    error("WebSocket is closed.")
                end

                return rawget(self, "__OBJECT_CLOSE")
            end

            if index == "Send" then
                return function(_, message, is_binary)
                    if not rawget(self, "__OBJECT_ACTIVE") then
                        error("WebSocket is closed.")
                    end

                    bridge:send("websocket_send", rawget(self, "__OBJECT"), message, is_binary)
                end
            end

            if index == "Close" then
                return function(_)
                    if not rawget(self, "__OBJECT_ACTIVE") then
                        error("WebSocket is closed.")
                    end
                    rawset(self, "__OBJECT_ACTIVE", false)

                    bridge:send("websocket_close", rawget(self, "__OBJECT"))
                end
            end
        end,
        __newindex = function()
            error("WebSocket is readonly.")
        end,
        __type = "WebSocket",
    }

    function WebSocket.connect(url: string)
        -- TODO: This might break (mix up) if called quickly within a short time span

        local success = bridge:send("websocket_connect", url)
        if not success then
            error("Failed to start/connect WebSocket server", 2)
        end

        local websocket_connection = setmetatable({
            ClassName = "WebSocket",
            __OBJECT = url,
            __OBJECT_ACTIVE = true,
            __OBJECT_MESSAGE = goodsignal.new(),
            __OBJECT_CLOSE = goodsignal.new(),
        }, websocket_mt)

        websocket_connection.__OBJECT_CLOSE:Connect(function()
            websocket_connection.__OBJECT_ACTIVE = false
        end)

        game:GetService("Players").LocalPlayer.OnTeleport:Connect(function(teleportState)
            if teleportState == Enum.TeleportState.Started and websocket_connection.__OBJECT_ACTIVE then
                websocket_connection:Close()
            end
        end)

        bridge:register_callback(url .. "_message", function(...)
            websocket_connection.__OBJECT_MESSAGE:Fire(...)
        end)

        bridge:register_callback(url .. "_close", function(...)
            websocket_connection.__OBJECT_CLOSE:Fire(...)
        end)

        return websocket_connection
    end

    misc.WebSocket = WebSocket
end

misc.http = { request = misc.request }

function misc.lrm_load_script(script_id)
    local code = [[

ce_like_loadstring_fn = loadstring;
loadstring = nil;

]] .. script_env.httpget("https://api.luarmor.net/files/v3/l/" .. script_id .. ".lua")
    return script_env.loadstring(code)({ Origin = "Incognito" })
end

return function(_script_env)
    script_env = _script_env
    return misc,
        {
            ["getthreadidentity"] = { "getidentity", "getthreadcontext" },
            ["identifyexecutor"] = { "getexecutorname", "whatexecutor" },
            ["request"] = { "http_request" },
            ["setclipboard"] = { "toclipboard" },
        }
end
