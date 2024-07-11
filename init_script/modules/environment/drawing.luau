-- objects
local camera = workspace.CurrentCamera

local drawing_container = Instance.new("ScreenGui")
drawing_container.Name = "Drawing"
drawing_container.IgnoreGuiInset = true
drawing_container.DisplayOrder = 0x7fffffff

local wedge_template = Instance.new("ImageLabel")
wedge_template.BackgroundTransparency = 1
wedge_template.AnchorPoint = Vector2.one / 2
wedge_template.BorderSizePixel = 0
wedge_template.Image = "rbxassetid://0"
wedge_template.ImageColor3 = Color3.new()
wedge_template.ZIndex = 0

-- variables
local vect2_half = Vector2.one / 2
local drawing_idx = 0

local drawing_obj_reg = {}

local base_drawing_obj = setmetatable({
    Visible = true,
    ZIndex = 0,
    Transparency = 1,
    Color = Color3.new(),
    Remove = function(self)
        setmetatable(self, nil)

        local obj_idx = table.find(drawing_obj_reg, self)
        if obj_idx then
            table.remove(drawing_obj_reg, obj_idx)
        end
    end,
}, {
    __add = function(t1, t2)
        local result = table.clone(t1)

        for index, value in t2 do
            result[index] = value
        end
        return result
    end,
})

local drawing_fonts_list = {
    [0] = Font.fromEnum(Enum.Font.BuilderSans),
    Font.fromEnum(Enum.Font.Arial),
    Font.fromEnum(Enum.Font.Nunito),
    Font.fromEnum(Enum.Font.RobotoMono),
}

local triangle_assets = {
    left = "rbxassetid://319692171",
    right = "rbxassetid://319692151",
}

-- function
local function get_font_from_idx(font_idx: number): Font
    return drawing_fonts_list[font_idx]
end

local function convert_dtransparency(transparency: number): number
    return math.clamp(1 - transparency, 0, 1)
end

-- from egomoose: https://github.com/EgoMoose/Articles/blob/master/2d%20triangles/2d%20triangles.md
local function new_2d_triangle(parent)
    local wedges = {
        w1 = wedge_template:Clone(),
        w2 = wedge_template:Clone(),
    }
    local is_destroyed = false

    wedges.w1.Parent = parent
    wedges.w2.Parent = parent

    local function construct_triangle(point_a, point_b, point_c)
        if not (wedges.w1.Visible and wedges.w2.Visible) then
            return
        end

        if is_destroyed then
            return
        end

        local ab, ac, bc = point_b - point_a, point_c - point_a, point_c - point_b
        local abd, acd, bcd = ab:Dot(ab), ac:Dot(ac), bc:Dot(bc)

        if abd > acd and abd > bcd then
            point_c, point_a = point_a, point_c
        elseif acd > bcd and acd > abd then
            point_a, point_b = point_b, point_a
        end

        ab, ac, bc = (point_b - point_a), (point_c - point_a), (point_c - point_b)

        local unit = bc.Unit
        local height = unit:Cross(ab)
        local flip = (height >= 0)
        local theta = math.deg(math.atan2(unit.y, unit.x)) + (if flip then 0 else 180)

        local m1 = (point_a + point_b) / 2
        local m2 = (point_a + point_c) / 2

        wedges.w1.Image = (if flip then triangle_assets.right else triangle_assets.left)
        wedges.w1.AnchorPoint = vect2_half
        wedges.w1.Size = UDim2.fromOffset(math.abs(unit:Dot(ab)), height)
        wedges.w1.Position = UDim2.fromOffset(m1.x, m1.y)
        wedges.w1.Rotation = theta

        wedges.w2.Image = (if flip then triangle_assets.left else triangle_assets.right)
        wedges.w2.AnchorPoint = vect2_half
        wedges.w2.Size = UDim2.fromOffset(math.abs(unit:Dot(ac)), height)
        wedges.w2.Position = UDim2.fromOffset(m2.x, m2.y)
        wedges.w2.Rotation = theta
    end

    local function destroy_triangle()
        is_destroyed = true

        for _, obj in wedges do
            obj:Destroy()
        end
        table.clear(wedges)
    end
    return construct_triangle, destroy_triangle, wedges
