'''
Created on Jan 23, 2016

@author: Max Ruiz
'''
from tkinter import *
from FileIO import FileIO
from Tools import RadixConversionUI, ADCCodeVoltUI
from AvailableConversions import AvailableConversions
from FILE_TYPES import *

class ConversionUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('File Converter')
        self.pack()

        self.fileIO = FileIO()
        self.fromFile = None
        self.toFile = None
        self.AC = AvailableConversions()
        self.conversionTable = self.AC.getConversionTable()

        self.fromFileType = DOT_HEX
        self.toFileType = DOT_MIF

        self.menuBar()

        self.mainFrame()

    def mainFrame(self):
        convertFromToFrame = LabelFrame(self, text = 'Available conversion: from -> to')
        self.fromListbox = Listbox(convertFromToFrame)
        i = 0
        for keys in self.conversionTable:
            self.fromListbox.insert(i, keys)
            i = i + 1
        self.fromListbox.pack(side='left')
        self.toListbox = Listbox(convertFromToFrame)
        self.toListbox.pack(side='left')
        convertFromToFrame.pack()

        self.convertButton = Button(self, text = 'Select Files and Convert', command = self.convertFile)
        self.convertButton.config(state=DISABLED)
        self.convertButton.pack(fill = 'both')


        logFrame = LabelFrame(self, text = 'Log')
        self.logText = StringVar()
        self.log = Message(logFrame, textvariable = self.logText, bg='white')
        self.log.pack(fill = 'both')
        logFrame.pack(fill='both')

        self.fromListbox.bind('<<ListboxSelect>>', self.updateToListbox)

    def convertFile(self):

        if self.fromFileType == None:
            self.logText.set('Please select a file to open.')
            self.fileIO.errorPopup('Please select a file to open.')
        elif self.toFileType == None:
            self.logText.set('Please select a file to be saved to.')
            self.fileIO.errorPopup('Please select a file to be saved to.')
        else:

            try:
                self.AC.convert(self.fromFileType, self.toFileType)
                if self.AC.wasSuccessful():
                    self.logText.set('Successfully converted {0} to {1}'.format(self.fromFileType, self.toFileType))
            except:
                self.logText.set('Could not convert {0} to {1}'.format(self.fromFileType, self.toFileType))
                self.fileIO.errorPopup('Could not convert {0} to {1}'.format(self.fromFileType, self.toFileType))

    def updateToListbox(self, event):
        sel = self.fromListbox.curselection()
        self.fromFileType = self.fromListbox.get(sel)
        self.logText.set('{} selected to open'.format(self.fromFileType))

        if self.toListbox.size() != 0:
            self.toListbox.delete(0, self.toListbox.size())

        for i in range(len(self.conversionTable[self.fromFileType])):
            self.toListbox.insert(i, self.conversionTable[self.fromFileType][i])

        self.convertButton.config(state=DISABLED)
        self.toListbox.bind('<<ListboxSelect>>', self.setToFileType)

    def setToFileType(self, event):
         sel = self.toListbox.curselection()
         self.toFileType = self.toListbox.get(sel)
         self.logText.set('{} selected to save to'.format(self.toFileType))

         # Enable convert button
         self.convertButton.config(state=ACTIVE)

    def menuBar(self):
        self.menubar = Menu(self)

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        toolsmenu = Menu(self.menubar, tearoff=0)
        toolsmenu.add_command(label="Radix Conversion", command=self.radixConversion)
        toolsmenu.add_separator()
        toolsmenu.add_command(label="ADC Code/Volt Convert", command=self.adcCodeVolt)
        self.menubar.add_cascade(label="Tools", menu=toolsmenu)

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="How To Use", command=self.howToUse)
        helpmenu.add_command(label="About", command=self.aboutProg)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=self.menubar)

    def radixConversion(self):
        root = Toplevel()
        subapp = RadixConversionUI(master=root)
        subapp.mainloop()

    def adcCodeVolt(self):
        root = Toplevel()
        subapp = ADCCodeVoltUI(master=root)
        subapp.mainloop()

    def aboutProg(self):
        pass

    def howToUse(self):
        pass

