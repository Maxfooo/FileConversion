'''
Created on Jul 5, 2016

@author: maxr
'''

from ParseHexFile import ParseHexFile
from ProgramBoronArduinoCode import arduinoCode
from Utils import lst2d2str
from FileIO import FileIO as FIO
from MifUI import MifUI
from tkinter import Toplevel
from FILE_TYPES import *


class HexClass(object):
    
    def __init__(self):
        self.hexConversionTable = {DOT_HEX : [DOT_MIF, DOT_INO]}
        self.fio = FIO()
    
    def fetchMifParams(self):
        mifTop = Toplevel()
        self.mifApp = MifUI(mifTop)
        self.mifApp.mainloop()
        mifParams = self.mifApp.getParameters()
        mifTop.destroy()
        self.depth = int(mifParams[0])
        self.width = int(mifParams[1])
        self.address_radix = int(mifParams[2])
        self.data_radix = int(mifParams[3])
        self.fillZeros = int(mifParams[4])
    
    def convert(self, toFileType):
        self.fio.openFile(exten=DOT_HEX, ftypes=[('Hex files', DOT_HEX), ('all files', DOT_ALL)])
        fromFile = self.fio.getOpenedFile()
        self.phf = ParseHexFile(fromFile)
        self.fio.closeOpened()
        
        self.fio.saveFile(exten=toFileType, ftypes=[(toFileType.strip('.') + ' files', toFileType),
                                    ('all files', DOT_ALL)], ifilen='myfile' + toFileType)
        toFile = self.fio.getSavedFile()
        
        
        if toFileType == DOT_MIF:
            try:
                self.hexToMif(toFile)
            except:
                self.fio.errorPopup('Something\'s wrong with the Mif parameters!')
        elif toFileType == DOT_INO:
            self.hexToIno(toFile)
        
        self.fio.closeSaved()
        
    def hexToMif(self, mifFile):
        self.fetchMifParams()
        self.phf.setByteWidth(self.width)
        mifFile.write('DEPTH = {};\nWIDTH = {};\n'.format(str(self.depth),str(self.width)) +
                           'ADDRESS_RADIX = {};\n'.format(str(self.address_radix)) +
                           'DATA_RADIX = {};\n'.format((self.data_radix)) +
                           'CONTENT\nBEGIN\n')

        mifLineCount = 0
        for i in range(len(self.phf.hexLen)):
            tempAddress = []
            for j in range(int(self.phf.hexLen[i],self.data_radix)):
                addr = int(self.phf.hexAddr[i],self.data_radix)+j
                tempAddress.append(addr)
                if addr > mifLineCount:
                    mifLineCount = addr
            for k in range(len(tempAddress)):
                mifFile.write(str(hex(tempAddress[k])).replace('0x','') +
                                   '\t:\t' + str(self.phf.hexData[i][k]) + ';\n')
        # Fill in the rest of the addresses with 00
        if mifLineCount < int(self.depth) and self.fillZeros == 1:
            for i in range(int(self.depth) - mifLineCount):
                mifFile.write(str(hex(mifLineCount + i + 1)).replace('0x','') +
                                   '\t:\t' + '00' + ';\n')
        mifFile.write('END;')
        mifFile.close()
        
    def hexToIno(self, inoFile, dataArrFormat = None, printArr = False):
        print(1)
        if dataArrFormat == None:
            format = ['dpl', 'dph', 'ndb', 'dat']
        else:
            format = dataArrFormat
        print(2)
        orgHexData = self.phf.structureHexContents(format)
        arrayStr, arrLen = lst2d2str(orgHexData, pad=False)
        print(3)

        inoFile.write(arduinoCode(arrLen, arrayStr, str(format) + " (repeated for however many hex lines where made)"))
        
        if printArr:
            print(arrayStr, "\n" + str(format) + " (repeated for however many hex lines where made)")
            
        inoFile.close()
            
            
            
            
            
            
            