end
-- main
local drawing_lib = {}
drawing_lib.Fonts = {
    ["UI"] = 0,
    ["System"] = 1,
    ["Plex"] = 2,
    ["Monospace"] = 3,
}
do
    local function new(drawing_type)
        drawing_idx += 1
        local drawing_obj = {}

        if drawing_type == "Line" then
            local drawing_info = (
                {
                    From = Vector2.zero,
                    To = Vector2.zero,
                    Thickness = 1,
                } + base_drawing_obj
            )

            local lineFrame = Instance.new("Frame")
            lineFrame.Name = drawing_idx
            lineFrame.AnchorPoint = (Vector2.one * 0.5)
            lineFrame.BorderSizePixel = 0

            lineFrame.BackgroundColor3 = drawing_info.Color
            lineFrame.Visible = drawing_info.Visible
            lineFrame.ZIndex = drawing_info.ZIndex
            lineFrame.BackgroundTransparency = convert_dtransparency(drawing_info.Transparency)

            lineFrame.Size = UDim2.new()

            lineFrame.Parent = drawing_container

            return setmetatable(drawing_obj, {
                __newindex = function(_, index, value)
                    if type(drawing_info[index]) == "nil" then
                        return
                    end

                    if index == "From" then
                        local direction = (drawing_info.To - value)
                        local center = (drawing_info.To + value) / 2
                        local distance = direction.Magnitude
                        local theta = math.deg(math.atan2(direction.Y, direction.X))

                        lineFrame.Position = UDim2.fromOffset(center.X, center.Y)
                        lineFrame.Rotation = theta
                        lineFrame.Size = UDim2.fromOffset(distance, drawing_info.Thickness)
                    elseif index == "To" then
                        local direction = (value - drawing_info.From)
                        local center = (value + drawing_info.From) / 2
                        local distance = direction.Magnitude
                        local theta = math.deg(math.atan2(direction.Y, direction.X))

                        lineFrame.Position = UDim2.fromOffset(center.X, center.Y)
                        lineFrame.Rotation = theta
                        lineFrame.Size = UDim2.fromOffset(distance, drawing_info.Thickness)
                    elseif index == "Thickness" then
                        local distance = (drawing_info.To - drawing_info.From).Magnitude

                        lineFrame.Size = UDim2.fromOffset(distance, value)
                    elseif index == "Visible" then
                        lineFrame.Visible = value
                    elseif index == "ZIndex" then
                        lineFrame.ZIndex = value
                    elseif index == "Transparency" then
                        lineFrame.BackgroundTransparency = convert_dtransparency(value)
                    elseif index == "Color" then
                        lineFrame.BackgroundColor3 = value
                    end
                    drawing_info[index] = value
                end,
                __index = function(self, index)
                    if index == "Remove" or index == "Destroy" then
                        return function()
                            lineFrame:Destroy()
                            drawing_info.Remove(self)
                            return drawing_info:Remove()
                        end
                    end
                    return drawing_info[index]
                end,
            })
        elseif drawing_type == "Text" then
            local drawing_info = (
                {
                    Text = "",
                    Font = drawing_lib.Fonts.UI,
                    Size = 0,
                    Position = Vector2.zero,
                    Center = false,
                    Outline = false,
                    OutlineColor = Color3.new(),
                } + base_drawing_obj
            )

            local textLabel, uiStroke = Instance.new("TextLabel"), Instance.new("UIStroke")
            textLabel.Name = drawing_idx
            textLabel.AnchorPoint = (Vector2.one * 0.5)
            textLabel.BorderSizePixel = 0
            textLabel.BackgroundTransparency = 1

            textLabel.Visible = drawing_info.Visible
            textLabel.TextColor3 = drawing_info.Color
            textLabel.TextTransparency = convert_dtransparency(drawing_info.Transparency)
            textLabel.ZIndex = drawing_info.ZIndex

            textLabel.FontFace = get_font_from_idx(drawing_info.Font)
            textLabel.TextSize = drawing_info.Size

            textLabel:GetPropertyChangedSignal("TextBounds"):Connect(function()
                local textBounds = textLabel.TextBounds
                local offset = textBounds / 2

                textLabel.Size = UDim2.fromOffset(textBounds.X, textBounds.Y)
                textLabel.Position = UDim2.fromOffset(
                    drawing_info.Position.X + (if not drawing_info.Center then offset.X else 0),
                    drawing_info.Position.Y + offset.Y
                )
            end)

            uiStroke.Thickness = 1
            uiStroke.Enabled = drawing_info.Outline
            uiStroke.Color = drawing_info.Color

            textLabel.Parent, uiStroke.Parent = drawing_container, textLabel
            return setmetatable(drawing_obj, {
                __newindex = function(_, index, value)
                    if type(drawing_info[index]) == "nil" then
                        return
                    end

                    if index == "Text" then
                        textLabel.Text = value
                    elseif index == "Font" then
                        value = math.clamp(value, 0, 3)
                        textLabel.FontFace = get_font_from_idx(value)
                    elseif index == "Size" then
                        textLabel.TextSize = value
                    elseif index == "Position" then
                        local offset = textLabel.TextBounds / 2

                        textLabel.Position = UDim2.fromOffset(
                            value.X + (if not drawing_info.Center then offset.X else 0),
                            value.Y + offset.Y
                        )
                    elseif index == "Center" then
                        local position = (if value then camera.ViewportSize / 2 else drawing_info.Position)

                        textLabel.Position = UDim2.fromOffset(position.X, position.Y)
                    elseif index == "Outline" then
                        uiStroke.Enabled = value
                    elseif index == "OutlineColor" then
                        uiStroke.Color = value
                    elseif index == "Visible" then
                        textLabel.Visible = value
                    elseif index == "ZIndex" then
                        textLabel.ZIndex = value
                    elseif index == "Transparency" then
                        local transparency = convert_dtransparency(value)

                        textLabel.TextTransparency = transparency
                        uiStroke.Transparency = transparency
                    elseif index == "Color" then
                        textLabel.TextColor3 = value
                    end
                    drawing_info[index] = value
                end,
                __index = function(self, index)
                    if index == "Remove" or index == "Destroy" then
                        return function()
                            textLabel:Destroy()
                            drawing_info.Remove(self)
                            return drawing_info:Remove()
                        end
                    elseif index == "TextBounds" then
                        return textLabel.TextBounds
                    end
                    return drawing_info[index]
                end,
            })
        elseif drawing_type == "Circle" then
            local drawing_info = (
                {
                    Radius = 150,
                    Position = Vector2.zero,
                    Thickness = 0.7,
                    Filled = false,
                } + base_drawing_obj
            )

            local circleFrame, uiCorner, uiStroke =
                Instance.new("Frame"), Instance.new("UICorner"), Instance.new("UIStroke")
            circleFrame.Name = drawing_idx
            circleFrame.AnchorPoint = (Vector2.one * 0.5)
            circleFrame.BorderSizePixel = 0

            circleFrame.BackgroundTransparency = (
                if drawing_info.Filled then convert_dtransparency(drawing_info.Transparency) else 1
            )
            circleFrame.BackgroundColor3 = drawing_info.Color
            circleFrame.Visible = drawing_info.Visible
            circleFrame.ZIndex = drawing_info.ZIndex

            uiCorner.CornerRadius = UDim.new(1, 0)
            circleFrame.Size = UDim2.fromOffset(drawing_info.Radius, drawing_info.Radius)

            uiStroke.Thickness = drawing_info.Thickness
            uiStroke.Enabled = not drawing_info.Filled
            uiStroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border

            circleFrame.Parent, uiCorner.Parent, uiStroke.Parent = drawing_container, circleFrame, circleFrame
            return setmetatable(drawing_obj, {
                __newindex = function(_, index, value)
                    if type(drawing_info[index]) == "nil" then
                        return
                    end

                    if index == "Radius" then
                        local radius = value * 2
                        circleFrame.Size = UDim2.fromOffset(radius, radius)
                    elseif index == "Position" then
                        circleFrame.Position = UDim2.fromOffset(value.X, value.Y)
                    elseif index == "Thickness" then
                        value = math.clamp(value, 0.6, 0x7fffffff)
                        uiStroke.Thickness = value
                    elseif index == "Filled" then
                        circleFrame.BackgroundTransparency = (
                            if value then convert_dtransparency(drawing_info.Transparency) else 1
                        )
                        uiStroke.Enabled = not value
                    elseif index == "Visible" then
                        circleFrame.Visible = value
                    elseif index == "ZIndex" then
                        circleFrame.ZIndex = value
                    elseif index == "Transparency" then
                        local transparency = convert_dtransparency(value)

                        circleFrame.BackgroundTransparency = (if drawing_info.Filled then transparency else 1)
                        uiStroke.Transparency = transparency
                    elseif index == "Color" then
                        circleFrame.BackgroundColor3 = value
                        uiStroke.Color = value
                    end
                    drawing_info[index] = value
                end,
                __index = function(self, index)
                    if index == "Remove" or index == "Destroy" then
                        return function()
                            circleFrame:Destroy()
                            drawing_info.Remove(self)
                            return drawing_info:Remove()
                        end
                    end
                    return drawing_info[index]
                end,
            })
        elseif drawing_type == "Square" then
            local drawing_info = (
                {
                    Size = Vector2.zero,
                    Position = Vector2.zero,
                    Thickness = 0.7,
                    Filled = false,
                } + base_drawing_obj
            )

            local squareFrame, uiStroke = Instance.new("Frame"), Instance.new("UIStroke")
            squareFrame.Name = drawing_idx
            squareFrame.BorderSizePixel = 0

            squareFrame.BackgroundTransparency = (
                if drawing_info.Filled then convert_dtransparency(drawing_info.Transparency) else 1
            )
            squareFrame.ZIndex = drawing_info.ZIndex
            squareFrame.BackgroundColor3 = drawing_info.Color
            squareFrame.Visible = drawing_info.Visible

            uiStroke.Thickness = drawing_info.Thickness
            uiStroke.Enabled = not drawing_info.Filled
            uiStroke.LineJoinMode = Enum.LineJoinMode.Miter

            squareFrame.Parent, uiStroke.Parent = drawing_container, squareFrame
            return setmetatable(drawing_obj, {
                __newindex = function(_, index, value)
                    if type(drawing_info[index]) == "nil" then
                        return
                    end

                    if index == "Size" then
                        squareFrame.Size = UDim2.fromOffset(value.X, value.Y)
                    elseif index == "Position" then
                        squareFrame.Position = UDim2.fromOffset(value.X, value.Y)
                    elseif index == "Thickness" then
                        value = math.clamp(value, 0.6, 0x7fffffff)
                        uiStroke.Thickness = value
                    elseif index == "Filled" then
                        squareFrame.BackgroundTransparency = (
                            if value then convert_dtransparency(drawing_info.Transparency) else 1
                        )
                        uiStroke.Enabled = not value
                    elseif index == "Visible" then
                        squareFrame.Visible = value
                    elseif index == "ZIndex" then
                        squareFrame.ZIndex = value
                    elseif index == "Transparency" then
                        local transparency = convert_dtransparency(value)

                        squareFrame.BackgroundTransparency = (if drawing_info.Filled then transparency else 1)
                        uiStroke.Transparency = transparency
                    elseif index == "Color" then
                        uiStroke.Color = value
                        squareFrame.BackgroundColor3 = value
                    end
                    drawing_info[index] = value
                end,
                __index = function(self, index)
                    if index == "Remove" or index == "Destroy" then
                        return function()
                            squareFrame:Destroy()
                            drawing_info.Remove(self)
                            return drawing_info:Remove()
                        end
                    end
                    return drawing_info[index]
                end,
            })
        elseif drawing_type == "Image" then
            local drawing_info = (
                {
                    Data = "",
                    DataURL = "rbxassetid://0",
                    Size = Vector2.zero,
                    Position = Vector2.zero,
                } + base_drawing_obj
            )

            local imageFrame = Instance.new("ImageLabel")
            imageFrame.Name = drawing_idx
            imageFrame.BorderSizePixel = 0
            imageFrame.ScaleType = Enum.ScaleType.Stretch
            imageFrame.BackgroundTransparency = 1

            imageFrame.Visible = drawing_info.Visible
            imageFrame.ZIndex = drawing_info.ZIndex
            imageFrame.ImageTransparency = convert_dtransparency(drawing_info.Transparency)
            imageFrame.ImageColor3 = drawing_info.Color

            imageFrame.Parent = drawing_container
            return setmetatable(drawing_obj, {
                __newindex = function(_, index, value)
                    if type(drawing_info[index]) == "nil" then
                        return
                    end

                    if index == "DataURL" then -- temporary property
                        imageFrame.Image = value
                    elseif index == "Size" then
                        imageFrame.Size = UDim2.fromOffset(value.X, value.Y)
                    elseif index == "Position" then
                        imageFrame.Position = UDim2.fromOffset(value.X, value.Y)
                    elseif index == "Visible" then
                        imageFrame.Visible = value
                    elseif index == "ZIndex" then
                        imageFrame.ZIndex = value
                    elseif index == "Transparency" then
                        imageFrame.ImageTransparency = convert_dtransparency(value)
                    elseif index == "Color" then
                        imageFrame.ImageColor3 = value
                    end
                    drawing_info[index] = value
                end,
                __index = function(self, index)
                    if index == "Remove" or index == "Destroy" then
                        return function()
                            imageFrame:Destroy()
                            drawing_info.Remove(self)
                            return drawing_info:Remove()
                        end
                    end
                    return drawing_info[index]
                end,
            })
        elseif drawing_type == "Quad" then
            local drawing_info = (
                {
                    PointA = Vector2.zero,
                    PointB = Vector2.zero,
                    PointC = Vector2.zero,
                    PointD = Vector2.zero,
                    Thickness = 1,
                    Filled = false,
                } + base_drawing_obj
            )

            local line_points = {}
            line_points.A = drawing_lib.new("Line")
            line_points.B = drawing_lib.new("Line")
            line_points.C = drawing_lib.new("Line")
            line_points.D = drawing_lib.new("Line")

            local construct_tri1, remove_tri1, wedges1 = new_2d_triangle(drawing_container)
            local construct_tri2, remove_tri2, wedges2 = new_2d_triangle(drawing_container)

            construct_tri1(drawing_info.PointA, drawing_info.PointB, drawing_info.PointC)
            construct_tri2(drawing_info.PointA, drawing_info.PointC, drawing_info.PointD)
            wedges1.w1.Visible = drawing_info.Filled
            wedges1.w2.Visible = drawing_info.Filled
            wedges2.w1.Visible = drawing_info.Filled
            wedges2.w2.Visible = drawing_info.Filled

            return setmetatable(drawing_obj, {
                __newindex = function(_, index, value)
                    if type(drawing_info[index]) == "nil" then
                        return
                    end

                    if index == "PointA" then
                        line_points.A.From = value
                        line_points.B.To = value
                        construct_tri1(value, drawing_info.PointB, drawing_info.PointC)
                        construct_tri2(value, drawing_info.PointC, drawing_info.PointD)
                    elseif index == "PointB" then
                        line_points.B.From = value
                        line_points.C.To = value
                        construct_tri1(drawing_info.PointA, value, drawing_info.PointC)
                    elseif index == "PointC" then
                        line_points.C.From = value
                        line_points.D.To = value
                        construct_tri1(drawing_info.PointA, drawing_info.PointB, value)
                        construct_tri2(drawing_info.PointA, value, drawing_info.PointD)
                    elseif index == "PointD" then
                        line_points.D.From = value
                        line_points.A.To = value
                        construct_tri2(drawing_info.PointA, drawing_info.PointC, value)
                    elseif
                        index == "Thickness"
                        or index == "Visible"
                        or index == "Color"
                        or index == "Transparency"
                        or index == "ZIndex"
                    then
                        for _, line_obj in line_points do
                            line_obj[index] = value
                        end

                        if index == "Visible" then
                            wedges1.w1.Visible = (drawing_info.Filled and value)
                            wedges1.w2.Visible = (drawing_info.Filled and value)
                            wedges2.w1.Visible = (drawing_info.Filled and value)
                            wedges2.w2.Visible = (drawing_info.Filled and value)
                        elseif index == "ZIndex" then
                            wedges1.w1.ZIndex = value
                            wedges1.w2.ZIndex = value
                            wedges2.w1.ZIndex = value
                            wedges2.w2.ZIndex = value
                        elseif index == "Color" then
                            wedges1.w1.ImageColor3 = value
                            wedges1.w2.ImageColor3 = value
                            wedges2.w1.ImageColor3 = value
                            wedges2.w2.ImageColor3 = value
                        elseif index == "Transparency" then
                            wedges1.w1.ImageTransparency = convert_dtransparency(value)
                            wedges1.w2.ImageTransparency = convert_dtransparency(value)
                            wedges2.w1.ImageTransparency = convert_dtransparency(value)
                            wedges2.w2.ImageTransparency = convert_dtransparency(value)
                        end
                    elseif index == "Filled" then
                        wedges1.w1.Visible = (drawing_info.Visible and value)
                        wedges1.w2.Visible = (drawing_info.Visible and value)
                        wedges2.w1.Visible = (drawing_info.Visible and value)
                        wedges2.w2.Visible = (drawing_info.Visible and value)
                    end
                    drawing_info[index] = value
                end,
                __index = function(self, index)
                    if index == "Remove" or index == "Destroy" then
                        return function()
                            for _, line_obj in line_points do
                                line_obj:Remove()
                            end

                            remove_tri1()
                            remove_tri2()
                            drawing_info.Remove(self)
                            return drawing_info:Remove()
                        end
                    end
                    return drawing_info[index]
                end,
            })
        elseif drawing_type == "Triangle" then
            local drawing_info = (
                {
                    PointA = Vector2.zero,
                    PointB = Vector2.zero,
                    PointC = Vector2.zero,
                    Thickness = 1,
                    Filled = false,
                } + base_drawing_obj
            )

            local line_points = {}
            line_points.A = drawing_lib.new("Line")
            line_points.B = drawing_lib.new("Line")
            line_points.C = drawing_lib.new("Line")

            local construct_tri1, remove_tri1, wedges1 = new_2d_triangle(drawing_container)

            construct_tri1(drawing_info.PointA, drawing_info.PointB, drawing_info.PointC)
            wedges1.w1.Visible = drawing_info.Filled
            wedges1.w2.Visible = drawing_info.Filled

            return setmetatable(drawing_obj, {
                __newindex = function(_, index, value)
                    if type(drawing_info[index]) == "nil" then
                        return
                    end

                    if index == "PointA" then
                        line_points.A.From = value
                        line_points.B.To = value
                        construct_tri1(value, drawing_info.PointB, drawing_info.PointC)
                    elseif index == "PointB" then
                        line_points.B.From = value
                        line_points.C.To = value
                        construct_tri1(drawing_info.PointA, value, drawing_info.PointC)
                    elseif index == "PointC" then
                        line_points.C.From = value
                        line_points.A.To = value
                        construct_tri1(drawing_info.PointA, drawing_info.PointB, value)
                    elseif
                        index == "Thickness"
                        or index == "Visible"
                        or index == "Color"
                        or index == "Transparency"
                        or index == "ZIndex"
                    then
                        for _, line_obj in line_points do
                            line_obj[index] = value
                        end

                        if index == "Visible" then
                            wedges1.w1.Visible = (drawing_info.Filled and value)
                            wedges1.w2.Visible = (drawing_info.Filled and value)
                        elseif index == "ZIndex" then
                            wedges1.w1.ZIndex = value
                            wedges1.w2.ZIndex = value
                        elseif index == "Color" then
                            wedges1.w1.ImageColor3 = value
                            wedges1.w2.ImageColor3 = value
                        elseif index == "Transparency" then
                            wedges1.w1.ImageTransparency = convert_dtransparency(value)
                            wedges1.w2.ImageTransparency = convert_dtransparency(value)
                        end
                    elseif index == "Filled" then
                        wedges1.w1.Visible = (drawing_info.Visible and value)
                        wedges1.w2.Visible = (drawing_info.Visible and value)
                    end
                    drawing_info[index] = value
                end,
                __index = function(self, index)
                    if index == "Remove" or index == "Destroy" then
                        return function()
                            for _, line_obj in line_points do
                                line_obj:Remove()
                            end

                            remove_tri1()
                            drawing_info.Remove(self)
                            return drawing_info:Remove()
                        end
                    end
                    return drawing_info[index]
                end,
            })
        end
        return error(`Drawing object "{drawing_type}" doesn't exist`, 2)
    end

    function drawing_lib.new(...)
        local drawing_obj = new(...)
        table.insert(drawing_obj_reg, drawing_obj)
        return drawing_obj
    end
