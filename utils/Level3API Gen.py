import json
import requests
import os

colors = {
    "grey": 90,
    "dark red": 91,
    "dark green": 92,
    "orange": 93,
    "dark blue": 94,
    "pink": 95,
    "aqua": 96,
    "grey": 97,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "purple": 35,
    "bright white": 37,
    "error": 41,
    "cyan": 36,
    "magenta": 35,
    "bright red": 91,
    "bright yellow": 93,
    "bright magenta": 95,
    "white": 97,
}


def print_in_color(text, color_name):
    if color_name is None:
        print(text)
        return

    color_code = colors.get(color_name)
    if color_code is not None:
        colored_text = f"\033[{color_code}m{text}\033[0m"
        print(colored_text)
    else:
        print("Color not found in the list.")


class AutocreateList:
    def __init__(self):
        self.__dict__ = {}

    def __getitem__(self, index):
        if index not in self.__dict__:
            self.__dict__[index] = AutocreateList()
        return self.__dict__[index]

    def __setitem__(self, index, value):
        self.__dict__[index] = value


class List:
    def __init__(self):

        self.Accessible = AutocreateList()
        self.Inaccessible = AutocreateList()

    def __getitem__(self, Accessible):
        return self.Accessible if Accessible else self.Inaccessible


LVL_3_API = List()


Capabilities = {
    "None": True,
    "PluginSecurity": True,
    "LocalUserSecurity": True,
    "RobloxScriptSecurity": True,
}


def FetchAPI():
    API_Dump_Url = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/Mini-API-Dump.json"
    API_Dump = requests.get(API_Dump_Url).json()
    API_Classes = API_Dump["Classes"]
    print()
    for API_Class in API_Classes:
        ClassName = API_Class["Name"]
        ClassMembers = API_Class["Members"]
        Unique = False
        for Member in ClassMembers:
            MemberName = Member["Name"]
            MemberType = Member["MemberType"]

            Security = Member["Security"]
            if isinstance(Security, str):
                if Security == "None":
                    continue
                LVL_3_API[Capabilities.get(Security)][MemberType][ClassName][
                    MemberName
                ] = Security
            else:
                Read, Write = Security.get("Read", "None"), Security.get(
                    "Write", "None"
                )

                if Read == Write:
                    if Read == "None":
                        continue
                    LVL_3_API[Capabilities.get(Read)][MemberType][ClassName][
                        MemberName
                    ] = Read
                else:
                    Unique = True
                    Read_Status, Write_Status = Capabilities.get(
                        Read
                    ), Capabilities.get(Write)
                    if Read_Status == Write_Status:
                        print_in_color(
                            f"Read != Write : {ClassName}.{MemberName}", "yellow"
                        )
                        LVL_3_API[Read_Status][MemberType][ClassName][MemberName] = {
                            "Read": Read,
                            "Write": Write,
                        }
                    else:
                        LVL_3_API[Read_Status][MemberType][ClassName][
                            MemberName
                        ] = "Read"
                        LVL_3_API[Write_Status][MemberType][ClassName][
                            MemberName
                        ] = "Write"
                        print_in_color(
                            f"Only {Read_Status and 'Read ' or 'Write'}    : {ClassName}.{MemberName}",
                            "red",
                        )
        if Unique:
            print()


FetchAPI()


class AutocreateListEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, AutocreateList):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


sorted_list = {
    k: dict(sorted(v.__dict__.items())) for k, v in sorted(LVL_3_API.__dict__.items())
}


script_dir = os.path.dirname(os.path.realpath(__file__))
output_file_path = os.path.join(script_dir, "Level3API.json")

with open(output_file_path, "w") as f:
    json.dump(sorted_list, f, indent=4, sort_keys=True, cls=AutocreateListEncoder)
