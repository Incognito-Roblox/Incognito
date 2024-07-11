--[[
    filesystem-wrapper.lua
    @jLn0n | 2024

    You think, why do we need to do this wrapping?
    Because our filesystem implementation yields because of bridge
    and this implementation removes yielding while being able to be real.
    By default, filesystem functions doesn't yield so we try to be like that.
--]]

local bridge = load_module("bridge")

-- variables
local BLACKLISTED_EXTENSIONS = {
    ".exe", ".bat",  ".com", ".cmd",  ".inf", ".ipa",
    ".apk", ".apkm", ".osx", ".pif",  ".run", ".wsh",
    ".bin", ".app",  ".vb",  ".vbs",  ".scr", ".fap",
    ".cpl", ".inf1", ".ins", ".inx",  ".isu", ".job",
    ".lnk", ".msi",  ".ps1", ".reg",  ".vbe", ".js",
    ".x86", ".pif",  ".xlm", ".scpt", ".out", ".ba_",
    ".jar", ".ahk",  ".xbe", ".0xe",  ".u3p", ".bms",
    ".jse", ".cpl",  ".ex",  ".osx",  ".rar", ".zip",
    ".7z",  ".py",   ".cpp", ".cs",   ".prx", ".tar",
    ".",    ".wim",  ".htm", ".html", ".css",
    ".appimage", ".applescript", ".x86_64", ".x64_64",
    ".autorun", ".tmp", ".sys", ".dat", ".ini", ".pol",
    ".vbscript", ".gadget", ".workflow", ".script",
    ".action", ".command", ".arscript", ".psc1",
}
local FILESYSTEM_LOADED = false

local filesys_storage = {}
local script_env

-- functions
local function sanitize_path(dir_path: string)
    if #dir_path < 1 then
        return
    end

    dir_path = string.gsub(
        dir_path,
        "[\0\1\2\3\4\5\6\7\8\11\12\13\14\15\16\17\18\19\20\21\22\23\24\25\26\27\28\29\30\31]+[:*?\"<>|]+",
        ""
    )
    return dir_path
end

