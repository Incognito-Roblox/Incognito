# from: https://github.com/LorekeeperZinnia/Dex/blob/master/build.py
import os, argparse, base64, re

import misc.app_info as IncognitoApp
from rbx.bytecode import Bytecode

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--debug", dest="debug_mode", action="store_true")

main_dir = os.path.dirname(os.path.abspath(__file__))
init_script_path = os.path.join(main_dir, "init_script")
modules_path = os.path.join(init_script_path, "modules")
modules_list = os.listdir(modules_path)

def read_file(path):
    file = open(path, "r")
    str = file.read()
    file.close()
    return str

def embed_module_file(path) -> str:
    module_name = os.path.splitext(os.path.basename(path))[0]
    module_src = read_file(path)

    return '["' + module_name + '"] = function(load_module)\n' + module_src + '\nend,\n'

def init_build() -> str:
    script_content = "local embedded_modules = {\n"

    for sub_module_name in modules_list:
        full_dir = f"{modules_path}/{sub_module_name}"

        if os.path.isfile(full_dir):
            script_content += embed_module_file(full_dir)

        elif os.path.isdir(full_dir):
            module_group_name = os.path.splitext(os.path.basename(sub_module_name))[0]
            sub_module_list = os.listdir(full_dir)
            script_content += f"[\"{module_group_name}\"] = " + "{\n"

            for sub_module_name in sub_module_list:
                script_content += embed_module_file(f"{full_dir}/{sub_module_name}")

            script_content += "},\n"

    script_content += "}"
    script_content += "\n\n" + read_file(init_script_path + "/loader.lua")

    script_content = re.sub(
        pattern=r"\${VERSION_AUTOMATIC}",
        repl=IncognitoApp.VERSION,
        string=script_content,
        count=1,
    )
    return script_content

built_script = init_build()
args = arg_parser.parse_args()

with open(os.path.join(main_dir, "misc", "init_script.py"), "w") as file:
    file_result = "content,debug_mode=r\"\"\""

    if args.debug_mode:
        file_result += built_script
    else:
        compiled_result = Bytecode.Compile(built_script)
        file_result += base64.b64encode(compiled_result[0]).decode(errors="ignore")

    file_result += f"\n\"\"\",{args.debug_mode}"
    file.write(file_result)
    file.close()
