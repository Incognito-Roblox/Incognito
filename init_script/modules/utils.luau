local core_gui = game:GetService("CoreGui")
local core_packages = game:GetService("CorePackages")

local utils = {}

utils.string_to_hex = function(value, offset, seperator)
    offset = offset or 227
    seperator = seperator or ""

    return string.gsub(value, ".", function(char)
        return string.format("%02X", string.byte(char) * offset) .. seperator
    end)
end

utils.hex_to_string = function(value, offset)
    offset = offset or 1

    return string.gsub(value, "..", function(char)
        return tonumber(char, 16):: number // 1
    end)
end

local _fetch_stubmodule do
    local current_module = 1
    local modules_list = {}

    for _, obj in core_gui:GetDescendants() do
        if not obj:IsA("ModuleScript") then continue end
        table.insert(modules_list, obj:Clone())
    end

    for _, obj in core_packages:GetDescendants() do
        if not obj:IsA("ModuleScript") then continue end
        table.insert(modules_list, obj:Clone())
    end

    function _fetch_stubmodule()
        local idx = math.random(1, #modules_list)

        if idx == current_module then
            return _fetch_stubmodule()
        end

        current_module = idx
        return modules_list[idx]
    end
end
utils.fetch_stubmodule = _fetch_stubmodule

return utils