local function sanitize_file_name(file_name: string): string?
    local _sanitized_name = sanitize_path(file_name) :: string
    if file_name ~= _sanitized_name then
        return error(`Blacklisted character in file name '{file_name}'`, 0)
    end

    local extention_splits = string.split(file_name, ".")
    local file_extension = extention_splits[#extention_splits]

    if table.find(BLACKLISTED_EXTENSIONS, `.{file_extension}`) then
        return error(`Blacklisted extension in file name '{file_name}'`, 0)
    end
    return file_name
end

local function parse_file_path(dir_path: string, no_sanity: boolean): { string }
    if not no_sanity then
        local _sanitized_path = sanitize_path(dir_path)
        if dir_path ~= _sanitized_path then
            return error(`Blacklisted character in path '{dir_path}'`, 0)
        end
    end

    local result = {}

    for path_name in string.gmatch(dir_path, "([^\\/]+)") do
        table.insert(result, path_name)
    end
    return result
end

local function get_dir_content(dir_data, path_list)
    local current_file = dir_data

    if type(current_file) == "table" and #path_list > 0 then
        for _, current_path in path_list do
            current_path = sanitize_file_name(current_path)

            local selected_file
            for path_name, path_content in current_file do
                if not (path_name == current_path or string.lower(path_name) == current_path) then continue end
                selected_file = path_content
            end

            if not selected_file then return end
            current_file = selected_file
        end
    end
    return current_file
end

local function get_dir_parent(dir_data, path_list)
    local folder_path = table.clone(path_list)
    table.remove(folder_path, #folder_path)

    -- checks folder existance
    local folder_dir = get_dir_content(dir_data, folder_path)
    if not (folder_dir and type(folder_dir) == "table") then
        return error(`Path '{table.concat(path_list, "/")}' parent {if not folder_dir then "doesn't exist" else "not a folder"}`, 0)
    end

    return folder_dir
end

local function fetch_paths_list(parent_path, dir_data, result)
    for file_name, value in dir_data do
        if not value then
            continue
        end
        local path_result = `{parent_path}/{file_name}`

        table.insert(result, path_result)
        if type(value) == "table" then
            fetch_paths_list(path_result, value, result)
        end
    end
end

local function get_all_file_paths(dir_data, path: string): { string }
    path = path or ""
    local result = {}

    fetch_paths_list(path, dir_data, result)
    return result
end

local function synchronize_to_external(path: string)
    local path_list = parse_file_path(path, true)
    local dir_parent = get_dir_parent(filesys_storage, path_list)
    local dir_name = sanitize_file_name(path_list[#path_list])

    local content_type = type(dir_parent[dir_name])

    if content_type == "string" then
        bridge:send("write_file", path, dir_parent[dir_name])
    elseif content_type == "table" then
        bridge:send("make_folder", path)
    elseif content_type == "nil" then
        bridge:send("delete_dir", path)
    end
end

-- main
local filesystem = {}

filesystem.readfile = function(dir_path: string): string?
    assert(type(dir_path) == "string", "arg #1 must be type string")

    local path_list = parse_file_path(dir_path)
    local file_content = get_dir_content(filesys_storage, path_list)

    local file_content_type = type(file_content)
    if file_content_type ~= "string" then
        return error(`Path '{dir_path}' {if file_content_type == "table" then "is a folder" else "cannot be determined"}`, 0)
    end

    return file_content
end

filesystem.writefile = function(dir_path: string, content: string)
    assert(type(dir_path) == "string", "arg #1 must be type string")
    assert(type(content) == "string", "arg #2 must be type string")

    local path_list = parse_file_path(dir_path)
    local file_parent = get_dir_parent(filesys_storage, path_list)

    local file_name = sanitize_file_name(path_list[#path_list])

    file_parent[file_name] = content
    task.spawn(synchronize_to_external, dir_path)
end

filesystem.appendfile = function(dir_path: string, content: string)
    assert(type(dir_path) == "string", "arg #1 must be type string")
    assert(type(content) == "string", "arg #2 must be type string")

    local path_list = parse_file_path(dir_path)
    local file_parent = get_dir_parent(filesys_storage, path_list)

    local file_name = sanitize_file_name(path_list[#path_list])

    file_parent[file_name] ..= content
    task.spawn(synchronize_to_external, dir_path)
end

filesystem.loadfile = function(dir_path: string): ()
    return script_env.loadstring(script_env.readfile(dir_path), dir_path)
end

filesystem.deletepath = function(dir_path: string)
    assert(type(dir_path) == "string", "arg #1 must be type string")

    local path_list = parse_file_path(dir_path)
    local file_parent = get_dir_parent(filesys_storage, path_list)

    local file_name = sanitize_file_name(path_list[#path_list])

    file_parent[file_name] = nil
    task.spawn(synchronize_to_external, dir_path)
end

filesystem.makefolder = function(dir_path: string)
    assert(type(dir_path) == "string", "arg #1 must be type string")

    local path_list = parse_file_path(dir_path)
    local dir_parent = get_dir_parent(filesys_storage, path_list)
    local dir_name = sanitize_file_name(path_list[#path_list])

    dir_parent[dir_name] = {}
    task.spawn(synchronize_to_external, dir_path)
end

filesystem.isfile = function(dir_path: string)
    assert(type(dir_path) == "string", "arg #1 must be type string")

    local path_list = parse_file_path(dir_path)
    local success, file_parent = pcall(get_dir_parent, filesys_storage, path_list)

    if success then
        local file_name = path_list[#path_list]

        return type(file_parent[file_name]) == "string"
    end
    return false
end

filesystem.isfolder = function(dir_path: string)
    assert(type(dir_path) == "string", "arg #1 must be type string")

    local path_list = parse_file_path(dir_path)
    local success, file_parent = pcall(get_dir_parent, filesys_storage, path_list)

    if success then
        local file_name = path_list[#path_list]

        return type(file_parent[file_name]) == "table"
    end
    return false
end

filesystem.listfiles = function(dir_path: string)
    assert(type(dir_path) == "string", "arg #1 must be type string")

    local path_list = parse_file_path(dir_path)
    local folder_dir = get_dir_content(filesys_storage, path_list)
    if type(folder_dir) ~= "table" then
        return error(`Path '{dir_path}' doesn't resolve to a folder`, 0)
    end

    return get_all_file_paths(folder_dir, dir_path)
end

filesystem.fs_loaded = function()
    return FILESYSTEM_LOADED
end

-- synchronizer
-- TODO: probably do external -> roblox file sync repeatedly
bridge:register_callback("synchronize_files", function()
    bridge:register_callback("synchronize_files", nil)
    local got_list, dir_list = bridge:send("list_files", "\\")

    if not got_list then
        return warn("Failed to load directory of workspace")
    end

    for _, path in dir_list do
        local success, path_type = bridge:send("get_path_type", path)
        if not success then
            continue
        end

        local path_list = parse_file_path(path, true)
        local path_parent = get_dir_parent(filesys_storage, path_list)
        local current_dir = path_list[#path_list]

        if path_type == "file" then
            local read_success, file_content = bridge:send("read_file", path)
            if not read_success then
                continue
            end

            path_parent[current_dir] = file_content
        elseif path_type == "folder" then
            path_parent[current_dir] = {}
        end
    end
    FILESYSTEM_LOADED = true
end)

return function(_script_env)
    script_env = _script_env

    return filesystem, {
        ["deletepath"] = { "delfile", "delfolder" },
        ["loadfile"] = { "dofile" },
    }
end
