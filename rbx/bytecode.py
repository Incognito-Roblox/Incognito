import os, ctypes

dll = ctypes.CDLL("./bin/incognito-luau.dll")

RBXCompile_t = dll.RBXCompile
RBXCompile_t.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

RBXDecompress_t = dll.RBXDecompress
RBXDecompress_t.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

class Bytecode:
    def Compile(source: str, path="compressed.btc"):
        RBXCompile_t(
            path.encode(errors="ignore"), 
            source.encode(errors="ignore")
        )

        try:
            with open(path, "rb") as file:
                file = open(path, "rb")
                bytecode = file.read().split(b" size: ")
                file.close()

        except:
            pass

        os.remove(path)

        return [bytecode[0], int(bytecode[1])]

    def Decompress(source: bytes, path="decompressed.btc"):
        RBXDecompress_t(
            path.encode(errors="ignore"), 
            source
        )

        try:
            with open(path, "rb") as file:
                file = open(path, "rb")
                bytecode = file.read().split(b" size: ")
                file.close()

        except:
            pass

        os.remove(path)

        if len(bytecode) > 1:
            return [bytecode[0], int(bytecode[1])]
        else:
            return [None, -1]