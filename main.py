'''
Created on Jan 21, 2016

@author: Max Ruiz
'''
from tkinter import Tk
from ConversionUI import ConversionUI

if __name__ == '__main__':
    root = Tk()
    app = ConversionUI(master=root)
    app.mainloop()
