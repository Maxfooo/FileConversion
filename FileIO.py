'''
Created on Jan 21, 2016

@author: Max Ruiz
'''
import tkinter
from tkinter import filedialog
from tkinter import messagebox

class FileIO():

    def __init__(self):
        self.openedFile = None
        self.readFile = None
        self.savedFile = None
        self.fileLocation = None
        self.folderLocation = None

    def filePrompt(self, command = 'open', msg = ''):
        root = tkinter.Tk()
        root.withdraw()
        if(command == 'open'):
            messagebox.showinfo('Open File','Please select a file to open!\n{}'.format(msg))
        elif(command == 'save'):
            messagebox.showinfo('Save File','Please select a file to save to!\n{}'.format(msg))
        elif(command == 'file'):
            messagebox.showinfo('File Location','Please locate a file!\n{}'.format(msg))
        elif(command == 'folder'):
            messagebox.showinfo('Folder Location','Please locate a folder!\n{}'.format(msg))


    def openFile(self, exten='.hex', ftypes=[('all files', '.*')], idir='C:\\',
                 ifilen='myfile.hex', title='Open File'):
        root = tkinter.Tk()
        file_opt = options = {}
        options['defaultextension'] = exten
        options['filetypes'] = ftypes
        options['initialdir'] = idir
        options['initialfile'] = ifilen
        options['parent'] = root
        options['title'] = title
        root.withdraw()
        self.openedFile = filedialog.askopenfile(mode='r', **file_opt)

    def openFileRead(self, exten='.hex', ftypes=[('all files', '.*')], idir='C:\\',
                 ifilen='myfile.hex', title='Open File'):
        root = tkinter.Tk()
        file_opt = options = {}
        options['defaultextension'] = exten
        options['filetypes'] = ftypes
        options['initialdir'] = idir
        options['initialfile'] = ifilen
        options['parent'] = root
        options['title'] = title
        root.withdraw()
        self.openedFile = filedialog.askopenfile(mode='r', **file_opt)
        self.readFile = self.openedFile.read()
        self.openedFile.close()


    def saveFile(self, exten='.hex', ftypes=[('all files', '.*')], idir='C:\\',
                 ifilen='myfile.hex', title='Save File'):
        root = tkinter.Tk()
        file_opt = options = {}
        options['defaultextension'] = exten
        options['filetypes'] = ftypes
        options['initialdir'] = idir
        options['initialfile'] = ifilen
        options['parent'] = root
        options['title'] = title
        root.withdraw()
        self.savedFile = filedialog.asksaveasfile(mode='w', **file_opt)

    def fileLocation(self):
        exten='.*'
        ftypes=[('all files', '.*')]
        idir='C:\\',
        title='Get File Location'

        root = tkinter.Tk()
        file_opt = options = {}
        options['defaultextension'] = exten
        options['filetypes'] = ftypes
        options['initialdir'] = idir
        options['parent'] = root
        options['title'] = title
        root.withdraw()

        self.locatedFile = filedialog.askopenfilename(**file_opt)

    def folderLocation(self):
        root = tkinter.Tk()
        file_opt = options = {}
        options['parent'] = root
        root.withdraw()
        self.locatedFolder = filedialog.askdirectory(parent=root, title='Path to Copy to', \
                                         initialdir='.')

    def errorPopup(self, message):
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror('ERROR', message)

    def getOpenedFile(self):
        try:
            if self.openedFile.closed:
                return None
            else:
                return self.openedFile
        except:
            return None


    def getReadFile(self):
        return self.readFile

    def getSavedFile(self):
        return self.savedFile

    def getFileLocation(self):
        return self.fileLocation

    def getFolderLocation(self):
        return self.folderLocation

    def closeOpened(self):
        try:
            if self.openedFile.closed:
                pass
            else:
                self.openedFile.close()
        except:
            pass

    def closeSaved(self):
        try:
            if self.savedFile.closed:
                pass
            else:
                self.savedFile.close()
        except:
            pass
