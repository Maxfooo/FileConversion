'''
Created on Jan 21, 2016

@author: Max Ruiz
'''
import re
from testing import tempAddress

class HEXClass(object):
    '''
    Intel hex
    http://www.keil.com/support/docs/1584/
    :LLAAAATT[DD...]CC
    '''


    def __init__(self, hexFile, mifFile):
        self.hexFile = hexFile
        self.mifFile = mifFile
        self.base = 16
        self.hexContent = None
        self.hexLen = []
        self.hexAddr = []
        self.hexType = []
        self.hexData = []
        self.hexCS = []
        self.hexTypeEOF = '01'
        self.hexFileSettings()
        self.readHEXFile()

    def hexFileSettings(self, depth=16, width=8, address_radix='HEX', data_radix='HEX', fillZeros=0):
        self.depth = depth
        self.width = width
        self.address_radix = address_radix
        self.data_radix = data_radix
        self.data_digits = self.base / width
        self.fillZeros = fillZeros

    def convertHEXtoMIF(self):
        self.sortHEXContents()
        self.writeMIFFile()
    
    def readHEXFile(self):
        try:
            if isinstance(self.hexFile, str):
                self.hexContent = self.hexFile
            self.hexContent = self.hexFile.read()
        except:
            pass

    def sortHEXContents(self):
        hex_format_expression = r':(\w{2})(\w{4})(\w{2})(\w*)(\w{2})'
        hexFields = re.findall(hex_format_expression,self.hexContent)
        
        for records in hexFields:
            self.hexLen.append(records[0])
            self.hexAddr.append(records[1])
            self.hexType.append(records[2])
            if self.hexType[-1] == self.hexTypeEOF:
                self.hexData.append(['00'])
            else:
                self.hexData.append(re.findall(r'\w{%d}' %self.data_digits,records[3]))
            self.hexCS.append(records[4])
                

    def writeMIFFile(self):
        self.mifFile.write('DEPTH = {};\nWIDTH = {};\n'.format(self.depth,self.width) +
                           'ADDRESS_RADIX = {};\n'.format(self.address_radix) +
                           'DATA_RADIX = {};\n'.format(self.data_radix) +
                           'CONTENT\nBEGIN\n')
        

        self.mifLineCount = 0
        for i in range(len(self.hexLen)):
            tempAddress = []
            for j in range(int(self.hexLen[i],self.base)):
                addr = int(self.hexAddr[i],self.base)+j
                tempAddress.append(addr)
                if addr > self.mifLineCount:
                    self.mifLineCount = addr
            for k in range(len(tempAddress)):
                self.mifFile.write(str(hex(tempAddress[k])).replace('0x','') +
                                   '\t:\t' + str(self.hexData[i][k]) + ';\n')
        
        
        # Fill in the rest of the addresses with 00
        if self.mifLineCount < int(self.depth) and self.fillZeros == 1:
            for i in range(int(self.depth) - self.mifLineCount):
                    self.mifFile.write(str(hex(self.mifLineCount + i + 1)).replace('0x','') +
                                   '\t:\t' + '00' + ';\n')
        
        self.mifFile.write('END;')
        
        