end
-- * misc drawing funcs

local function clearDrawCache()
    for _, drawing_obj in drawing_obj_reg do
        if not drawing_obj then
            continue
        end
        drawing_obj:Remove()
    end
    table.clear(drawing_obj_reg)
end

local function isRenderObject(object): boolean
    local objPos = table.find(drawing_obj_reg, object)

    return (if objPos then (type(drawing_obj_reg[objPos]) == "table") else false)
end

local function getRenderProperty(object, property: string): any
    local objPos = table.find(drawing_obj_reg, object)
    if not objPos then
        return error(`arg #1 not a valid render object`)
    end

    return object[property]
end

local function setRenderProperty(object, property: string, value: any)
    local objPos = table.find(drawing_obj_reg, object)
    if not objPos then
        return error(`arg #1 not a valid render object`)
    end

    if type(object[property]) == "nil" then
        return error(`'{property}' is not a valid render property`)
    end

    object[property] = value
end

return function(script_env)
    task.spawn(function()
        while not script_env.gethui do
            task.wait()
        end

        drawing_container.Parent = script_env.gethui()
    end)

    return {
        ["Drawing"] = drawing_lib,

        ["cleardrawcache"] = clearDrawCache,
        ["isrenderobj"] = isRenderObject,

        ["getrenderproperty"] = getRenderProperty,
        ["setrenderproperty"] = setRenderProperty,
    }
end
