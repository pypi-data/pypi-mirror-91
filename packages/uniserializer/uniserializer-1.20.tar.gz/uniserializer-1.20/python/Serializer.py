import sys, ctypes
class Serializer:
    def __init__(self, buffer):
        self.frombuffer(buffer)
    def __VerifyEntrySize(self, size):
        assert(type(size) == int)
        return len(self.buffer) < (self.position + size)
    def encode_8(self, value):
        assert(type(value) == int)
        assert(value < 0x100)

        val = value & 0xff
        if self.__VerifyEntrySize(1):
            self.buffer += bytes(range((self.position + 1)-len(self.buffer)))
        self.buffer[self.position] = val
        self.position += 1
    def encode_16(self, value):
        assert(type(value) == int)
        assert(value < 0x10000)

        val = [0,0]
        if sys.byteorder == "big":
            val[0] = value & 0xff
            val[1] = (value >> 8) & 0xff
        else:
            val[1] = value & 0xff
            val[0] = (value >> 8) & 0xff
        if self.__VerifyEntrySize(2):
            self.buffer += bytes(range((self.position + 2)-len(self.buffer)))
        self.buffer[self.position] = val[0]
        self.buffer[self.position + 1] = val[1]
        self.position += 2
    def encode_32(self, value):
        assert(type(value) == int)
        assert(value < 0x100000000)

        val = [0,0,0,0]
        if sys.byteorder == "big":
            val[0] = value & 0xff
            val[1] = (value >> 8) & 0xFF
            val[2] = (value >> 16) & 0xFF
            val[3] = (value >> 24) & 0xFF
        else:
            val[3] = value & 0xff
            val[2] = (value >> 8) & 0xFF
            val[1] = (value >> 16) & 0xFF
            val[0] = (value >> 24) & 0xFF
        if self.__VerifyEntrySize(4):
            self.buffer += bytes(range((self.position + 4)-len(self.buffer)))
        self.buffer[self.position] = val[0]
        self.buffer[self.position + 1] = val[1]
        self.buffer[self.position + 2] = val[2]
        self.buffer[self.position + 3] = val[3]
        self.position += 4
    def encode_64(self, value):
        assert(type(value) == int)
        assert(value < 0x10000000000000000)

        val = [0,0,0,0,0,0,0,0]
        if sys.byteorder == "big":
            val[0] = value & 0xff
            val[1] = (value >> 8) & 0xFF
            val[2] = (value >> 16) & 0xFF
            val[3] = (value >> 24) & 0xFF
            val[4] = (value >> 32) & 0xFF
            val[5] = (value >> 40) & 0xFF
            val[6] = (value >> 48) & 0xFF
            val[7] = (value >> 56) & 0xFF
        else:
            val[7] = value & 0xff
            val[6] = (value >> 8) & 0xFF
            val[5] = (value >> 16) & 0xFF
            val[4] = (value >> 24) & 0xFF
            val[3] = (value >> 32) & 0xFF
            val[2] = (value >> 40) & 0xFF
            val[1] = (value >> 48) & 0xFF
            val[0] = (value >> 56) & 0xFF
    
        if self.__VerifyEntrySize(8):
            self.buffer += bytes(range((self.position + 8)-len(self.buffer)))
        self.buffer[self.position] = val[0]
        self.buffer[self.position + 1] = val[1]
        self.buffer[self.position + 2] = val[2]
        self.buffer[self.position + 3] = val[3]
        self.buffer[self.position + 4] = val[4]
        self.buffer[self.position + 5] = val[5]
        self.buffer[self.position + 6] = val[6]
        self.buffer[self.position + 7] = val[7]
        self.position += 8
    def encode_String(self, value):
        assert(type(value) == str)
        
        length = len(value)+1
        val = list(map(ord, value))
        val.append(0)
        if self.__VerifyEntrySize(length):
            self.buffer += bytes(range((self.position + length)-len(self.buffer)))
        for i in range(length):
            self.buffer[self.position+i] = val[i]
        self.position += length
    def encode_Bytes(self, value):
        assert(type(value) == bytearray or type(value) == bytes)
        val = memoryview(value)
        length = len(val)
        if self.__VerifyEntrySize(length):
            self.buffer += bytes(range((self.position + length)-len(self.buffer)))
        for i in range(length):
            self.buffer[self.position+i] = val[i] & 0xff
        self.position += length
    def encode_Bool(self, value):
        assert(type(value) == bool)
        self.encode_8(int(bool(value)))
    def frombuffer(self, buffer):
        assert(type(buffer) == bytearray)
        self.buffer = bytearray(buffer)
        self.reset()
    def reset(self):
        self.position = 0
