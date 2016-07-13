'''
Created on Jul 5, 2016

@author: maxr
'''

from ParseHexFile import ParseHexFile
from arduinoCode import arduinoCode
from Utils import lst2d2str
from FileIO import FileIO as FIO
from MifUI import MifUI
from tkinter import Toplevel
from FILE_TYPES import *
import pickle


class HexClass(object):

    def __init__(self):
        self.hexConversionTable = {DOT_HEX : [DOT_MIF, DOT_INO, DOT_A51]}
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
        elif toFileType == DOT_A51:
            self.hexToA51(toFile)

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
        if dataArrFormat == None:
            format = ['dpl', 'dph', 'ndb', 'dat']
        else:
            format = dataArrFormat
        orgHexData = self.phf.structureHexContents(format)
        arrayStr, arrLen = lst2d2str(orgHexData, pad=False)

        inoFile.write(arduinoCode(arrLen, arrayStr, str(format) + " (repeated for however many hex lines where made)"))

        if printArr:
            print(arrayStr, "\n" + str(format) + " (repeated for however many hex lines where made)")

        inoFile.close()

    def hexToA51(self, a51File):
        try:
            instruction_table = pickle.load(open("instruction_table.p", 'rb'))
        except:
            print("No instruction_table file found.")
            return

        hexLetters = ['A', 'B', 'C', 'D', 'E', 'F']
        csegs = self.phf.getHexAddr()
        dataLines = self.phf.getHexData()
        print(1)
        for i, memLoc in enumerate(csegs):
            print(2)
            if i == 0:
                a51File.write('\n\ncseg ' + str(memLoc) + '\n')
            elif int(str(memLoc), 16) - 16 != csegs[i-1]:
                a51File.write('\n\ncseg ' + memLoc + '\n')

            print(3)
            paramCnt = 0
            paramWrtn = 0
            params = []
            cmd = ''
            cmdDone = True
            currInst = None
            for j, dat in enumerate(dataLines[i]):
                if cmdDone:
                    currInst = instruction_table[dat]
                    cmd = currInst[0]
                    paramCnt = currInst[1] - 1
                    print("param Count", paramCnt)
                    cmdDone = False

                if paramCnt == 0:
                    if len(params) == 1:
                        for hl in hexLetters:
                            lett = params[0].find(hl)
                            if lett == 0:
                                params[0] = '0' + params[0]
                        cmd = cmd % str(params[0])
                        print(cmd)
                        a51File.write(cmd + '\n')
                    elif len(params) == 2:
                        for p in range(2):
                            for hl in hexLetters:
                                lett = params[p].find(hl)
                                if lett == 0:
                                    params[p] = '0' + params[p]

                        cmd = cmd %(str(params[0]), str(params[1]))
                        print(cmd)
                        a51File.write(cmd + '\n')
                    else:
                        a51File.write(cmd + '\n')
                    cmdDone = True
                    params = []

                else:
                    cmdDone = False
                    params.append(dat)
                    paramCnt -= 1

        a51File.close()







