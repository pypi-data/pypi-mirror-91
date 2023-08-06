#!/usr/bin/env python3
#coding:utf-8


from . import des_c
from . import utils

#---------------------------------------------------------------------
class DES:

    des_c_obj = None

    #-----------------------------------------------------------------
    def __init__(self, key_str):
        ""
        k = str_to_key56(key_str)
        k = key56_to_key64(k)
        key_str = utils.lst2str(k)
        self.des_c_obj = des_c.DES(key_str)

    #-----------------------------------------------------------------
    def encrypt(self, plain_text):
        ""
        return self.des_c_obj.encrypt(plain_text)

    #-----------------------------------------------------------------
    def decrypt(self, crypted_text):
        ""
        return self.des_c_obj.decrypt(crypted_text)

#---------------------------------------------------------------------
#Some Helpers
#---------------------------------------------------------------------

DESException = 'DESException'

#---------------------------------------------------------------------
def str_to_key56(key_str):
    ""
    if type(key_str) != type(''):
        #rise DESException, 'ERROR. Wrong key type.'
        pass
    if len(key_str) < 7:
        key_str = key_str + b'\000\000\000\000\000\000\000'[:(7 - len(key_str))]
    key_56 = b''
    for i in key_str[:7]:
        key_56 += bytes([i])

    return key_56

#---------------------------------------------------------------------
def key56_to_key64(key_56: bytes) -> bytes:
    ""
    key = []
    for i in range(8):
        key.append(bytes([0]))

    key[0] = key_56[0]
    key[1] = ((key_56[0] << 7) & 0xFF) | (key_56[1] >> 1)
    key[2] = ((key_56[1] << 6) & 0xFF) | (key_56[2] >> 2)
    key[3] = ((key_56[2] << 5) & 0xFF) | (key_56[3] >> 3)
    key[4] = ((key_56[3] << 4) & 0xFF) | (key_56[4] >> 4)
    key[5] = ((key_56[4] << 3) & 0xFF) | (key_56[5] >> 5)
    key[6] = ((key_56[5] << 2) & 0xFF) | (key_56[6] >> 6)
    key[7] =  (key_56[6] << 1) & 0xFF

    key_bytes = b''
    for b in key:
        key_bytes += bytes([b])

    key = set_key_odd_parity(key_bytes)

    return key

#---------------------------------------------------------------------
def set_key_odd_parity(key: bytes):
    ""

    tmp_key = []
    for i in range(len(key)):
        tmp_key.append(bytes([0]))

    for i in range(len(key)):
        for k in range(7):
            bit = 0
            t = key[i] >> k
            bit = (t ^ bit) & 0x1

        tmp_key[i] = (key[i] & 0xFE) | bit

    ret = b''
    for i in range(len(tmp_key)):
        ret += bytes([tmp_key[i]])

    return ret
