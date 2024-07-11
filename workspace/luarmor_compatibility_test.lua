local console
local tests
local function render_console()
    console.Text = "Luarmor Compatibility Tester\n\n"
    console.Text = console.Text .. "Executor: " .. identifyexecutor() .. "\n"
    for i, v in tests do
        local pass = v.success == false and "⛔" or v.success == true and "✅" or "-"
        console.Text = console.text .. v.name .. " " .. pass .. " " .. v.result .. "\n"
    end
end
local function json_decode(str)
    return game:GetService("HttpService"):JSONDecode(str)
end
local sr_resp, gg_resp
tests = {
    {
        name = "Has custom http func",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            self.result = "request()"
            self.success = true
            if syn and syn.request then
                self.result = "syn.request()"
            elseif not request then
                self.result = "func cant be found"
                self.success = false
            end
        end,
    },
    {
        name = "Has custom WS func",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            local ws = syn and syn.websocket and syn.websocket.connect
                or WebSocket and WebSocket.connect
                or WebsocketClient
            if ws then
                self.result = tostring(ws)
                self.success = true
            else
                self.result = "func cant be found"
                self.success = false
            end
        end,
    },
    {
        name = "Custom httpfunc user-agent",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            local req = syn and syn.request or request
            sr_resp = req({ Url = "https://httpbin.org/get", Method = "Get" }).Body
            self.result = json_decode(sr_resp).headers["User-Agent"]
            self.success = true
        end,
    },
    {
        name = "game.httpget user-agent",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            gg_resp = game:HttpGet("https://httpbin.org/get")
            self.result = json_decode(gg_resp).headers["User-Agent"]
            self.success = true
        end,
    },
    {
        name = "httpget roblox-session-id header",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            local obj = json_decode(gg_resp).headers["Roblox-Session-Id"]
            if obj then
                self.result = "exists"
                self.success = true
            else
                self.result = "not present"
                self.success = false
            end
        end,
    },
    {
        name = "roblox-session-id.gameid field",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            local obj = json_decode(gg_resp).headers["Roblox-Session-Id"]
            if obj then
                obj = json_decode(obj)
                if obj.GameId then
                    self.result = tostring(obj.GameId)
                    self.success = true
                else
                    self.result = "not present"
                    self.success = false
                end
            else
                self.result = "not present"
                self.success = false
            end
        end,
    },
    {
        name = "httpget roblox-game-id header",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            local obj = json_decode(gg_resp).headers["Roblox-Game-Id"]
            if obj then
                self.result = obj
                self.success = true
            else
                self.result = "not present"
                self.success = false
            end
        end,
    },
    {
        name = "raw headers",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            local obj = game:GetService("HttpService"):JSONEncode(json_decode(sr_resp).headers)
            self.result = tostring(obj)
            self.success = true
        end,
    },
    {
        name = "test luarmor script",
        result = "(pending...)",
        success = nil,
        run_task = function(self)
            setclipboard(console.Text)
            local noclose = self
            callback = function()
                noclose.success = true
                noclose.result = "Success"
                render_console()
            end
            loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/f42f3746fb3eb60f837d3673581c14a5.lua"))()
        end,
    },
}

do
    local mouse = game:GetService("Players").LocalPlayer:GetMouse()
    local inputService = game:GetService("UserInputService")
    local ScreenGui = Instance.new("ScreenGui")
    local Frame = Instance.new("Frame")
    local ImageLabel = Instance.new("ImageLabel")
    local TextBox = Instance.new("TextBox")
    local UICorner = Instance.new("UICorner")

    ScreenGui.Parent = game:GetService("CoreGui")
    ScreenGui.Name = "LuarmorTestUtil"
    ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

    Frame.Parent = ScreenGui
    Frame.BackgroundColor3 = Color3.fromRGB(62, 181, 255)
    Frame.BackgroundTransparency = 1.000
    Frame.BorderColor3 = Color3.fromRGB(27, 42, 53)
    Frame.BorderSizePixel = 0
    Frame.Position = UDim2.new(0.4093418935, 0, 0.405985038, 0)
    Frame.Size = UDim2.new(0, 414, 0, 489)

    ImageLabel.Parent = Frame
    ImageLabel.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
    ImageLabel.BackgroundTransparency = 1.000
    ImageLabel.Position = UDim2.new(-0.0261243284, 0, -0.0164751261, 0)
    ImageLabel.Size = UDim2.new(0, 424, 0, 505)
    ImageLabel.Image = "rbxassetid://12648173604"

    TextBox.Parent = ImageLabel
    TextBox.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
    TextBox.BackgroundTransparency = 0.900
    TextBox.Position = UDim2.new(0.0895741284, 0, 0.163428098, 0)
    TextBox.Size = UDim2.new(0, 352, 0, 373)
    TextBox.Font = Enum.Font.Roboto
    TextBox.Text = ""
    TextBox.TextColor3 = Color3.fromRGB(200, 200, 200)
    TextBox.TextSize = 14.000
    TextBox.TextWrapped = true
    TextBox.TextYAlignment = Enum.TextYAlignment.Top
    TextBox.TextXAlignment = Enum.TextXAlignment.Left
    TextBox.RichText = true
    TextBox.TextEditable = false
    TextBox.ClearTextOnFocus = false

    UICorner.CornerRadius = UDim.new(0.0299999993, 0)
    UICorner.Parent = TextBox
    console = TextBox
    local frame = Frame
    local s, event = pcall(function()
        return frame.MouseEnter
    end)

    if s then
        frame.Active = true

        event:Connect(function()
            local input = frame.InputBegan:Connect(function(key)
                if key.UserInputType == Enum.UserInputType.MouseButton1 then
                    local objectPosition =
                        Vector2.new(mouse.X - frame.AbsolutePosition.X, mouse.Y - frame.AbsolutePosition.Y)
                    while task.wait() and inputService:IsMouseButtonPressed(Enum.UserInputType.MouseButton1) do
                        pcall(function()
                            frame:TweenPosition(
                                UDim2.new(
                                    0,
                                    mouse.X - objectPosition.X + (frame.Size.X.Offset * frame.AnchorPoint.X),
                                    0,
                                    mouse.Y - objectPosition.Y + (frame.Size.Y.Offset * frame.AnchorPoint.Y)
                                ),
                                "Out",
                                "Linear",
                                0.1,
                                true
                            )
                        end)
                    end
                end
            end)

            local leave
            leave = frame.MouseLeave:Connect(function()
                input:Disconnect()
                leave:Disconnect()
            end)
        end)
    end
end
render_console()
task.wait(1)
for i, v in tests do
    v:run_task()
    task.wait(0.1)
    render_console()
end
console.Text = console.Text .. "\nCOPIED TO CLIPBOARD! ✅✅✅✅"
setclipboard(console.Text)
