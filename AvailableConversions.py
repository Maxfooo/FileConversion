'''
Created on Jul 1, 2016

@author: maxr
'''

from Utils import RadixConversion
from FileIO import FileIO as FIO
from HexClass import HexClass
from FILE_TYPES import *


class AvailableConversions(object):

    def __init__(self):
        self.rc = RadixConversion()
        self.fio = FIO()
        self.conversionTable = dict()
        self.hexClass = HexClass()
        self.conversionTable.update(self.hexClass.hexConversionTable)
        self.conversionComplete = False


    def check(self, fromFileType, toFileType):
        if fromFileType in self.conversionTable.keys():
            if toFileType in self.conversionTable[fromFileType]:
                return True
            else:
                return False
        else:
            return False

    def convert(self, fromFileType, toFileType):
        if self.check(fromFileType, toFileType):
            if fromFileType == DOT_HEX:
                self.hexClass.convert(toFileType)
                self.conversionComplete = True
        else:
            self.fileIO.errorPopup('A conversion from {0} to {1} does not exist'.format(self.fromFileType, self.toFileType))
            self.conversionComplete = False


    def getConversionTable(self):
        return self.conversionTable

    def wasSuccessful(self):
        return self.conversionComplete









