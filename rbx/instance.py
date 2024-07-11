from rbx.base import Window, Process, RBXString
from rbx.classdescriptor import ClassDescriptor
from rbx.utils import Offsets, GetRenderView
from rbx.bytecode import Bytecode as RBXBytecode

import time

BytecodeCaches: dict[int, any] = {}

class Instance:
    def __init__(self, Address: int):
        self.Address = Address

    @property
    def ClassDescriptor(self):
        if self.Address < 1000:
            return None

        return ClassDescriptor(
            Process.read_longlong(
                self.Address + Offsets.ClassDescriptor
            )
        )

    @property
    def ClassName(self):
        if self.Address < 1000:
            return "None"

        return self.ClassDescriptor.Name

    @property
    def Name(self):
        if self.Address < 1000:
            return "None"

        name_pointer = Process.read_longlong(
            self.Address + Offsets.Name
        )

        return RBXString(name_pointer)

    @property
    def Parent(self):
        if self.Address < 1000:
            return Instance(0)

        return Instance(
            Process.read_longlong(
                self.Address + Offsets.Parent
            )
        )

    @property
    def LocalPlayer(self):
        if self.Address < 1000:
            return Instance(0)

        if self.ClassName == "Players":
            return self.FindFirstChildOfClass("Player")

        return Instance(0)

    @property
    def Bytecode(self):
        if self.Address < 1000:
            return "None"

        if self.ClassName in Offsets.Bytecode:
            bytecode_pointer = Process.read_longlong(
                self.Address +
                Offsets.Bytecode[self.ClassName]
            )

            bytecode_pointer_str = Process.read_longlong(bytecode_pointer + 0x10)
            bytecode_size = Process.read_long(bytecode_pointer + 0x20)

            compressed_bytecode = Process.read_bytes(
                bytecode_pointer_str,
                bytecode_size
            )
            raw_bytecode = RBXBytecode.Decompress(compressed_bytecode)

            return raw_bytecode[0]

    @property
    def Value(self):
        if self.Address < 1000:
            return None

        if self.ClassName == "BoolValue":
            return Process.read_byte(self.Address + Offsets.ValueBase) == 1

        elif self.ClassName == "NumberValue":
            return Process.read_double(self.Address + Offsets.ValueBase)

        elif self.ClassName == "ObjectValue":
            return Instance(Process.read_longlong(self.Address + (Offsets.ValueBase - 0x8)))

        elif self.ClassName == "StringValue":
            string_pointer = self.Address + Offsets.ValueBase
            string_length = Process.read_long(string_pointer + 0x10)

            if string_length > 15:
                string_pointer = Process.read_longlong(string_pointer)

            return Process.read_string(string_pointer, string_length)

    def Spoof(self, other: int):
        spoofed_addy = (other.Address if isinstance(other, Instance) else other)
        Process.write_longlong(self.Address + 0x8, spoofed_addy)

    def GetChildren(self, do_yield=False, range_limit=-1):
        if self.Address < 1000:
            return []

        new_childlist = []

        children_pointer = Process.read_longlong(self.Address + Offsets.Children)

        top = Process.read_longlong(children_pointer)
        end = Process.read_longlong(children_pointer + 0x8) + 1

        for child_addy in range(top, end, 0x10):
            current_index = child_addy // end

            if range_limit > 0 and current_index > range_limit:
                break

            child_ptr = Process.read_longlong(child_addy)
            if child_ptr < 1000:
                continue

            child = Instance(child_ptr)
            if child.Address > 1000:
                if do_yield:
                    yield child

                new_childlist.append(child)

        return new_childlist

    def GetChildrenCount(self, range_limit=-1) -> int:
        if self.Address < 1000:
            return -1

        children_count = 0
        children_pointer = Process.read_longlong(self.Address + Offsets.Children)

        top = Process.read_longlong(children_pointer)
        end = Process.read_longlong(children_pointer + 0x8) + 1

        for child_addy in range(top, end, 0x10):
            current_index = child_addy // end

            if range_limit > 0 and current_index > range_limit:
                break

            child_ptr = Process.read_longlong(child_addy)
            if child_ptr < 1000:
                continue

            child = Instance(child_ptr)
            if child.Address > 1000:
                children_count += 1

        return children_count

    def FindFirstChild(self, name: str, recursive=False, range_limit=-1):
        if self.Address < 1000:
            return Instance(0)

        children_pointer = Process.read_longlong(self.Address + Offsets.Children)

        top = Process.read_longlong(children_pointer)
        end = Process.read_longlong(children_pointer + 0x8) + 1

        for child_addy in range(top, end, 0x10):
            current_index = child_addy // end

            if range_limit > 0 and current_index > range_limit:
                break

            child_ptr = Process.read_longlong(child_addy)
            if child_ptr < 1000:
                continue

            child = Instance(child_ptr)
            if child.Name == name:
                return child

            if recursive:
                descendant_child = child.FindFirstChild(name, True)

                if descendant_child.Address > 1000:
                    return descendant_child

        return Instance(0)

    def FindFirstChildOfClass(self, class_name: str, recursive=False, range_limit=-1):
        if self.Address < 1000:
            return Instance(0)

        children_pointer = Process.read_longlong(self.Address + Offsets.Children)

        top = Process.read_longlong(children_pointer)
        end = Process.read_longlong(children_pointer + 0x8) + 1

        for child_addy in range(top, end, 0x10):
            current_index = child_addy // end

            if range_limit > 0 and current_index > range_limit:
                break

            child_ptr = Process.read_longlong(child_addy)
            if child_ptr < 1000:
                continue

            child = Instance(child_ptr)
            if child.ClassName == class_name:
                return child

            if recursive:
                descendant_child = child.FindFirstChildOfClass(class_name, True)

                if descendant_child.Address > 1000:
                    return descendant_child

        return Instance(0)

    def WaitForChild(self, name: str, timeout: int | bool):
        found_child = Instance(0)

        while ((isinstance(timeout, bool) and not timeout) and found_child.Address < 1000) or timeout > 1:
            found_child = self.FindFirstChild(name)

            if found_child.Address > 1000:
                return found_child

            time.sleep(1)

            if type(timeout) == int:
                timeout -= 1

        return found_child

    def SetModuleBypass(self):
        Process.write_longlong(
            self.Address + Offsets.ModuleFlags,
            0x100000000
        )

    def ResetModule(self, old_bytecode=None):
        old_bytecode = (BytecodeCaches[self.Address] if self.Address in BytecodeCaches else old_bytecode)

        if self.ClassName == "ModuleScript" and old_bytecode:
            """Process.write_longlong(self.Address + Offsets.ModuleFlags, 0)
            Process.write_longlong(self.Address + Offsets.Bytecode["ModuleScript"], old_bytecode[0])

            Process.free_memory(old_bytecode[1], Offsets.BytecodeSize)
            Process.free_memory(old_bytecode[2], old_bytecode[3])"""

            Process.free_memory(old_bytecode[3], old_bytecode[2])

            Process.write_longlong(old_bytecode[0] + 0x10, old_bytecode[1])
            Process.write_longlong(old_bytecode[0] + 0x20, old_bytecode[2])

            if (old_bytecode == BytecodeCaches[self.Address]):
                del BytecodeCaches[self.Address]

    def __setattr__(self, name: str, value) -> None:
        if (name != "Address" and self.Address < 1000):
            return Exception(f"Cannot set property on this Instance object")

        if name == "Bytecode" and (
            type(value) == list and len(value) == 2
            ) and (self.ClassName in Offsets.Bytecode):
            """new_bytecode_ptr = Process.allocate_memory(Offsets.BytecodeSize)
            protected_str_ptr = Process.allocate_memory(value[1])

            old_bytecode_ptr = Process.read_longlong(self.Address + Offsets.Bytecode["ModuleScript"])
            old_bytecode_bytes = Process.read_bytes(old_bytecode_ptr, Offsets.BytecodeSize)

            if not self.Address in BytecodeCaches:
                BytecodeCaches[self.Address] = [
                    old_bytecode_ptr,
                    new_bytecode_ptr,
                    protected_str_ptr,
                    value[1]
                ]

            Process.write_bytes(new_bytecode_ptr, old_bytecode_bytes)
            Process.write_bytes(protected_str_ptr, value[0])

            Process.write_longlong(new_bytecode_ptr + 0x10, protected_str_ptr)
            Process.write_long(new_bytecode_ptr + 0x20, value[1])

            Process.write_longlong(self.Address + Offsets.Bytecode["ModuleScript"], new_bytecode_ptr)"""

            old_bytecode_ptr = Process.read_longlong(self.Address + Offsets.Bytecode["ModuleScript"])

            old_protected_str = Process.read_long(old_bytecode_ptr + 0x10)
            old_bytecode_size = Process.read_long(old_bytecode_ptr + 0x20)

            protected_str_ptr = Process.allocate_memory(value[1])

            if not self.Address in BytecodeCaches:
                BytecodeCaches[self.Address] = [
                    old_bytecode_ptr,
                    old_protected_str,
                    old_bytecode_size,
                    protected_str_ptr
                ]

            Process.write_bytes(protected_str_ptr, value[0])

            Process.write_longlong(old_bytecode_ptr + 0x10, protected_str_ptr)
            Process.write_long(old_bytecode_ptr + 0x20, value[1])

        elif name == "Bytecode" and type(value) == int and (self.ClassName in Offsets.Bytecode):
            Process.write_longlong(
                self.Address + Offsets.Bytecode[self.ClassName],
                value
            )

        elif name == "Value" and self.ClassName.endswith("Value"):
            if self.ClassName == "BoolValue":
                Process.write_byte(
                    self.Address + Offsets.ValueBase,
                    int(value)
                )

            elif self.ClassName == "NumberValue":
                Process.write_double(
                    self.Address + Offsets.ValueBase,
                    value
                )

            elif self.ClassName == "ObjectValue":
                Process.write_longlong(
                    self.Address + (Offsets.ValueBase - 0x8),
                    (value.Address if type(value) == Instance else 0)
                )

            elif self.ClassName == "StringValue":
                string_addy = self.Address + Offsets.ValueBase
                string_length = Process.read_long(string_addy + 0x10)
                redirected_ptr: int = None

                if string_length > 15:
                    redirected_ptr = Process.read_longlong(string_addy)

                Process.write_string((redirected_ptr or string_addy), value)
                Process.write_long(string_addy + 0x10, len(value) + 1)

        elif name == "Parent" and type(value) == Instance:
            Process.write_longlong(
                self.Address + Offsets.Parent,
                (value.Address if value else 0)
            )

        else:
            self.__dict__[name] = value

    def __repr__(self):
        return f"({self.Name} as {self.ClassName} | {hex(self.Address)})"

def FetchRenderView(process_id: int) -> int:
    Process.update_pid(process_id)
    RenderViewAddy = None

    try:
        RenderViewAddy = GetRenderView()

        if not RenderViewAddy:
            # TODO: find aob for RenderViewAddy
            pass

    except Exception as bruhmoment:
        print("Failed to fetch RenderView, info:", bruhmoment)

    return RenderViewAddy
