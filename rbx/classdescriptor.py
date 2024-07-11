from rbx.base import Process, RBXString
from rbx.propertydescriptor import PropertyDescriptorContainer
from rbx.boundfuncdescriptor import BoundFuncDescriptorContainer

class ClassDescriptor:
    def __init__(self, Address: int):
        self.Address = Address

    @property
    def Name(self):
        name_pointer = Process.read_longlong(
            self.Address + 0x8
        )

        return RBXString(name_pointer)
    
    @property
    def Capabilities(self):
        return Process.read_long(
            self.Address + 0x370
        )

    @property
    def PropertyDescriptors(self):
        return PropertyDescriptorContainer(
            self.Address
        )
    
    @property
    def BoundFuncDescriptors(self):
        return BoundFuncDescriptorContainer(
            self.Address
        )