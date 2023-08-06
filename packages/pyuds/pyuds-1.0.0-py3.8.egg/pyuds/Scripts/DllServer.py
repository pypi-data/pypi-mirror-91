#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 19:00:37 2021

@author: levy.he
@file  : DllServer.py
"""
import ctypes
import platform

KEY_ARRAY_SIZE = 64
c_byte_a = ctypes.c_char_p
c_size = ctypes.c_uint32
c_level = ctypes.c_uint32
c_buf = ctypes.c_char * KEY_ARRAY_SIZE
rtn_status = ctypes.c_int


from msl.loadlib import Server32, Client64

class DllServer(Server32):
    
    def __init__(self, libtype, host, port, quiet, seed_levels=[], dll_path=None):
        self.dll_path = dll_path
        if dll_path is not None:
            super(DllServer, self).__init__(dll_path, 'cdll', '127.0.0.1', '9527', True)
            self.seed_levels = seed_levels
            try:
                self.GenerateKeyEx = self.lib.GenerateKeyEx
                self.GenerateKeyEx.argtypes = [c_byte_a, c_size, c_level, c_byte_a, c_byte_a, c_size, ctypes.POINTER(c_size)]
                self.dll_type = 'Basic'
            except:
                self.GenerateKeyEx = self.lib.GenerateKeyExOpt
                self.GenerateKeyEx.argtypes = [c_byte_a, c_size, c_level, c_byte_a, c_byte_a, c_byte_a, c_size, ctypes.POINTER(c_size)]
                self.dll_type = 'Opt'

            self.GenerateKeyEx.restype = rtn_status
        else:
            self.seed_levels = []

    def KenGen(self, level, seed):
        if self.dll_path is None:
            return None
        key = c_buf()
        _seed = c_buf(*seed)
        key_out_size = c_size(0)
        varint = ''
        if self.dll_type == 'Opt':
            rtn = self.GenerateKeyEx(_seed, len(seed), level, varint.encode(
                'ascii'), varint.encode('ascii'), key, KEY_ARRAY_SIZE, ctypes.byref(key_out_size))
        else:
            rtn = self.GenerateKeyEx(_seed, len(seed), level, varint.encode(
                'ascii'), key, KEY_ARRAY_SIZE, ctypes.byref(key_out_size))
        if rtn == 0:
            key = key[0:key_out_size.value]
            return list(key)
        else:
            return None


