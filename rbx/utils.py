import os, re

RBXPath = os.getenv("LOCALAPPDATA") + "\\Roblox\\logs"
RENDER_VIEW_PATTERN = r"\[FLog::SurfaceController\] SurfaceController\[_:\d\]::initialize view\([A-F0-9]{16}\)"

# haha noob no updated offsets for u
class Offsets:
    DataModelHolder = 0x118
    DataModel = 0x198

    Name = 0x48
    Children = 0x50
    Parent = 0x60
    ClassDescriptor = 0x18

    ValueBase = 0xC0

    ModuleFlags = 0x1B4

    BytecodeSize = 0xA8
    Bytecode = {
        "LocalScript": 0x1C8,
        "ModuleScript": 0x168
    }

Capabilities = {
    0x0: "None",
    0x1: "Plugin",
    0x2: "LocalUser",
    0x4: "WritePlayer",
    0x8: "RobloxScriptSecurity",
    0x10: "RobloxEngine",
    0x20: "NotAccessible"
}

def GetLog():
    file_name = ""
    for dir in os.listdir(RBXPath):
        if dir.find("_Player_") > -1:
            file_name = dir

    return open(RBXPath + "\\" + file_name, "r", encoding="utf-8")

def GetRenderView():
    log_file = GetLog()
    if log_file:
        render_views = re.findall(RENDER_VIEW_PATTERN, log_file.read())
        log_file.close()

        if len(render_views) > 0:
            matched_str = render_views[-1]
            render_view_addy = re.search(r"[A-F0-9]{16}", matched_str)
            if not render_view_addy:
                return None

            return int(render_view_addy.group(0), 16)

        return None
