'''
Created on Jan 23, 2016

@author: Max Ruiz
'''
from tkinter import *
from FileIO import *
from HEXClass import *
from HexUI import *
from Tools import RadixConversionUI, ADCCodeVoltUI

class ConversionUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('File Converter')
        self.pack()

        self.fileIO = FileIO()
        self.fromFile = None
        self.toFile = None
        self.conversionTable = {'.hex' : ['.mif']}

        self.fromFileType = '.hex'
        self.toFileType = '.mif'

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

        fileConvertFrame = LabelFrame(self, text = 'Select files')
        
        """ Only a "Select files and convert" button. This button will then
        take the selected file types from the listbox and from there, the 
        appropriate files will be opened.
        
        If the "from" and "to" files have not been selected from the 
        listbox, then the button should be greyed out.
        
        This still needs to be added.
        """
        convertButton = Button(fileConvertFrame, text = 'Convert', command = self.convertFile)
        convertButton.pack(side='left',fill = 'both')
        fileConvertFrame.pack(fill = 'both')


        logFrame = LabelFrame(self, text = 'Log')
        self.logText = StringVar()
        self.log = Message(self, textvariable = self.logText, bg='white')
        self.log.pack(fill = 'both')
        logFrame.pack()

        self.fromListbox.bind('<<ListboxSelect>>', self.updateToListbox)


    def getFromFile(self):
        self.fileIO.openFile(exten = self.fromFileType, 
                             ftypes=[('{}'.format(self.fromFileType), '.{}'.format(self.fromFileType)),
                                    ('all files', '.*')], ifilen='myfile{}'.format(self.fromFileType))
        self.fromFile = self.fileIO.getOpenedFile()
        self.fileIO.closeOpened()

    def getToFile(self):
        self.fileIO.saveFile(exten = self.toFileType, 
                             ftypes=[('{}'.format(self.toFileType), '{}'.format(self.toFileType)),
                                    ('all files', '.*')], ifilen='myfile{}'.format(self.toFileType))
        self.toFile = self.fileIO.getSavedFile()
        self.fileIO.closeSaved()

    def convertFile(self):
        self.getFromFile()
        
        
        
        
        if self.fromFile == None:
            self.logText.set('Please select a file to open.')
            self.fileIO.errorPopup('Please select a file to open.')
        elif self.toFile == None:
            self.logText.set('Please select a file to be saved to.')
            self.fileIO.errorPopup('Please select a file to be saved to.')
        else:
            if self.fromFileType == '.hex' and self.toFileType == '.mif':
                hexClass = HEXClass(self.fromFile, self.toFile)
                try:
                    hexClass.hexFileSettings(depth=self.hexParams[0], width=self.hexParams[1],
                                             address_radix=self.hexParams[2], data_radix=self.hexParams[3],
                                             fillZeros=self.hexParams[4])
                    hexClass.convertHEXtoMIF()
                    self.fileIO.closeOpened()
                    self.fileIO.closeSaved()
                    self.logText.set('Successfully converted {0} to {1}'.format(self.fromFileType, self.toFileType))
                except:
                    self.fileIO.errorPopup('Please fill in Hex parameters!')
            else:
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

        self.toListbox.bind('<<ListboxSelect>>', self.setToFileType)

        try:
            self.constructTypeUI()
        except:
            pass

    def constructTypeUI(self):
        if self.fromFileType == '.hex':
            hexTop = Toplevel()
            self.hexApp = HexUI(hexTop)
            self.hexApp.mainloop()
            self.hexParams = self.hexApp.getParameters()
            hexTop.destroy()
        else:
            pass

    def setToFileType(self, event):
         sel = self.toListbox.curselection()
         self.toFileType = self.toListbox.get(sel)
         self.logText.set('{} selected to save to'.format(self.toFileType))

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

