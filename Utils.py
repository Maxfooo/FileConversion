'''
Created on Jun 23, 2016

@author: maxr
'''

class RadixConversion():

    def __init__(self):
        pass

    def bin2dec(self,val):
        return int(str(val), 2)

    def bin2hex(self,val):
        dec = self.bin2dec(val)
        return self.dec2hex(dec)

    def dec2bin(self,val, bits=None):
        if bits == None:
            return "{0:b}".format(int(val))
        else:
            return "{0:b}".format(int(val)).zfill(bits)

    def dec2hex(self,val):
        return hex(int(val))

    def hex2bin(self, val, bits=None):
        dec = self.hex2dec(val)
        return self.dec2bin(dec, bits=bits)

    def hex2dec(self,val):
        return int(str(val), 16)
