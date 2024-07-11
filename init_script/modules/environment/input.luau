--https://github.com/MaximumADHD/Roblox-Client-Tracker/tree/roblox/LuaPackages/Packages/_Index/Rhodium/Rhodium/InputTypes
local UserInputService = game:GetService("UserInputService")
local VirtualInputManager = Instance.new("VirtualInputManager")

local input, alias =
    {}, {
        ["isrbxactive"] = { "isgameactive", "iswindowactive" },
        ["keyclick"] = { "hitkey" },
    }

do -- IsFocused
    local window_focused = true -- TODO Find a better way instead of Assuming (Maybe we could force focus)

    UserInputService.WindowFocusReleased:Connect(function()
        window_focused = false
    end)
    UserInputService.WindowFocused:Connect(function()
        window_focused = true
    end)

    function input.isrbxactive()
        return window_focused
    end
end

-- QuotedDouble Hash Dollar Percent Ampersand LeftParenthesis RightParenthesis Asterisk Underscore Tilde Colon Plus Pipe LessThan GreaterThan Question At Caret LeftCurly RightCurly are all deprecated

-- basic virtual key code -> roblox KeyCode map (for backwards compatibility)
-- https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes
-- https://developer.roblox.com/api-reference/enum/KeyCode

--[[ --TODO Map these to mouse functions?

VK_LBUTTON 	0x01 	Left mouse button
VK_RBUTTON 	0x02 	Right mouse button

VK_MBUTTON 	0x04 	Middle mouse button
VK_XBUTTON1 	0x05 	X1 mouse button
VK_XBUTTON2 	0x06 	X2 mouse button

]]

local map = {
    -- [0x03] = Enum.KeyCode.LeftControl + Enum.KeyCode.Break

    [0x10] = Enum.KeyCode.LeftShift, -- Ambiguation Shift
    [0x11] = Enum.KeyCode.LeftControl, -- Ambiguation Ctrl
    [0x12] = Enum.KeyCode.LeftAlt, -- Ambiguation Alt

    -- TODO These need to only appear once (it will be a problem if we move some keycode from beginning to end, currently we only need to do the opposite luckily)
    [0x14] = Enum.KeyCode.CapsLock,

    [0x1F] = Enum.KeyCode.Mode,

    [0x21] = Enum.KeyCode.PageUp,
    [0x22] = Enum.KeyCode.PageDown,
    [0x23] = Enum.KeyCode.End,
    [0x24] = Enum.KeyCode.Home,
    [0x25] = Enum.KeyCode.Left,
    [0x26] = Enum.KeyCode.Up,
    [0x27] = Enum.KeyCode.Right,
    [0x28] = Enum.KeyCode.Down,
    [0x29] = false,
    [0x2A] = Enum.KeyCode.Print, -- Not sure
    [0x2B] = false,
    [0x2C] = Enum.KeyCode.Print,
    [0x2D] = Enum.KeyCode.Insert,
    [0x2E] = Enum.KeyCode.Delete,
    [0x2F] = Enum.KeyCode.Help,

    [0x5B] = Enum.KeyCode.LeftSuper,
    [0x5C] = Enum.KeyCode.RightSuper,
    [0x5D] = Enum.KeyCode.Menu, -- Not sure
    [0x5E] = false,
    [0x5F] = false,

    [0x6A] = Enum.KeyCode.KeypadMultiply,
    [0x6B] = Enum.KeyCode.KeypadPlus,
    [0x6C] = false,
    [0x6D] = Enum.KeyCode.KeypadMinus,
    [0x6E] = Enum.KeyCode.KeypadPeriod,
    [0x6F] = Enum.KeyCode.KeypadDivide,

    [0x7F] = false,

    [0x90] = Enum.KeyCode.NumLock,
    [0x91] = Enum.KeyCode.ScrollLock,

    [0xA0] = Enum.KeyCode.LeftShift,
    [0xA1] = Enum.KeyCode.RightShift,
    [0xA2] = Enum.KeyCode.LeftControl,
    [0xA3] = Enum.KeyCode.RightControl,
    [0xA4] = Enum.KeyCode.LeftAlt,
    [0xA5] = Enum.KeyCode.RightAlt,

    [0xBA] = Enum.KeyCode.Semicolon,
    [0xBB] = Enum.KeyCode.Plus,
    [0xBC] = Enum.KeyCode.Comma,
    [0xBD] = Enum.KeyCode.Minus,
    [0xBE] = Enum.KeyCode.Period,
    [0xBF] = Enum.KeyCode.Slash,

    [0xC0] = Enum.KeyCode.Backquote,

    [0xDB] = Enum.KeyCode.LeftBracket,
    [0xDC] = Enum.KeyCode.BackSlash,
    [0xDD] = Enum.KeyCode.RightBracket,
    [0xDE] = Enum.KeyCode.Quote,

    [0xE2] = Enum.KeyCode.LessThan,

    [0xFE] = Enum.KeyCode.Clear, -- Not sure
}
do -- Map Virtual Keys to KeyCode Enum
    local function virtual_to_keycode(value)
        for i, v in Enum.KeyCode:GetEnumItems() do
            if v.Value == value then
                return v
            end
        end
    end
    -- Re-Map
    for i = 0, 25 do
        map[i + 0x41] = virtual_to_keycode(i + 97)
    end -- A-Z
    for i = 0, 9 do
        map[i + 0x60] = virtual_to_keycode(i + 256)
    end -- Keypad 0-9
    for i = 0, 14 do
        map[i + 0x70] = virtual_to_keycode(i + 282)
    end -- Function 1-15

    for i, v in Enum.KeyCode:GetEnumItems() do -- ? Maybe blacklist Enum's containing "World" in the name
        local Override = map[v.Value]

        if Override == nil then
            if string.find(v.Name, "World", nil, true) then
                continue
            end
            map[v.Value] = v
        elseif Override == false then
            map[v.Value] = nil
        end
    end
