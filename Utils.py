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




def len2d(lst):
    i = 0
    for j in lst:
        for k in j:
            i = i + 1
    return i

    
def lst2d2str(lst, arrayType = 'byte', arrayName = 'data', radix='hex', bits=8, pad=True, str2D = False, initArr = False):
    print(1.1)
    rc = RadixConversion()
    print(1.11)
    print(lst)
    lst2dLen = len2d(lst) 
    print(1.2)
    if arrayType == None:
        arrOpen = "["
        arrClose = "]"
        if initArr:
            arrayStr = arrayName
        else:
            arrayStr = arrOpen
    else:
        arrOpen = "{"
        arrClose = "}"
        if initArr:
            arrayStr = "{0} {1}".format(arrayType, arrayName)
        else:
            arrayStr = arrOpen
    print(1.3)
    if initArr:
        if pad:
            rowLen = 0
            for row in lst:
                temp = len(row)
                if temp > rowLen:
                    rowLen = temp
            if str2D:
                arrayStr = arrayStr + "{2}{0}{3}{4}{1}{5}".format(len(lst), rowLen, arrOpen, arrClose
                                                                  , arrOpen, arrClose)
            else:
                arrayStr = arrayStr + "{1}{0}{2}".format(lst2dLen, arrOpen, arrClose)
        else:
            arrayStr = arrayStr + "{1}{0}{2}".format(lst2dLen, arrOpen, arrClose)
        print(1.4)    
        arrayStr = arrayStr + " = {}".format(arrOpen)
    
    for i, line in enumerate(lst):
        print(1.5)
        for j, d in enumerate(line):
            print(1.6)
            if radix == 'hex':
                data = "0x" + str(d) 
            elif radix == 'bin':
                data = "0x" + rc.hex2bin(str(d), bits=8)
                
            if j == 0:
                if str2D:
                    arrayStr = arrayStr + "{0}{1}".format(arrOpen, data)
                elif i == 0:
                    arrayStr = arrayStr + "{}".format(data)
                else:
                    arrayStr = arrayStr + ", {}".format(data)
                    
            else:
                arrayStr = arrayStr + ", {}".format(data)
        print(1.7)
        if pad:
            j = rowLen - len(line)
            if j > 0:
                for i in range(j):
                    if radix == 'hex':
                        data = "0x" + "00" 
                    elif radix == 'bin':
                        data = "0x" + rc.hex2bin(str(0), bits=8)
                    arrayStr = arrayStr + ", {}".format(data)
        print(1.8)
        if str2D:
            if i < len(lst)-1:            
                arrayStr = arrayStr + "{}, ".format(arrClose)
            else:
                arrayStr = arrayStr + "{}".format(arrClose)
    arrayStr = arrayStr + "{};".format(arrClose)
    
    
    return arrayStr, lst2dLen
