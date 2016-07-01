'''
Created on Jul 1, 2016

@author: maxr
'''
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