end

do -- Keyboard
    local function get_keycode(key)
        local Type = typeof(key)
        if Type ~= "EnumItem" then
            if Type == "string" then
                key = tonumber(key)
            end
            key = map[key]
            assert(key, "Unable to map key to Enum.KeyCode. Use a Enum.KeyCode instead") -- ? We could also return Unknown keycode instead of this
        end
        return key
    end

    function input.keypress(key, isRepeatedKey)
        VirtualInputManager:SendKeyEvent(true, get_keycode(key), isRepeatedKey or false, nil)
    end

    function input.keyrelease(key, isRepeatedKey)
        VirtualInputManager:SendKeyEvent(false, get_keycode(key), isRepeatedKey or false, nil)
    end

    function input.keyclick(...)
        input.keypress(...)
        input.keyrelease(...)
    end
end

local Input = {
    KeyPress = input.keyclick,
    KeyDown = input.keypress,
    KeyUp = input.keyrelease,
}

do -- Mouse
    -- VirtualInputManager is typed to disallow a nil window, but it does not
    -- throw errors and tests rely on it `nil` being allowed
    local function mouse_generalized(mouseButton, isDown)
        return function(x, y, repeatCount)
            VirtualInputManager:SendMouseButtonEvent(
                x or UserInputService:GetMouseLocation().X,
                y or UserInputService:GetMouseLocation().Y,
                mouseButton,
                isDown,
                nil,
                repeatCount or 0
            )
        end
    end

    local mouse_map = { "LeftClick", "RightClick", "MiddleClick" }

    for i = 0, 2 do
        local lua_index = i + 1
        local base_name = "mouse" .. lua_index
        local press, release = mouse_generalized(i, true), mouse_generalized(i, false)

        local function click(...)
            press(...)
            release(...)
        end

        local up_name, down_name = base_name .. "press", base_name .. "release"
        input[up_name] = press
        input[down_name] = release
        input[base_name .. "click"] = click

        Input[mouse_map[lua_index]] = function(action)
            if 1 == action then
                press()
            elseif 2 == action then
                release()
            else
                click()
            end
        end

        alias[up_name] = { base_name .. "up" }
        alias[down_name] = { base_name .. "down" }
    end

    function input.mousemoveabs(x, y)
        VirtualInputManager:SendMouseMoveEvent(
            x or UserInputService:GetMouseLocation().X,
            y or UserInputService:GetMouseLocation().Y,
            nil
        )
    end

    function input.mousemoverel(x, y)
        -- x,y need to be specified here or we need a fallback (0)
        input.mousemoveabs(
            x and UserInputService:GetMouseLocation().X + x,
            y and UserInputService:GetMouseLocation().Y + y
        )
    end

    Input.MoveMouse = input.mousemoverel
    Input.ScrollMouse = input.mousescroll

    function input.mousescroll(pixels, x, y)
        if type(pixels) == "boolean" then
            pixels = pixels and 120 or -120
        end

        local isForwardScroll = pixels >= 0 -- input.Position.Z is 1 when forward, -1 otherwise

        for i = 1, math.abs(pixels // 120) do
            VirtualInputManager:SendMouseWheelEvent(
                x or UserInputService:GetMouseLocation().X,
                y or UserInputService:GetMouseLocation().Y,
                isForwardScroll,
                nil
            )
            VirtualInputManager:WaitForInputEventsProcessed()
        end
    end
end

input.Input = Input

return function()
    return input, alias
end
