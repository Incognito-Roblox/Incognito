-- ! Meant for Studio

local GlobalSettings, GlobalBasicSettings = settings(), UserSettings()
local service = setmetatable({}, {
	__index = function(self, index)
		local Service = game:GetService(index)
			or GlobalSettings:GetService(index)
			or GlobalBasicSettings:GetService(index)
		self[index] = Service
		return Service
	end,
})
local List
do
	local mt
	mt = {
		__index = function(self, index)
			local Category = rawget(self, index)
			if not Category then
				Category = setmetatable({}, mt)
				self[index] = Category
			end
			return Category
		end,
	}
	List = setmetatable({ Accessible = setmetatable({}, mt), Inaccessible = setmetatable({}, mt) }, {
		__index = function(self, Accessible)
			return Accessible and self.Accessible or self.Inaccessible
		end,
	})
end
local Capabilities = { None = true, PluginSecurity = true, LocalUserSecurity = true, RobloxScriptSecurity = true }

service.HttpService.HttpEnabled = true

do
	local function FetchAPI()
		local API_Dump_Url =
			"https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/Mini-API-Dump.json"
		local API_Dump = service.HttpService:GetAsync(API_Dump_Url, true)
		local API_Classes = service.HttpService:JSONDecode(API_Dump).Classes

		for _index_0 = 1, #API_Classes do
			local API_Class = API_Classes[_index_0]
			local ClassName = API_Class.Name
			local ClassMembers = API_Class.Members

			for _index_1 = 1, #ClassMembers do
				local Member = ClassMembers[_index_1]
				local MemberName = Member.Name
				local MemberType = Member.MemberType

				local Security = Member.Security
				if type(Security) == "string" then
					if Security == "None" then
						continue
					end
					List[Capabilities[Security]][MemberType][ClassName][MemberName] = Security
				else
					local Read, Write = Security.Read, Security.Write

					if Read == Write then
						if Read == "None" then
							continue
						end
						List[Capabilities[Read]][MemberType][ClassName][MemberName] = Read
					else
						warn("Read != Write", ClassName, MemberName)
						local Read_Status, Write_Status = Capabilities[Read], Capabilities[Write]
						if Read_Status == Write_Status then
							List[Read_Status][MemberType][ClassName][MemberName] = { Read = Read, Write = Write }
						else
							List[Read_Status][MemberType][ClassName][MemberName] = "Read"
							List[Write_Status][MemberType][ClassName][MemberName] = "Write"
							warn(`Only {Read_Status and "Read" or "Write"}`, ClassName, MemberName)
						end
					end
				end
			end
		end
	end

	local ok, result = pcall(FetchAPI)

	if ok then
		local Script = Instance.new("Script")

		Script.Source = service.HttpService:JSONEncode(List)

		Script.Parent = workspace
	else
		warn(result)
	end
end
