'''
Created on Jun 23, 2016

@author: maxr
'''
from tkinter import *
from Utils import RadixConversion as RC

class RadixConversionUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('Radix Conversion')
        self.pack()

        self.rc = RC()
        self.mainFrame()

    def mainFrame(self):

        binFrame = LabelFrame(self, text="Binary Converter")
        fromBinVal = StringVar()
        self.binEntry = Entry(binFrame, textvariable=fromBinVal)
        self.binEntry.pack(side='left')
        binButton = Button(binFrame, text="Convert", command=lambda: self.convert('bin'))
        binButton.pack(side='left')

        binResultFrame = Frame(binFrame)
        self.binResultText = Text(binResultFrame, height=3, width = 20)
        self.binResultText.pack()
        binResultFrame.pack(side='left', fill=BOTH)

        binFrame.pack()

        hexFrame = LabelFrame(self, text="Hex Converter")
        fromHexVal = StringVar()
        self.hexEntry = Entry(hexFrame, textvariable=fromHexVal)
        self.hexEntry.pack(side='left')
        hexButton = Button(hexFrame, text = "Convert", command=lambda: self.convert('hex'))
        hexButton.pack(side='left')

        hexResultFrame = Frame(hexFrame)
        self.hexResultText = Text(hexResultFrame, height=3, width=20)
        self.hexResultText.pack()
        hexResultFrame.pack(side='left',fill=BOTH)

        hexFrame.pack()

        decFrame = LabelFrame(self, text="Decimal Converter")
        fromDecVal = StringVar()
        self.decEntry = Entry(decFrame, textvariable=fromDecVal)
        self.decEntry.pack(side='left')
        decButton = Button(decFrame, text="Convert", command=lambda: self.convert('dec'))
        decButton.pack(side='left')

        decResultFrame = Frame(decFrame)
        self.decResultText = Text(decResultFrame, height=3, width=20)
        self.decResultText.pack()
        decResultFrame.pack(side='left')

        decFrame.pack()

    def convert(self, fromType=None):
        if fromType == 'bin':
            val = self.binEntry.get()
            try:
                self.binResultText.delete('0.0', END)
                self.binResultText.insert(INSERT, "Hex: {}\n".format(self.rc.bin2hex(val)))
                self.binResultText.insert(INSERT, "Dec: {}".format(self.rc.bin2dec(val)))
            except:
                self.binResultText.delete('0.0', END)
                self.binResultText.insert(INSERT, "Invalid Entry")

        elif fromType == 'hex':
            val = self.hexEntry.get()

            try:
                if val.find(',') != -1:
                    temp = val.split(',')
                    val = temp[0]
                    if temp[1] == '':
                        bits = None
                    else:
                        bits = int(temp[1])
                else:
                    bits = None
                self.hexResultText.delete('0.0', END)
                self.hexResultText.insert(INSERT, "Bin: {}\n".format(self.rc.hex2bin(val,bits=bits)))
                self.hexResultText.insert(INSERT, "Dec: {}".format(self.rc.hex2dec(val)))
            except:
                self.hexResultText.delete('0.0', END)
                self.hexResultText.insert(INSERT, "Invalid Entry")

        elif fromType == 'dec':
            val = self.decEntry.get()

            try:
                if val.find(',') != -1:
                    temp = val.split(',')
                    val = temp[0]
                    if temp[1] == '':
                        bits = None
                    else:
                        bits = int(temp[1])
                else:
                    bits = None
                self.decResultText.delete('0.0', END)
                self.decResultText.insert(INSERT, "Bin: {}\n".format(self.rc.dec2bin(val,bits=bits)))
                self.decResultText.insert(INSERT, "Hex: {}".format(self.rc.dec2hex(val)))
            except:
                self.decResultText.delete('0.0', END)
                self.decResultText.insert(INSERT, "Invalid Entry")


class ADCCodeVoltUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('ADC Volt/Code Conversion')
        self.pack()

        self.mainFrame()

    def mainFrame(self):

        circuitParamsFrame = LabelFrame(self, text="Static Params")

        adcBitsFrame = Frame(circuitParamsFrame)
        adcBitsLabel = Label(adcBitsFrame, text = "ADC Bit Precision")
        adcBitsLabel.pack(side='left')
        adcBitsVal = StringVar()
        self.adcBitsEntry = Entry(adcBitsFrame, textvariable=adcBitsVal, relief=SUNKEN)
        self.adcBitsEntry.pack(side='right')
        adcBitsFrame.pack()

        maxVoltFrame = Frame(circuitParamsFrame)
        maxVoltLabel = Label(maxVoltFrame, text = "Maximum Voltage")
        maxVoltLabel.pack(side='left')
        maxVoltVal = StringVar()
        self.maxVoltEntry = Entry(maxVoltFrame, textvariable=maxVoltVal)
        self.maxVoltEntry.pack(side='right')
        maxVoltFrame.pack(fill=BOTH)

        circuitParamsFrame.pack(side='top')

        v2cFrame = LabelFrame(self, text = "Volt to ADC Code")

        v2cEntryFrame = Frame(v2cFrame)

        v2cInputVoltFrame = Frame(v2cEntryFrame)
        v2cInputVoltLabel = Label(v2cInputVoltFrame, text = "Input Voltage")
        v2cInputVoltLabel.pack(side='left')
        v2cInputVoltVal = StringVar()
        self.v2cInputVoltEntry = Entry(v2cInputVoltFrame, textvariable=v2cInputVoltVal)
        self.v2cInputVoltEntry.pack(side='right',fill=BOTH)
        v2cInputVoltFrame.pack(fill=BOTH)

        v2cEntryFrame.pack(fill=BOTH)

        v2cButton = Button(v2cFrame, text="Convert", command=lambda:self.convert('v2c'), padx=10)
        v2cButton.pack()

        self.v2cResultText = Text(v2cFrame, height=5, width = 20)
        self.v2cResultText.pack(fill=BOTH)

        v2cFrame.pack(fill=BOTH)

        """ ------------------"""
        c2vFrame = LabelFrame(self, text = "ADC Code to Voltage")

        c2vEntryFrame = Frame(c2vFrame)

        c2vInputCodeFrame = Frame(c2vEntryFrame)
        c2vInputCodeLabel = Label(c2vInputCodeFrame, text = "Input ADC Code")
        c2vInputCodeLabel.pack(side='left')
        c2vInputCodeVal = StringVar()
        self.c2vInputCodeEntry = Entry(c2vInputCodeFrame, textvariable=c2vInputCodeVal)
        self.c2vInputCodeEntry.pack(side='right',fill=BOTH)
        c2vInputCodeFrame.pack(fill=BOTH)

        c2vEntryFrame.pack(fill=BOTH)

        c2vButton = Button(c2vFrame, text="Convert", command=lambda:self.convert('c2v'), padx=10)
        c2vButton.pack()

        self.c2vResultText = Text(c2vFrame, height=5, width = 20)
        self.c2vResultText.pack(fill=BOTH)

        c2vFrame.pack(fill=BOTH)

    def convert(self, type):
        adcBits = self.adcBitsEntry.get()
        maxVolt = self.maxVoltEntry.get()
        try:
            adcBits = int(adcBits)
            maxVolt = float(maxVolt)
            maxADCCode = 2**adcBits-1
            if type == 'v2c':
                try:
                    frac = round(float(self.v2cInputVoltEntry.get()) / float(maxVolt), 3)
                    adcCode = round(frac*maxADCCode)
                    self.v2cResultText.delete('0.0', END)
                    self.v2cResultText.insert(INSERT, "Max ADC Code: {}\n".format(str(maxADCCode)))
                    self.v2cResultText.insert(INSERT, "Fraction: {}\n".format(str(frac)))
                    self.v2cResultText.insert(INSERT, "ADC Code: {}\n".format(adcCode))

                except:
                    self.v2cResultText.delete('0.0', END)
                    self.v2cResultText.insert(INSERT, "Invalid Input")


            elif type == 'c2v':
                try:
                    adcCodeDec = int(self.c2vInputCodeEntry.get(), 2)
                    frac = round(adcCodeDec / maxADCCode, 3)
                    adcVolt = round(frac*maxVolt, 4)
                    self.c2vResultText.delete('0.0', END)
                    self.c2vResultText.insert(INSERT, "Max ADC Code: {}\n".format(str(maxADCCode)))
                    self.c2vResultText.insert(INSERT, "ADC Code Dec Val: {}\n".format(str(adcCodeDec)))
                    self.c2vResultText.insert(INSERT, "Fraction: {}\n".format(str(frac)))
                    self.c2vResultText.insert(INSERT, "Voltage: {}\n".format(adcVolt))
                except:
                    self.c2vResultText.delete('0.0', END)
                    self.c2vResultText.insert(INSERT, "Invalid Input")

        except:
            self.v2cResultText.delete('0.0', END)
            self.v2cResultText.insert(INSERT, "Check Bit precision or Max voltage")
            self.c2vResultText.delete('0.0', END)
            self.c2vResultText.insert(INSERT, "Check Bit precision or Max voltage")


"""
if __name__ == '__main__':
    root = Tk()
    #app = RadixConversionUI(master=root)
    app = ADCCodeVoltUI(master=root)
    app.mainloop()
"""
