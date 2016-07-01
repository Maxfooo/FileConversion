'''
Created on Jul 1, 2016

@author: maxr
'''

from Utils import *
from FileIO import FileIO as FIO
from ProgramBoronArduinoCode import arduinoCode as AC
from ParseHexFile import *
import re

class AvailableConversions(object):
    
    def __init__(self):
        self.rc = RadixConversion()
        self.fio = FIO()
    
    def hexToMif(self):
        self.fio.openFile(exten='.hex', ftypes=[('Hex files', '.hex'), ('all files', '.*')])
        fromFile = self.fio.getOpenedFile()
        phf = ParseHexFile(fromFile)
        self.fio.closeOpened()
        
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
        
    def hexToIno(self, dataArrFormat = None, printArr = False):
        self.fio.openFile(exten='.hex', ftypes=[('Hex files', '.hex'), ('all files', '.*')])
        fromFile = self.fio.getOpenedFile()
        phf = ParseHexFile(fromFile)
        self.fio.closeOpened()
        
        if dataArrFormat == None:
            format = ['dpl', 'dph', 'ndb', 'dat']
        else:
            format = dataArrFormat
        orgHexData = phf.structureHexContents(format)
        arrayStr, arrLen = lst2d2str(orgHexData, pad=False)
        
        self.fio.saveFile(exten='.ino', ftypes=[('Arduino files', '.ino'), ('all files', '.*')])
        toFile = self.fio.getSavedFile()
        toFile.write(AC(arrLen, arrayStr, str(format) + " (repeated for however many hex lines where made)"))
        self.fio.closeSaved()
        
        if printArr:
            print(arrayStr, "\n" + str(format) + " (repeated for however many hex lines where made)")
        
        
        
        
        
        
        
        
        
