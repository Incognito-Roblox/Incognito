from rbx.base import Process, RBXString

class BoundFuncDescriptor:
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

class BoundFuncDescriptorContainer:
    def __init__(self, Address):
        self.Address = Address

    def GetAllYield(self):
        top = Process.read_longlong(self.Address + 0x178)
        end = Process.read_longlong(self.Address + 0x180)

        for address in range(top, end, 0x8):
            Descriptor = BoundFuncDescriptor(
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
            
        return BoundFuncDescriptor(0)

    def GetAll(self):
        return self.GetAllList()