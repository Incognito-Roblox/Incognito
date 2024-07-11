local cache = {}
local script_env

local CloneRefs = { Clones = setmetatable({}, { __mode = "ks" }), Originals = setmetatable({}, { __mode = "vs" }) } --*s means shrinkable, weak keys for Clones because structure is {Clone = Originals[OriginalInstance]} so when clone gets garbage collected the only ref to value inside Originals table is garbage collected too because Originals has weak values

do
    local function ReturnOriginal(instance) --! This function might be needed to call in other functions (testing required)
        local CloneInfo = CloneRefs.Clones[instance] -- *Checks if its a clone and not a real instance

        if CloneInfo then
            return CloneInfo.Original -- *Grabs the original instance then
        end
    end

    function cache.cloneref(instance)
        -- TODO Test if Instance returned by cloneref messes up our custom funcs

        -- assert(typeof(instance) == "Instance", `arg #1 must be type Instance`) -- Uncomment when we start hooking typeof
        local Original = ReturnOriginal(instance)
        if Original then
            instance = Original
        end

        local Clone = newproxy(true)
        local Mt_Clone = getmetatable(Clone)
        local Mt_Real = script_env.getrawmetatable(instance)

        local CloneInfo = CloneRefs.Originals[instance] --* If this exists then Instance has already been cloned at least once
        if not CloneInfo then
            CloneInfo = { Original = instance, __type = Mt_Real.__type }
            CloneRefs.Originals[instance] = CloneInfo
        end

        CloneRefs.Clones[Clone] = CloneInfo --* All clones of the same instance point to the same table

        for Metamethod, Value in Mt_Real do
            Mt_Clone[Metamethod] = type(Value) == "function"
                    and function(self, ...)
                        return Value(instance, ...)
                    end
                or Value
        end

        return Clone --, if Mt_Clone then Mt_Clone else nil -- Make sure this only works inside init script
    end

    function cache.compareinstances(instance, instance2)
        -- assert(typeof(instance) == "Instance", `arg #1 must be type Instance`) -- Uncomment when we start hooking typeof
        -- assert(typeof(instance2) == "Instance", `arg #2 must be type Instance`) -- Uncomment when we start hooking typeof

        local CloneInfo = CloneRefs.Clones[instance] -- *Checks if its a clone and not a real instance
        local CloneInfo2 = CloneRefs.Clones[instance2] -- *Checks if its a clone and not a real instance
        if CloneInfo then
            instance = CloneInfo.Original
        end
        if CloneInfo2 then
            instance2 = CloneInfo2.Original
        end

        return instance == instance2
    end
    -- task.spawn(function()
    --     while not script_env do
    --         task.wait()
    --     end
    --     while not script_env.getrawmetatable do
    --         task.wait()
    --     end

    --     local RealPart = Instance.new("Part")
    --     local ClonedPart = cache.cloneref(RealPart)
    --     local ClonedPart2 = cache.cloneref(RealPart)

    -- 	-- assert(typeof(ClonedPart) == "Instance", "ClonedPart is not Instance; Please hook typeof in renv")
    -- 	-- assert(typeof(ClonedPart2) == "Instance", "ClonedPart is not Instance; Please hook typeof in renv")
    -- 	warn("typeof" .. utf8.char(9989))

    --     ClonedPart.Name = "Renamed1"
    -- 	assert(tostring(RealPart) == "Renamed1", "RealPart Didn't Reflect")
    -- 	assert(tostring(ClonedPart) == "Renamed1", "ClonedPart Didn't Reflect")
    -- 	assert(tostring(ClonedPart2) == "Renamed1", "ClonedPart2 Didn't Reflect")
    -- 	warn("Property Changes" .. utf8.char(9989))

    -- 	assert(ClonedPart ~= RealPart, "ClonedPart Shouldn't be equal to RealPart")
    -- 	assert(ClonedPart ~= ClonedPart2, "ClonedPart Shouldn't be equal to ClonedPart2")
    -- 	warn("Comparison" .. utf8.char(9989))

    --     -- Clone the clone, cloneref should return new clone each time (new clone but same mt on all hm.. fluxus)
    -- 	assert(cache.compareinstances(RealPart, RealPart), "RealPart Should be equal to RealPart")
    -- 	assert(cache.compareinstances(RealPart, ClonedPart), "RealPart Should be equal to ClonedPart")
    -- 	assert(cache.compareinstances(RealPart, ClonedPart2), "RealPart Should be equal to ClonedPart2")
    -- 	assert(cache.compareinstances(ClonedPart2, ClonedPart), "ClonedPart2 Should be equal to ClonedPart")
    -- 	assert(cache.compareinstances(ClonedPart, ClonedPart2), "ClonedPart Should be equal to ClonedPart2")
    -- 	warn("compareinstances" .. utf8.char(9989))

    -- 	ClonedPart2.Parent = workspace
    -- 	ClonedPart2.Name = "Renamed2"
    -- 	assert(RealPart:GetFullName() == "Workspace.Renamed2", "RealPart GetFullName Failed")
    -- 	assert(ClonedPart:GetFullName() == "Workspace.Renamed2", "ClonedPart GetFullName Failed")
    -- 	assert(ClonedPart2:GetFullName() == "Workspace.Renamed2", "ClonedPart2 GetFullName Failed")
    -- 	warn("GetFullName" .. utf8.char(9989))

    --     local CloneInfo
    -- 	local Count = 0
    -- 	for i, v in CloneRefs.Clones do -- Must print two
    --         print(i, v)
    --         CloneInfo = v
    -- 		Count += 1
    -- 	end
    -- 	assert(Count == 2, "Clones Count should be 2")
    -- 	warn("Clones" .. utf8.char(9989))

    -- 	Count = 0
    -- 	local CloneInfo_Ref
    -- 	for i, v in CloneRefs.Originals do -- Must print one
    -- 		print(i, v) -- Last must be true
    -- 		CloneInfo_Ref = v
    -- 		Count += 1
    -- 	end
    -- 	assert(Count == 1, "Originals Count should be 2")
    -- 	assert(CloneInfo_Ref == CloneInfo, "CloneInfo should be a Reference")
    -- 	warn("Originals" .. utf8.char(9989))

    --     ClonedPart, ClonedPart2 = nil, nil
    --     task.wait(11)
    -- 	Count = 0
    -- 	warn("Clones")
    -- 	for i, v in CloneRefs.Clones do
    -- 		print(i, v)
    -- 		Count += 1
    -- 	end
    -- 	warn("Originals")
    -- 	for i, v in CloneRefs.Originals do
    -- 		print(i, v)
    -- 		Count += 1
    -- 	end
    -- 	assert(Count == 0, "Originals & Clones Tables should be Weak")
    -- 	warn("Weak Test" .. utf8.char(9989))
    -- end)
end

return function(_script_env)
    script_env = _script_env
    return cache
end
