'''
Created on Jun 30, 2016

@author: maxr
'''

from FileIO import FileIO as FIO
from Utils import RadixConversion as RC
from ProgramBoronArduinoCode import arduinoCode as AC
import re

class ParseHexFile():
    
    def __init__(self, hexFile):
        self.hexFile = hexFile
        self.base = 16
        self.hexContent = None
        self.hexLen = []
        self.hexAddr = []
        self.hexAddrSep = []
        self.hexType = []
        self.hexData = []
        self.hexCS = []
        self.hexTypeEOF = '01'
        self.hexFileSettings()
        self.readHexFile()
        self.sortHexContents()
    
    def hexFileSettings(self, depth=16, width=8, address_radix='HEX', data_radix='HEX', fillZeros=0):
        self.depth = depth
        self.width = width
        self.address_radix = address_radix
        self.data_radix = data_radix
        self.data_digits = self.base / width
        self.fillZeros = fillZeros
    
    def readHexFile(self):
            try:
                if isinstance(self.hexFile, str):
                    self.hexContent = self.hexFile
                else:
                    self.hexContent = self.hexFile.read()
            except:
                pass

    def sortHexContents(self):
        hex_format_expression = r':(\w{2})(\w{4})(\w{2})(\w*)(\w{2})'
        self.hexFields = re.findall(hex_format_expression,self.hexContent)
        
        for records in self.hexFields:
            self.hexLen.append(records[0])
            self.hexAddr.append(records[1])
            self.hexAddrSep.append(re.findall(r'\w{%d}' %self.data_digits,records[1]))
            self.hexType.append(records[2])
            if self.hexType[-1] == self.hexTypeEOF:
                self.hexData.append(['00'])
            else:
                self.hexData.append(re.findall(r'\w{%d}' %self.data_digits,records[3]))
            self.hexCS.append(records[4])
            
    def structureHexContents(self, order=['dpl', 'dph', 'ndb', 'dat', 'csm'], includeEOF = False):
        orgFields = []
        i = len(self.hexFields)
        if not includeEOF:
            i = i - 1
        for j in range(i):
            line = []
            for record in order:
                if record == 'dpl':
                    line.append(self.hexAddrSep[j][1])
                elif record == 'dph':
                    line.append(self.hexAddrSep[j][0])
                elif record == 'ndb':
                    line.append(self.hexLen[j])
                elif record == 'dat':
                    for d in self.hexData[j]:
                        line.append(d)
                elif record == 'csm':
                    line.append(self.hexCS)
            orgFields.append(line)
        return orgFields
    
    def getHexLen(self):
        return self.hexLen
    
    def getHexAddr(self):
        return self.hexAddr
    
    def getHexAddrSep(self):
        return self.hexAddrSep
    
    def getHexType(self):
        return self.hexType
    
    def getHexData(self):
        return self.hexData
    
    def getHexCS(self):
        return self.hexCS



def hexToDataArray():
    fio = FIO()
    rc = RC()
    fio.openFileRead('.hex')
    hfile = fio.getReadFile()
    phf = ParseHexFile(hfile)
    format = ['dpl', 'dph', 'ndb', 'dat']
    mylst = phf.structureHexContents(format)
    arrayStr, arrLen = lst2d2str(mylst, pad=False)
    print(AC(arrLen, arrayStr, str(format) + " (repeated for however many hex lines where made)"))
    

def len2d(lst):
    i = 0
    for j in lst:
        for k in j:
            i = i + 1
    return i


def lst2d2str(lst, arrayType = 'byte', arrayName = 'data', radix='hex', bits=8, pad=True, str2D = False):
    rc = RC()
    
    if arrayType == None:
        arrayStr = arrayName
        arrOpen = "["
        arrClose = "]"
    else:
        arrayStr = "{0} {1}".format(arrayType, arrayName)
        arrOpen = "{"
        arrClose = "}"
    
    if pad:
        rowLen = 0
        for row in lst:
            temp = len(row)
            if temp > rowLen:
                rowLen = temp
        if str2D:
            arrayStr = arrayStr + "[{0}][{1}]".format(len(lst), rowLen)
        else:
            arrayStr = arrayStr + "[{}]".format(len2d(lst))
    else:
        arrayStr = arrayStr + "[{}]".format(len2d(lst))
        
    arrayStr = arrayStr + " = {}".format(arrOpen)
    
    for i, line in enumerate(lst):
        for j, d in enumerate(line):
            if radix == 'hex':
                data = "0x" + d 
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
                
        if pad:
            j = rowLen - len(line)
            if j > 0:
                for i in range(j):
                    if radix == 'hex':
                        data = "0x" + "00" 
                    elif radix == 'bin':
                        data = "0x" + rc.hex2bin(str(0), bits=8)
                    arrayStr = arrayStr + ", {}".format(data)
        
        if str2D:
            if i < len(lst)-1:            
                arrayStr = arrayStr + "{}, ".format(arrClose)
            else:
                arrayStr = arrayStr + "{}".format(arrClose)
    arrayStr = arrayStr + "{};".format(arrClose)
    
    
    return arrayStr, len2d(lst)
    
    
    
hexToDataArray()
    
