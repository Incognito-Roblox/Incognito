from rbx.base import Process, RBXString

OldAccessibleFlags = {}

class PropertyDescriptor:
    def __init__(self, Address):
        self.Address = Address

    @property
    def Name(self):
        return RBXString(
            Process.read_longlong(self.Address + 0x8)
        )
    
    @property
    def Capabilities(self):
        return Process.read_long(self.Address + 0x38)

    @property
    def AccessibleFlags(self):
        return Process.read_long(self.Address + 0x40)

    def SetScriptable(self, scriptable):
        hex_address = hex(self.Address)
        if scriptable:
            if not hex_address in OldAccessibleFlags:
                OldAccessibleFlags[hex_address] = self.AccessibleFlags
                Process.write_long(self.Address + 0x40, 63)
        else:
            if self.OldAccessibleFlags:
                Process.write_long(self.Address + 0x40, OldAccessibleFlags[hex_address])

class PropertyDescriptorContainer:
    def __init__(self, Address):
        self.Address = Address

    def GetAllYield(self):
        top = Process.read_longlong(self.Address + 0x28)
        end = Process.read_longlong(self.Address + 0x30)

        for address in range(top, end, 0x8):
            Descriptor = PropertyDescriptor(
                Process.read_longlong(address)
            )

            if Descriptor.Address > 1000:
                yield Descriptor

    def GetAllList(self):
        descriptors = []

        for Descriptor in self.GetAllYield():
            descriptors.append(Descriptor)

        return descriptors

    def Get(self, Name):
        for Descriptor in self.GetAllYield():
            if Descriptor.Name == Name:
                return Descriptor
            
        return PropertyDescriptor(0)

    def GetAll(self):
        return self.GetAllList()
