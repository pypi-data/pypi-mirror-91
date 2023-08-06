from msl.loadlib import Server32, Client64
import ctypes
import platform

KEY_ARRAY_SIZE = 64
c_byte_a = ctypes.c_char_p
c_size = ctypes.c_uint32
c_level = ctypes.c_uint32
c_buf = ctypes.c_char * KEY_ARRAY_SIZE
rtn_status = ctypes.c_int



class DllClient(Client64):
    def __init__(self, *seed_levels, dll_path=None):
        self.dll_path = dll_path
        if dll_path is not None:
            self.seed_levels = seed_levels
            super(DllClient, self).__init__(module32='DllServer', seed_levels=seed_levels, dll_path=dll_path)
        else:
            self.seed_levels = []

    def KenGen(self, level, seed):
        return self.request32('KenGen', level, seed)
        

if __name__ == '__main__':
    key = DllClient([1, 3, 0x11], dll_path='GAC_A39_SRS.dll')
    print(key.KenGen())
