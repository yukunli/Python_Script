"""
File:  ksdkGUI.py
=================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Class for PGKSDK GUI**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.5

Inheritance
+++++++++++
.. inheritance-diagram:: ksdkGUI

UML
+++
.. uml:: {{/../../../src/ksdkGUI.py

API
+++

"""

## USER MODULES
from ksdkTools import KsdkTools as kT
import ksdkTools as kTool
import ksdkObj as kSdk
import ksdkProj as kProj
import ksdkImg as kImg
import ksdkIar as kIar
import ksdkIarNew as kIarNew
import ksdkKds as kKds
import ksdkKdsNew as kKdsNew
import ksdkMdk as kMdk
import ksdkMdkNew as kMdkNew
import ksdkAtl as kAtl
import ksdkAtlNew as kAtlNew

## PYTHON MODULES
from Tkinter import *
from ttk import *
import tkFileDialog
import tkMessageBox
import re
import time
import sys
import os
import platform
import getpass
import subprocess
import shutil
import webbrowser
import xml.etree.ElementTree as ET
import json
import threading
from ksdkObj import ToolchainType
import Constants
import Texts

#: PGKSDK name displayed in window bar
PGKSDK_NAME = 'KSDK Project Generator'

#: PGKSDK Version displayed in window bar
PGKSDK_VERSION = '2.0'

ADVANCED_ENABLE = True

WIN_SCALE = 1

#Initial image displayed in GUI
testImage = kImg.boardImages['kds_icon.gif']

#Advanced help text
ADV_HELP = "Choose to create a 'New' project or 'Clone' an existing one.\n" + \
           "\n" + \
           "New:\n" + \
           "\t- Select the options you wish to use for your project.\n" + \
           "\t- Some selections will restrict your options to prevent adding\n" + \
           "\t  incompatible components.\n" + \
           "\t- A toolchain must be selected in order for a project to be\n" + \
           "\t  generated.\n" + \
           "\n" + \
           "Clone:\n" + \
           "\t- Cloned projects will retain their original names. They will\n" + \
           "\t  be placed into '/examples/{selectedBoard}/user_apps' if\n" + \
           "\t  the 'Generate standalone project' checkbox is not checked.\n" + \
           "\n" + \
           "Advanced Generate:\n" + \
           "\t- Will generate a project based solely on the configuration in\n" + \
           "\t  this window.\n"


MQX_DEVICES = ['K21DA5', 'K21FA12', 'K22F51212', 'K24F25612', 'K60D10', 'K64F12', 'K65F18', 'K66F18', \
               'K80F25615', 'K81F25615', 'K82F25615', 'KL25Z4', 'KL26Z4', 'KL27Z644', 'KL33Z644', 'KL43Z4', \
               'KL46Z4', 'KV10Z1287', 'KV10Z7', 'KV11Z7', 'KV31F51212', 'KV46F15', 'KV46F16', 'KV56F22', 'KV58F22', 'KW01Z4', 'KW24D5', 'KW40Z4']

RTOS_DEVICES = ['K21DA5', 'K21FA12', 'K22F51212', 'K24F25612', 'K60D10', 'K64F12', 'K65F18', 'K66F18', \
               'K80F25615', 'K81F25615', 'K82F25615', 'KL25Z4', 'KL26Z4', 'KL27Z644', 'KL33Z644', 'KL43Z4', \
               'KL46Z4', 'KV10Z1287', 'KV11Z7', 'KV31F51212', 'KV46F15', 'KV46F16', 'KV56F22', 'KV58F22', 'KW01Z4', 'KW24D5', 'KW40Z4']


class PgGui(Frame):
    """
    This class contains all the methods used to generate the GUI widgets
    """

    def __init__(self, master=None):
        """Init function for the PgGui class

            :param master: Tkinter object

            .. todo::

                Add try,except to catch bad paths

        """
        Frame.__init__(self, master)

        self.currState = ''
        self.widgetList = []

        self.string = ""
        self.grid()

        # Set defaults
        osName = platform.system()
        kT.debug_log(osName)
        projName = 'myProject'
        # Check for settings file
        if osName != 'Darwin':
            self.settingsPath = './settings.json'
        else:
            ##print os.getcwd()
            self.settingsPath = '/Users/' + getpass.getuser() + '/Documents/KSDK_Project_Generator/settings.json'

        if os.path.isfile(self.settingsPath):
            with open(self.settingsPath, "r+") as f:
                jsonSettings = json.load(f)
                ##print jsonSettings[0]
                if osName == "Windows":
                    osBuild = platform.release()
                elif osName == "Linux":
                    osBuild = str(platform.linux_distribution()[0]) + ' ' + \
                              str(platform.linux_distribution()[1])
                else:
                    osBuild = platform.mac_ver()[0]
                userName = jsonSettings[0]["userName"]
                ksdkPath = jsonSettings[0]["ksdkPath"]
                f.close()
        else:
            userName = getpass.getuser()
            #try to find SDK
            directoryPrefix = ''
            
            if osName == "Windows":
                directoryPrefix = 'C:\\'
            elif osName == 'Linux':
                directoryPrefix = '/home/' + userName + '/'
            else:
                if not os.path.isdir('/Users/' + userName + '/Documents/KSDK_Project_Generator'):
                    os.makedirs('/Users/' + userName + '/Documents/KSDK_Project_Generator')
                directoryPrefix = '/Applications/'
            
            #first check content of nxp dir
            nxpPath = directoryPrefix + 'nxp'
            sdkPathList = []
            if os.path.isdir(nxpPath):
                for d in os.listdir(nxpPath):
                    if os.path.isdir(os.path.join(nxpPath, d)):
                        if d.find('SDK_') != -1:
                            sdkPathList.append(os.path.join(nxpPath, d))
            # if there is no SDK check Freescale directory
            if len(sdkPathList) == 0:
                freescalePath = directoryPrefix + 'Freescale'
                if os.path.isdir(freescalePath):
                    for d in os.listdir(freescalePath):
                        if os.path.isdir(os.path.join(freescalePath, d)):
                            if d.find('SDK_') != -1:
                                sdkPathList.append(os.path.join(freescalePath, d))
            if len(sdkPathList) != 0:
                sdkTwo = [d for d in sdkPathList if d.find('SDK_2') != -1]
                sdkOnePointThree = [d for d in sdkPathList if d.find('SDK_1.3') != -1]
                sdkOnePoinTwo = [d for d in sdkPathList if d.find('SDK_1.2') != -1]
                if len(sdkTwo) != 0:
                    ksdkPath = sdkTwo[0]
                elif len(sdkOnePointThree) != 0:
                    ksdkPath = sdkOnePointThree[0]
                elif len(sdkOnePoinTwo) != 0:
                    ksdkPath = sdkOnePoinTwo[0]
                else:
                    ksdkPath = 'No KSDK Found, please choose a path.'
            else:   
                ksdkPath = 'No KSDK Found, please choose a path.'
            
            # Tried to find a local installation
            if osName == "Windows":
                osBuild = platform.release()
            elif osName == 'Linux':
                osBuild = str(platform.linux_distribution()[0]) + ' ' + \
                          str(platform.linux_distribution()[1])
            elif osName == 'Darwin':
                osBuild = platform.mac_ver()[0]
            # Save details to JSON file
            settingsData = [{'userName':userName, 'ksdkPath':ksdkPath}]
            try:
                with open(self.settingsPath, "w+") as f:
                    json.dump(settingsData, f, sort_keys=True, indent=2)
                    f.close()
            except IOError:
                tkMessageBox.showinfo("Error", \
                                      'Check Read/Write permissions.')

        curDate = time.strftime("%m/%d/%Y")
        kT.debug_log(curDate)
        kT.debug_log('\n\n\tKSDK Project Generator running on ' + osName + ' ' + osBuild + \
                     '\n\n\tUser: ' + userName + \
                     '\n\tDate: ' + curDate + '\n\n')

        # Create a KSDK object
        self.localSDK = kSdk.kinetisSDK(ksdkPath)               # Create new KSDK object
        self.newProj = kProj.ksdkProjClass(projName, self.localSDK.get_version(), self.localSDK.path, \
                                          osName, userName, curDate)
        
        ### TODO: Add try,except to catch bad paths
        self.validPath = True
        try:
            self.localSDK.get_version()
        except IOError:
            self.validPath = False

        # defining options for opening a directory
        self.dir_opt = {}
        if osName == 'Windows':
            self.dir_opt['initialdir'] = 'C:\\'
        elif osName == 'Linux':
            self.dir_opt['initialdir'] = '/home/' + userName
        elif osName == 'Darwin':
            self.dir_opt['initialdir'] = '/Users/' + userName
        self.dir_opt['mustexist'] = False
        self.dir_opt['parent'] = master

        # Create Vars for Advanced GUI
        self.advancedProjType = IntVar(self)
        self.advancedLibType = IntVar(self)
        self.advancedRtosType = IntVar(self)
        self.advIsKds = IntVar(self)
        self.advIsIar = IntVar(self)
        self.advIsMdk = IntVar(self)
        self.advIsAts = IntVar(self)
        self.advIsGcc = IntVar(self)
        self.advIsBsp = IntVar(self)
        self.advIsUsb = IntVar(self)
        self.advIsStandalone = IntVar(self)
        self.advBrdSelect = StringVar(self)
        self.advDevSelect = StringVar(self)
        self.advancedDevType = IntVar(self)
        self.devPackage = StringVar(self)

        # Map callback functions to Vars
        self.advDevSelect.trace('w', self.update_proj)
        self.advancedProjType.trace('w', self.update_gui)
        self.advancedLibType.trace('w', self.update_proj)
        self.advancedRtosType.trace('w', self.update_proj)

        self.advIsStandalone.trace('w', self.update_proj)
        self.advBrdSelect.trace('w', self.clone_update)
        self.advancedDevType.trace('w', self.update_dev)
        self.devPackage.trace('w', self.update_package)
        
        #updates path to projects
        self.advBrdSelect.trace('w', self.update_proj)

        self.prevProjType = self.advancedProjType.get()
        self.prevWksp = ''
        self.prevName = ''
        self.curr = ''
        self.currBoard = ''
        self.displayBoard = None
        self.imageList = []
        self.firstLoad = True
        self.isValidConfig = IntVar()
        self.isValidConfig.set(0)
        self.isHalSet = False
        self.sessionSDKPath = None
        self.standAloneProj = False

        self.showWarning = IntVar(self)
        self.showWarning.set(0)  ## Kind of inverted logic
        self._retLoop = None

        # support automation test
        self.pop_gen = None
        self.pop_package = None

        self.main_gui(master)

    def main_gui(self, master):
        """Main class method for generate first menu 'Quick start menu'

            It appends the list of widgets (buttons, labels, entries, etc...)
            in order for the next menu method to remove those widgets on launch.

            :param master: Tkinter object
        """
        # Turn off polling function
        self._retLoop = None

        # Reset advanced options
        self.advancedProjType.set(0)
        self.advancedRtosType.set(0)
        self.advIsKds.set(0)
        self.advIsIar.set(0)
        self.advIsMdk.set(0)
        self.advIsAts.set(0)
        self.advIsGcc.set(0)
        self.advIsBsp.set(0)
        self.advIsUsb.set(0)
        self.advIsStandalone.set(0)
        self.advancedDevType.set(0)

        kT.debug_log(self.validPath)

        #kT.debug_log("DPI Scale: " + str(WIN_SCALE))

        #Remove active widgets from the screen and then clear widget list out
        if self.widgetList:
            for w in self.widgetList:
                w.grid_remove()
            del self.widgetList[:]

        # Begin repopulating window with new widget list
        osName = platform.system()
        if osName != 'Darwin':
            labelFont =  'Arial 9 bold'
        else:
            labelFont = 'bold'

        ### Widget 0 is a label for KSDK path entry
        self.widgetList.append(Label(self, text='KSDK Path:', font=labelFont))
        self.widgetList[0].grid(row=0, column=1, sticky=W, pady=(5, 0))

        ### Widget 1 is a text field entry for KSDK path
        #### By default the text field is populated with the KSDK_PATH variable
        if self.newProj.osType == 'Windows':
            self.widgetList.append(Entry(self, width=55))
        else:
            self.widgetList.append(Entry(self, width=45))
        self.widgetList[1].insert(0, self.localSDK.path)
        self.widgetList[1].grid(row=1, column=1, sticky=W, pady=(0, 0))

        self.localSDK.setNewKSDKPath(self.widgetList[1].get())

        ### Widget 2 is a button to browse for KSDK path
        self.dir_opt['title'] = 'Select the directory containing the ' + \
                                'version of KSDK you wish to use.'
        self.widgetList.append(Button(self, text='Browse', \
                                      command=lambda: self.ask_set_directory(False, 1)))
        self.widgetList[2].grid(row=1, column=2, columnspan=2, sticky=E+W, pady=(0, 0))

        ### Widget 3 is a label for the project name text field
        self.widgetList.append(Label(self, text='Project Name:', font=labelFont))
        self.widgetList[3].grid(row=2, column=1, sticky=W, pady=(0, 0))

        ### Widget 4 is the text field for project name entry
        if self.newProj.osType == 'Windows':
            self.widgetList.append(Entry(self, width=55))
        else:
            self.widgetList.append(Entry(self, width=45))
        self.widgetList[4].insert(0, self.newProj.name)
        self.widgetList[4].grid(row=3, column=1, sticky=W,)

        ### Widgets 5-7 are for the board list
        #### Widget 5 is a scrollbar
        #### Widget 6 is a list box for all the support boards
        #### Widget 7 is the label for the board list
        self.widgetList.append(Scrollbar(self, orient=VERTICAL))
        self.widgetList.append(Listbox(self, yscrollcommand=self.widgetList[5].set))
        self.widgetList.append(Label(self, text='Choose board:', font=labelFont))
        self.widgetList[5].config(command=self.widgetList[6].yview)
        self.widgetList[5].grid(row=5, column=2, sticky=N+S+W, pady=(0, 0))
        self.widgetList[6].grid(row=5, column=1, sticky=E+W, pady=(0, 0))
        self.widgetList[7].grid(row=4, column=1, sticky=W+N, pady=(5, 0))

        self.widgetList[6].config(state=(NORMAL if self.validPath else DISABLED))

        # Call to populate list box with board names
        self.pop_main_boards()

        # Set current selection to inital index of the board list
        self.curr = self.widgetList[6].curselection()

        # Set initial display image for board preview
        ### Widget 8 is a 'thumbnail' board preview (big thumbs)
        self.displayBoard = PhotoImage(data=testImage)
        self.widgetList.append(Button(self, \
                                      image=self.displayBoard, \
                                      command=lambda: self.web_launch(self.imageList[0][:-10])))
        self.widgetList[8].image = self.displayBoard
        self.widgetList[8].grid(row=5, column=3, columnspan=3, sticky=E+W+N+S)

        ### Widget 9 is a help button to provide assistance to the user
        helpString = 'Provide a valid KSDK installation path.\n' + \
                     'Enter a name for your new project.\n' + \
                     'Select a board from the list of Freescale development boards.\n' + \
                     'Click the \"Quick Generate!\" button to create your project.\n'
        self.widgetList.append(Button(self, text='Help', \
                                      command=lambda: self.pop_up_help(master, helpString)))
        self.widgetList[9].grid(row=1, column=4, sticky=E, columnspan=2, pady=(0, 0))

        ### Widget 10 is the button to generate the project
        if self.newProj.osType == 'Windows':
            style = Style()
            style.configure("Bold.TButton", font='system 8 bold')
            self.widgetList.append(Button(self, text='Quick Generate!', style="Bold.TButton", \
                                          command=lambda: self.begin_quick_gen(master)))
            self.widgetList[10].grid(row=11, column=4, rowspan=2, columnspan=2, \
                                     sticky=E+W+N+S, pady=(4, 0))
        else:
            self.widgetList.append(Button(self, text='Quick Generate!', \
                                          command=lambda: self.begin_quick_gen(master)))
            self.widgetList[10].grid(row=11, column=4, rowspan=2, columnspan=2, \
                                     sticky=E+W+N+S, pady=(4, 0))
        self.widgetList[10].state(["!disabled" if self.validPath else "disabled"])

        ### Widget 11 is a button to launch the advance project generator
        self.widgetList.append(Button(self, text='Advanced', \
                                      command=lambda: self.advanced_gui(master)))
        self.widgetList[11].grid(row=11, column=1, columnspan=1, sticky=W, pady=(4, 0))
        #self.widgetList[11].state(["!disabled" if self.validPath else "disabled"])
        self.widgetList[11].state(["!disabled" if ADVANCED_ENABLE else "disabled"])
        if not ADVANCED_ENABLE:
            self.widgetList[11].grid_remove()

        self.widgetList.append(Label(self, text='Usage Tips', foreground='forestgreen', \
                                     font=labelFont))
        self.widgetList[12].grid(row=6, column=1, sticky=W)

        self.defaultHelp = 'Hover over an item to view usage tips.\n\n\n'
        self.widgetList.append(Label(self, text=self.defaultHelp))
        self.widgetList[13].grid(row=7, column=1, rowspan=4, columnspan=6, sticky=W)

        ### Widget 14 is a label for padding column 0
        self.widgetList.append(Label(self, text='', font=labelFont))
        self.widgetList[14].grid(row=0, column=0, sticky=E+W, padx=5)

        ### Widget 15 is a label for padding row 13
        self.widgetList.append(Label(self, text='', font=labelFont))
        self.widgetList[15].grid(row=0, column=6, sticky=E+W, padx=5)

        ### Widget 16 is a label to explain the advanced button
        self.widgetList.append(Label(self, text='Click here to go to advanced menu.'))
        self.widgetList[16].grid(row=12, column=1, columnspan=2, sticky=W)
        self.widgetList[16].state(["!disabled" if ADVANCED_ENABLE else "disabled"])
        if not ADVANCED_ENABLE:
            self.widgetList[16].grid_remove()

        # Set usage tip binds to widgets
        ## Widget 1: KSDK Path entry
        self.widgetList[1].bind("<Enter>", \
                                lambda h: self.update_tips('Enter a valid KSDK path here.\n\n\n'))
        self.widgetList[1].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))
        ## Widget 2: Browse button
        self.widgetList[2].bind("<Enter>", \
                                lambda h: self.update_tips('Click to browse your computer for a' + \
                                                        ' valid KSDK directory.\n\n\n'))
        self.widgetList[2].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))
        ## Widget 4: Project name entry
        self.widgetList[4].bind("<Enter>", \
                                lambda h: self.update_tips('Enter a name for your project here.' + \
                                                         '\n\n\n' + \
                                                         'NOTE: Currently spaces are not allowed.'))
        self.widgetList[4].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))
        ## Widget 6: Board selection list
        self.widgetList[6].bind("<Enter>", \
                                lambda h: self.update_tips('Select a Freescale development board' +\
                                                         ' from this list.\nYour project will' + \
                                                         ' be configured for this board.\n' + \
                                                         'If you do not wish to use a Freescale' + \
                                                         ' development board, use the ' + \
                                                         '\"Advanced\" menu.\n'))
        self.widgetList[6].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))
        ## Widget 8: Board image and board page link
        self.widgetList[8].bind("<Enter>", \
                                lambda h: self.update_tips('Is this your board?\n' + \
                                                         'If so, then clicking on the board' + \
                                                         ' image will take you to the board' + \
                                                         ' homepage on freescale.com.\n\n'))
        self.widgetList[8].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))
        ## Widget 9: Board image and board page link
        self.widgetList[9].bind("<Enter>", \
                                lambda h: self.update_tips('Launch \"Help\" window.\n\n\n'))
        self.widgetList[9].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))
        ## Widget 10: Button to pop-up help guide
        self.widgetList[10].bind("<Enter>", \
                                lambda h: self.update_tips('Generate the new project.' + \
                                                         '\n\nNOTE: This project will not be a ' + \
                                                         'standalone project.\nTo create a ' + \
                                                         'standalone project use the ' + \
                                                         '\"Advanced\" menu.'))
        self.widgetList[10].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))
        ## Widget 11: Button to launch Advanced menu
        self.widgetList[11].bind("<Enter>", \
                                lambda h: self.update_tips('Launch the \"Advanced\" GUI.\n\n\n'))
        self.widgetList[11].bind("<Leave>", \
                                lambda h: self.update_tips(self.defaultHelp))

        # Poll on user's list selection to display appropriate board preview
        self.poll_selection()

        kT.debug_log(self.localSDK.path)

        return

    def begin_quick_gen(self, master):
        """
        """
        self.widgetList[11].state(["disabled"])
        self.widgetList[10].grid_remove()
        self.widgetList[10] = Progressbar(self, orient='horizontal', mode='determinate')
        self.widgetList[10].grid(row=11, column=4, rowspan=2, columnspan=2, \
                                     sticky=E+W+N+S, pady=(4, 0))
        self.widgetList[10].start(1)
        self.widgetList[10].update_idletasks()

        self.qck_gen_proj(master)

        self.widgetList[10].stop()
        self.widgetList[10].grid_remove()
        if self.newProj.osType == 'Windows':
            style = Style()
            style.configure("Bold.TButton", font='system 8 bold')
            self.widgetList[10] = Button(self, text='Quick Generate!', style="Bold.TButton", \
                                      command=lambda: self.begin_quick_gen(master))
            self.widgetList[10].grid(row=11, column=4, rowspan=2, columnspan=2, \
                                 sticky=E+W+N+S, pady=(4, 0))
        else:
            self.widgetList[10] = Button(self, text='Quick Generate!', \
                                          command=lambda: self.begin_quick_gen(master))
            self.widgetList[10].grid(row=11, column=4, rowspan=2, columnspan=2, \
                                     sticky=E+W+N+S, pady=(4, 0))
        self.widgetList[11].state(["!disabled"])

        return

    def pop_main_boards(self):
        """Method to populate list of boards in main_gui's listbox

        """
        if self.localSDK.brdList:
            del self.localSDK.brdList[:]
        try:
            self.localSDK.get_boards()              # Get list of boards from KSDK manifest file
        except IOError:
            self.localSDK.brdList = ['None']
        self.imageList = []
        count = 0
        # Iterate through board list to get matching images
        while count < len(self.localSDK.brdList):
            # Search for matching board image
            if kImg.boardImages.get(self.localSDK.brdList[count] + '_Thumb.gif'):
                self.imageList.append(kImg.boardImages[self.localSDK.brdList[count] + '_Thumb.gif'])
            # IF we can't find a matching image, set default image
            else:
                self.imageList.append(kImg.boardImages['NoPreview.gif'])
            count += 1
        index = 0
        self.widgetList[6].delete(index, END)             # Clear out the whole listBox
        while index < len(self.localSDK.brdList):
            self.widgetList[6].insert(index, self.localSDK.brdList[index])
            index += 1
        return

    def pop_adv_devices(self):
        """Method to populate list of devices in advanced menu

        """
        if self.localSDK.devList:
            del self.localSDK.devList[:]
        try:
            self.localSDK.get_devices()              # Get list of boards from KSDK manifest file
        except IOError:
            self.localSDK.devList = ['None']
        return

    def poll_selection(self):
        """Method to poll user selection of listbox in order to update image

        """
        osName = platform.system()

        ## Check if the user changed the KSDK_path
        try:
            checkPath = self.widgetList[1].get()
            if checkPath != self.localSDK.path:
                self.ask_set_directory(True, 1)

            ## Check if user updated project name
            checkName = self.widgetList[4].get()
            if checkName != self.newProj.name:
                if kT.check_proj_name(checkName):
                    self.newProj.name = checkName
                else:
                    self.newProj.name = None
                    if self.prevName != checkName:
                        tkMessageBox.showinfo("Invalid Project Name",\
                                          "No spaces or special characters.")
                        self.prevName = checkName
                        kT.debug_log("Invalid name")
        except AttributeError:
            kT.debug_log("Basic Changed menu", sys.exc_info()[2])
            #return

        try:
            now = self.widgetList[6].curselection()
            if now != self.curr:
                if len(self.widgetList[6].curselection()) > 0:
                    try:
                        self.displayBoard = PhotoImage(data=self.imageList[int(now[0])])
                    except IndexError:
                        kT.debug_log(now[0], sys.exc_info()[2])
                    self.widgetList[8].grid_remove()
                    self.widgetList[8] = Button(self, \
                                                image=self.displayBoard, \
                                                command=lambda:\
                                                self.web_launch(self.localSDK.brdList[\
                                                            int(self.widgetList[6].curselection()[0])]))
                    self.widgetList[8].image = self.displayBoard
                    self.widgetList[8].grid(row=5, column=3, columnspan=3, sticky=E+W+N+S)
                    self.widgetList[8].bind("<Enter>", \
                                            lambda h: self.update_tips('Is this your board?\n' + \
                                                                     'If so, ' + \
                                                                     'then clicking on the board' + \
                                                                     ' image will take you to the ' + \
                                                                     'board homepage on ' + \
                                                                     'freescale.com.\n\n'))
                    self.widgetList[8].bind("<Leave>", \
                                            lambda h: self.update_tips(self.defaultHelp))
                self.curr = now
                try:
                    self.currBoard = int(self.widgetList[6].curselection()[0]) + 1
                    # Clear out driver list and board
                    self.newProj.board = ()
                    self.newProj.drvList = []
                    # Configure ksdkProj given GUI state
                    self.localSDK.get_version()
                    self.newProj.name = self.widgetList[4].get()
                    self.newProj.setKsdkPath(self.localSDK.path)
                    self.newProj.sdkVer = self.localSDK.version
                    self.newProj.useBSP = not self.localSDK.isNewVersion()
                except IndexError:
                    self.displayBoard = PhotoImage(data=kImg.boardImages['kds_icon.gif'])
                    self.widgetList[8].config(image=self.displayBoard)
                    self.widgetList[8].image = self.displayBoard
                    self.widgetList[8].config(command=lambda: self.web_launch(kImg.boardImages['NoPreview.gif']))
                    kT.debug_log("Index Error", sys.exc_info()[2])
                    #return
        except IndexError:
            kT.debug_log("Index Error", sys.exc_info()[2])
            #return
        except AttributeError:
            kT.debug_log("AttributeError", sys.exc_info()[2])
            return

        self._retLoop = self.after(250, self.poll_selection)
        
    def _check_project_name(self):
        """
        Check project name
        """
        ## Check if user updated project name
        order = 4 if self.newProj.isQuickGenerate else 3
        checkName = self.widgetList[order].get()
        self.newProj.name = checkName
        if not kT.check_proj_name(checkName):
            tkMessageBox.showinfo("Invalid Project Name","No spaces or special characters or empty name.")
            return False
        return True       

    def ask_set_directory(self, isTyped, widgetIndex):
        """Callback method for browe selection of KSDK directory

        """
        if isTyped == True:
            self.localSDK.setKsdkPath(self.widgetList[widgetIndex].get())
            try:
                if not self.localSDK.isVersionSupported():
                    self.widgetList[6].config(state=DISABLED)
                    self.displayBoard = PhotoImage(data=kImg.boardImages['kds_icon.gif'])
                    self.widgetList[8].config(image=self.displayBoard)
                    self.widgetList[8].image = self.displayBoard
                    self.widgetList[8].config(command=lambda: self.web_launch(kImg.boardImages['NoPreview.gif']))
                    self.widgetList[10].state(["disabled"])
                    self.widgetList[11].state(["disabled"])
                    raise ValueError('This version of KSDK is not supported', self.localSDK.version)
                else:
                    self.widgetList[6].config(state=NORMAL)
                    self.widgetList[10].state(["!disabled"])
                    if not 'PREVIEW' in PGKSDK_VERSION:
                        self.widgetList[11].state(["!disabled"])
                    kT.update_json_file(self.settingsPath, "ksdkPath", self.localSDK.path)
            except IOError:
                self.widgetList[8].config(image=self.displayBoard)
                self.widgetList[8].image = self.displayBoard
                self.widgetList[8].config(command=lambda: self.web_launch(kImg.boardImages['NoPreview.gif']))
                kT.debug_log("Entering Text", sys.exc_info()[2])
            except ValueError as err:
                tkMessageBox.showinfo("Error", \
                                      'KSDK ' + \
                                      self.localSDK.version + \
                                      ' is not supported by this tool.')
                kT.debug_log(err.args, sys.exc_info()[2])
        else:
            self.localSDK.setNewKSDKPath(tkFileDialog.askdirectory(**self.dir_opt))
            if self.localSDK.path != '':
                self.widgetList[widgetIndex].delete(0, END)
                self.widgetList[widgetIndex].insert(0, self.localSDK.path)
            else:
                return
            kT.debug_log(self.localSDK.path)
            try:
                if not self.localSDK.isVersionSupported():
                    self.widgetList[6].config(state=DISABLED)
                    self.displayBoard = PhotoImage(data=kImg.boardImages['kds_icon.gif'])
                    self.widgetList[8].config(image=self.displayBoard)
                    self.widgetList[8].image = self.displayBoard
                    self.widgetList[8].config(command=lambda: self.web_launch(kImg.boardImages['NoPreview.gif']))
                    self.widgetList[10].state(["disabled"])
                    self.widgetList[11].state(["disabled"])
                    raise ValueError('This version of KSDK is not supported', self.localSDK.version)
                else:
                    self.widgetList[6].config(state=NORMAL)
                    self.widgetList[10].state(["!disabled"])
                    if not 'PREVIEW' in PGKSDK_VERSION:
                        self.widgetList[11].state(["!disabled"])
                    kT.update_json_file(self.settingsPath, "ksdkPath", self.localSDK.path)
            except IOError:
                tkMessageBox.showinfo("Error", \
                                      "No manifest file present." + \
                                      "\nSelect a valid KSDK installation.")
                kT.debug_log("No manifest file present.", sys.exc_info()[2])
            except ValueError as err:
                tkMessageBox.showinfo("Error", \
                                      'KSDK ' + \
                                      self.localSDK.version + \
                                      ' is not supported by this tool.')
                kT.debug_log(err.args, sys.exc_info()[2])
        self.pop_main_boards()
        return

    def proj_set_directory(self, isTyped, widgetIndex):
        """Callback method for browe selection of directory

        """
        if isTyped == True:
            newPath = self.widgetList[widgetIndex].get()
        else:
            newPath = tkFileDialog.askdirectory(**self.dir_opt)
            kT.debug_log('New path: ' + newPath)
            if newPath != '':
                self.widgetList[widgetIndex].delete(0, END)
                self.widgetList[widgetIndex].insert(0, newPath)
        return

    def pop_up_help(self, master, helpText):
        """Callback function for 'Help' button to provide a brieft user guide and links to websites

        :param master: Tkinter object
        :param helpText: Text string to be displayed in pop-up window
        """
        osName = platform.system()
        popHelp = Toplevel()
        popHelp.grid()
        winH = 0
        winW = 0
        if osName == 'Windows':
            winH = 150 * WIN_SCALE
            winW = 335 * WIN_SCALE
        elif osName == 'Darwin':
            if platform.mac_ver()[0][:5] == '10.10':
                winH = 150
                winW = 400
            elif  platform.mac_ver()[0][:5] == '10.11':
                winH = 150
                winW = 460
        else:
            winH = 150
            winW = 390
        popHelp.config(height=winH , width=winW)
        if osName == 'Linux':
            img = Image("photo", data=kImg.boardImages['kds_icon.gif']) # Use the .gif in Linux
            popHelp.tk.call('wm', 'iconphoto', popHelp._w, img)
        popHelp.title(PGKSDK_NAME + " Help")
        popHelp.geometry('%dx%d+%d+%d' % (winW, winH, master.winfo_x() + 20, master.winfo_y() + 20))
        popHelp.resizable(width=FALSE, height=FALSE)
        popHelp.configure(background='#E7E7E7')
        ## Get selected board name, or set name if no boad selected
        try:
            currBrd = self.localSDK.brdList[int(self.widgetList[6].curselection()[0])]
        except IndexError:
            currBrd = 'KSDK'

        ## If a board is selected add it to the help string
        if currBrd != 'KSDK':
            helpText = helpText + '\n' + currBrd + ' selected.'

        helpTxt = Label(popHelp, text=helpText, justify=LEFT)
        helpTxt.grid(row=0, column=0, rowspan=5, columnspan=2, padx=5, pady=5)
        if currBrd != 'KSDK':
            helpLnk = Button(popHelp, \
                             text='Go to ' + currBrd + ' website', \
                             command=lambda: self.web_launch(currBrd))
            helpLnk.grid(row=6, column=0, sticky=W, padx=(5, 0))
        ksdkLnk = Button(popHelp, \
                         text='Go to KSDK website', \
                         command=lambda: self.web_launch('KSDK'))
        ksdkLnk.grid(row=6, column=1, sticky=E, padx=(0, 5))

    @staticmethod
    def web_launch(boardName):
        """Callback method to launch freescale.com webpage for selected board or KSDK

        :param boardName: String of board that has been selected.

        :todo::

            Put correct URL for tool location
        """
        kT.debug_log(len(boardName))

        if boardName == 'TWR-KW24D512':
            webLink = 'http://www.freescale.com/TWR-KW2x'
        elif boardName == 'USB-KW40Z-K22F':
            webLink = 'http://www.freescale.com/USB-KW40Z'
        elif (boardName == 'MRB-KW019030JA')\
          or (boardName == 'MRB-KW019032EU')\
          or (boardName == 'MRB-KW019032NA'):
            webLink = 'http://www.freescale.com/MRB-KW0x'
        elif len(boardName) > 1000:
            webLink = 'http://www.freescale.com/'
        else:
            webLink = 'http://www.freescale.com/' + boardName
        webbrowser.open_new(webLink)
        return

    def qck_gen_proj(self, master):
        """Callback method to generate project, tell user where the project is now located,
           and open folder.

        :param master: Tkinter object
        """
        if not self._check_project_name():
            return

        # Clear out driver list and board
        self.newProj.board = ()
        self.newProj.drvList = []

        # Configure ksdkProj given GUI state
        self.localSDK.get_version()
        self.newProj.name = self.widgetList[4].get()
        self.newProj.setKsdkPath(self.localSDK.path)
        self.newProj.sdkVer = self.localSDK.version
        self.newProj.useBSP = not self.localSDK.isNewVersion()

        # Add the board
        try:
            userBoard = int(self.widgetList[6].curselection()[0]) + 1
            self.newProj.add_board(userBoard, self.localSDK.brdList)
        except IndexError:
            tkMessageBox.showinfo("No board selected!",\
                                  "Make sure a board has been selected.")
            return

        self.widgetList[10].step(30)
        self.widgetList[10].update_idletasks()

        # Quick check to see if this poject already exists
        checkPath = self.newProj.sdkPath + '/' + self.newProj.parent.getDirectoryStructureHelper().getUserLinkedExamplesPath(self.newProj.board[1]) + '/' + self.newProj.name
        if os.path.isdir(checkPath):
            tkMessageBox.showinfo("Project exists",\
                                  "A project by this name already exists.")
            return

        # in quick mode there is always generated the board project
        self.newProj.isBoardProject = True
        
        # Add all drivers for this device
        self.localSDK.get_drivers()
        maskRet = kT.mask_features(kTool.KsdkTools(), self.newProj.sdkPath, self.newProj.sdkVer, \
                                     self.localSDK.drvList, self.newProj.device[1], self.newProj.device[2])
        self.newProj.portCount = maskRet[0]
        self.newProj.dmaCount = maskRet[1]
        self.newProj.tsiVersion = maskRet[2]
        self.newProj.add_all_drv(self.localSDK.drvList)

        kT.debug_log('Port Count: ' + str(self.newProj.portCount))

        #Generate IAR project files
        #self.newProj.fast_build_IAR()
        self.newProj.workSpace = self.newProj.sdkPath + '/' + self.newProj.parent.getDirectoryStructureHelper().getUserLinkedExamplesPath(self.newProj.board[1]) + '/'
        projectPath = self.newProj.workSpace + self.newProj.name

        #Get all include paths lists into one list
        includeList = []
        index = 0
        isPresent = False
        while index < len(self.newProj.drvList):
            count = 0
            while count < len(self.newProj.drvList[index][2]):
                isPresent = False
                newPath = str(\
                         self.newProj.drvList[index][2][count]\
                             )
                if len(includeList) > 0:
                    listIndex = 0
                    while listIndex < len(includeList):
                        if newPath == includeList[int(listIndex) - 1]:
                            isPresent = True
                        listIndex += 1
                if not isPresent:
                    includeList.append(newPath)
                count += 1
            index += 1

        self.newProj.libList.append('platform')
        if not os.path.isdir(projectPath):
            os.makedirs(projectPath)
        self.newProj.rtos = 'bm'

        if not os.path.isfile(projectPath + '/main.c'):
            self.newProj.make_main_file(projectPath, includeList)
        if not os.path.isfile(projectPath + '/hardware_init.c'):
            self.newProj.make_hw_file(projectPath)

        self.widgetList[10].step(30)
        self.widgetList[10].update_idletasks()

        ## Copy over BSP files
        if self.newProj.useBSP:
            if not os.path.isdir(projectPath + '/board'):
                os.mkdir(projectPath + '/board')
            bspDir = self.newProj.sdkPath + '/examples/' + self.newProj.board[1]
            bspList = kT.list_files(bspDir)
            for f in bspList:
                if f[-2:] == '.c':
                    shutil.copyfile(bspDir + '/' + f, projectPath + '/board/' + f)
                if f[-2:] == '.h':
                    shutil.copyfile(bspDir + '/' + f, projectPath + '/board/' + f)

        if self.localSDK.isToolchainTypeSupported(kSdk.ToolchainType.IARname, self.newProj.device):
            print self.newProj.isLinked
            if self.localSDK.isNewVersion():
                newIar = kIarNew.KsdkIarNew(self.newProj)
            else:
                newIar = kIar.KsdkIar(self.newProj)
            newIar.gen_ewp(self.newProj)
            newIar.gen_eww(self.newProj)

        if self.localSDK.isToolchainTypeSupported(kSdk.ToolchainType.KeilMDK, self.newProj.device):
            #Generate MDK project files
            if self.localSDK.isNewVersion():
                newMdk = kMdkNew.KsdkMdkNew(self.newProj)
            else:
                newMdk = kMdk.KsdkMdk(self.newProj)
            newMdk.gen_proj(self.newProj)
            newMdk.gen_wkspace(self.newProj)

        if self.localSDK.isToolchainTypeSupported(kSdk.ToolchainType.KinetisDesignStudio, self.newProj.device):
            #Generate KDS project fiels
            print self.newProj.isLinked
            if self.localSDK.isNewVersion():
                newKds = kKdsNew.KsdkKdsNew(self.newProj)
            else:
                newKds = kKds.KsdkKds(self.newProj)

            newKds.gen_cproject(self.newProj)
            newKds.gen_project(self.newProj)
            newKds.gen_working_set(self.newProj)
            newKds.gen_debug(self.newProj)

        if self.localSDK.isToolchainTypeSupported(kSdk.ToolchainType.AtollicStudio, self.newProj.device):
            #Generate ATL project files
            if self.localSDK.isNewVersion():
                newAtl = kAtlNew.KsdkAtlNew(self.newProj)
            else:
                newAtl = kAtl.KsdkAtl(self.newProj)
            newAtl.gen_cproject(self.newProj)
            newAtl.gen_project(self.newProj)
            newAtl.gen_debug(self.newProj)
            newAtl.gen_settings(self.newProj)

        if self.localSDK.isToolchainTypeSupported(kSdk.ToolchainType.ARMgcc):
            #Generate GCC project files
            if not self.newProj.fast_build_GCC():
                tkMessageBox.showinfo("Missing CMake Files",\
                                      "CMake files are missing from your KSDK installation.")

        #Text for window
        genString = 'Your project was created in the following location:\n'
        pathString = ''
        pathString += self.newProj.sdkPath + '/' + self.newProj.parent.getDirectoryStructureHelper().getUserLinkedExamplesPath( self.newProj.board[1]) + '/' + self.newProj.name + '/'
        genString += pathString
        genString += '\nPress the button below to open project location folder.'

        #Create window to show USER that project has been generated and where it is.
        popGen = Toplevel()
        if self.newProj.osType == 'Windows':
            winH = 100 * WIN_SCALE
            winW = 600 * WIN_SCALE
        elif self.newProj.osType == 'Darwin':
            if platform.mac_ver()[0][:5] == '10.10':
                winH = 100
                winW = 600
            elif  platform.mac_ver()[0][:5] == '10.11':
                winH = 100
                winW = 660
        else:
            winH = 100
            winW = 600
        popGen.config(height=winH, width=winW)
        popGen.grid()
        if self.newProj.osType == 'Linux':
            img = Image("photo", data=kImg.boardImages['kds_icon.gif']) # Use the .gif in Linux
            popGen.tk.call('wm', 'iconphoto', popGen._w, img)
        popGen.title("Project created")
        popGen.geometry('%dx%d+%d+%d' % (winW, winH, master.winfo_x() + 20, master.winfo_y() + 20))
        popGen.resizable(width=FALSE, height=FALSE)
        popGen.configure(background='#E7E7E7')

        genTxt = Label(popGen, text=genString, justify=LEFT)
        genTxt.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        #Create button to open project folder
        ## IF we are in windows, we need to replace all '/' with '\\'
        tempString = pathString[:]
        if self.newProj.osType == 'Windows':
            pathString = ''
            pathString = kT.string_replace(tempString, '/', '\\')

        genButton = Button(popGen, text='Open Project Folder', command=lambda: self.view_project(pathString, popGen))
        genButton.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        self.widgetList[10].step(35)
        self.widgetList[10].update_idletasks()

        # patch to implement automation test
        self.pop_gen = popGen

        return

    def advanced_gui(self, master):
        """Callback method to launch Advanced options menu

        :param master: Tkinter object
        """

        # Turn off polling function
        self.newProj.isQuickGenerate = False
        self._retLoop = None

        #Remove active widgets from the screen and then clear widget list out
        if self.widgetList:
            for w in self.widgetList:
                w.grid_remove()
            del self.widgetList[:]

        osName = platform.system()

        if osName != 'Darwin':
            labelFont = 'Arial 9 bold'
        else:
            labelFont = 'bold'

        ### Widget 0 is a label for padding column 0
        self.widgetList.append(Label(self, text=''))
        self.widgetList[0].grid(row=0, column=0, sticky=E+W, padx=5)

        ### Widget 1 is a button to return to simple menu
        self.widgetList.append(Button(self, text='Return', \
                                      command=lambda: self.launch_basic(master)))
        self.widgetList[1].grid(row=16, column=1, sticky=W)

        ### Widget 2 is a label for the project name text field
        self.widgetList.append(Label(self, text='Project Name: ', font=labelFont))
        self.widgetList[2].grid(row=0, column=1, sticky=W, pady=(5, 0))

        ### Widget 3 is the text field for project name entry
        self.widgetList.append(Entry(self, width=25))
        self.widgetList[3].insert(0, self.newProj.name)
        self.widgetList[3].grid(row=1, column=1, sticky=W, pady=(0, 0))

        ### Widget 4 is the label for project type
        self.widgetList.append(Label(self, text='Project Type:', font=labelFont))
        self.widgetList[4].grid(row=2, column=1, sticky=W, pady=(5, 0))

        ### Widget 5 is a radio button for configuring a new project
        self.widgetList.append(Radiobutton(self, text='New', variable=self.advancedProjType, \
                                           value=0))
        self.widgetList[5].grid(row=3, column=1, sticky=W)

        ### Widget 6 is a radio button for configuring a cloned project
        self.widgetList.append(Radiobutton(self, text='Clone', variable=self.advancedProjType, \
                                           value=1))
        self.widgetList[6].grid(row=3, column=1, sticky=E)

        ### Widget 7 is the label for the device drop down menu
        self.widgetList.append(Label(self, text='Device:', font=labelFont))
        self.widgetList[7].grid(row=0, column=3, sticky=W, pady=(5, 0))

        ### Widget 8 is te drop down menu for the devices
        self.pop_adv_devices()
        #self.widgetList.append(OptionMenu(self, userDev, *self.localSDK.devList))
        self.widgetList.append(Combobox(self, state='readonly'))
        self.widgetList[8].config(textvariable=self.advDevSelect)
        self.widgetList[8]['values'] = self.localSDK.devList
        self.widgetList[8].grid(row=1, column=3, sticky=W, pady=(0, 0))
        try:
            self.newProj.add_board(self.currBoard, self.localSDK.brdList)
            self.widgetList[8].current(self.localSDK.devList.index(self.newProj.device[0]))
        except IOError:  ## Catch the case where the user hasn't selected anything
            self.widgetList[8].current(0)
        except ValueError:  ## Catch the case where there is no device given in manifest
            self.widgetList[8].current(0)

        ### Widget 9 is a label for the library configuration radio buttons
        libraryConfigurationWidget = Label(self, text='Library Configuration:', font=labelFont)
        self.widgetList.append(libraryConfigurationWidget)
        self.widgetList[9].grid(row=4, column=1, sticky=W, columnspan=2)

        ### Widget 10 is a radio button for the library configuration
        halOnlyWidget = Radiobutton(self, text='HAL only', variable=self.advancedLibType,value=0)
        self.widgetList.append(halOnlyWidget)
        self.widgetList[10].grid(row=6, column=1, sticky=W)

        ### Widget 11 is a radio button for the library configuration
        platformWidget = Radiobutton(self, text='Platform', variable=self.advancedLibType, value=1)
        self.widgetList.append(platformWidget)
        self.widgetList[11].grid(row=5, column=1, sticky=W)

        # Set default to select platform library
        self.advancedLibType.set(1)
        
        # in new version there is not hal vs. platform
        if self.localSDK.isNewVersion():
            libraryConfigurationWidget.grid_remove()
            halOnlyWidget.grid_remove()
            platformWidget.grid_remove()

        ### Widget 12 is a label for the library configuration radio buttons
        self.widgetList.append(Label(self, text='RTOS Configuration:', font=labelFont))
        self.widgetList[12].grid(row=7, column=1, sticky=W, columnspan=2)

        ### Widget 13 is a radio button for the library configuration
        self.widgetList.append(Radiobutton(self, text='None', variable=self.advancedRtosType, \
                                           value=0))
        self.widgetList[13].grid(row=8, column=1, sticky=W)

        ### Widget 14 is a radio button for the library configuration
        mqxWidget = Radiobutton(self, text='MQX', variable=self.advancedRtosType, value=1)
        self.widgetList.append(mqxWidget)
        mqxWidget.grid(row=9, column=1, sticky=W)

        # in KSDK 2.0 and newer version there is no MQX support so the MQX option has to be removed
        # in some older version of KSDK (1.2, 1.3) MQX support is missing so this option has to be removed
        if not self.localSDK.isMQXSupported():
            mqxWidget.grid_remove()


        ### Widget 15 is a radio button for the library configuration
        freeRTOSWidget = Radiobutton(self, text='FreeRTOS', variable=self.advancedRtosType, value=2)
        self.widgetList.append(freeRTOSWidget)
        freeRTOSWidget.grid(row=10, column=1, sticky=W)
        # if FreeRTOS is not supported in KSDK option should be removed
        if not self.localSDK.isFreeRTOSSupported():
            freeRTOSWidget.grid_remove()

        ### Widget 16 is a radio button for the library configuration
        uCOSIIWidget = Radiobutton(self, text='uC/OS-II', variable=self.advancedRtosType, value=3)
        self.widgetList.append(uCOSIIWidget)
        uCOSIIWidget.grid(row=11, column=1, sticky=W)
        if not self.localSDK.isuCOSIISupported():
            uCOSIIWidget.grid_remove()

        ### Widget 17 is a radio button for the library configuration
        uCOSIIIWidget = Radiobutton(self, text='uC/OS-III', variable=self.advancedRtosType, value=4)
        self.widgetList.append(uCOSIIIWidget)
        uCOSIIIWidget.grid(row=12, column=1, sticky=W)
        if not self.localSDK.isuCOSIIISupported():
            uCOSIIIWidget.grid_remove()

        ### Widget 18 is a label for the toolchain check boxes
        self.widgetList.append(Label(self, text='Choose Supported Toolchain(s):', font=labelFont))
        self.widgetList[18].grid(row=4, column=3, sticky=W, columnspan=2)

        ### Widget 19 is a check box for KDS
        kdsOptionWidget = Checkbutton(self, text=kSdk.KDSname, variable=self.advIsKds)
        self.widgetList.append(kdsOptionWidget)
        self.widgetList[19].grid(row=5, column=3, sticky=W, columnspan=2)

        ### Widget 20 is a check box for IAR
        iarOptionWidget = Checkbutton(self, text=kSdk.IARname, variable=self.advIsIar)
        self.widgetList.append(iarOptionWidget)
        self.widgetList[20].grid(row=6, column=3, sticky=W, columnspan=2)

        ### Widget 21 is a check box for MDK
        keilMdkOptionWidget = Checkbutton(self, text=kSdk.keilMDKARMname, variable=self.advIsMdk)
        self.widgetList.append(keilMdkOptionWidget)
        self.widgetList[21].grid(row=7, column=3, sticky=W, columnspan=2)

        ### Widget 22 is a check box for ATS
        atollicOptionWidget = Checkbutton(self, text=kSdk.AtollicStudio, variable=self.advIsAts)
        self.widgetList.append(atollicOptionWidget)
        self.widgetList[22].grid(row=8, column=3, sticky=W, columnspan=2)

        if not self.localSDK.isToolchainTypeSupported(ToolchainType.KinetisDesignStudio):
            kdsOptionWidget.grid_remove()
        if not self.localSDK.isToolchainTypeSupported(ToolchainType.IARname):
            iarOptionWidget.grid_remove()
        if not self.localSDK.isToolchainTypeSupported(ToolchainType.KeilMDK):
            keilMdkOptionWidget.grid_remove()
        if not self.localSDK.isToolchainTypeSupported(ToolchainType.AtollicStudio):
            atollicOptionWidget.grid_remove()

        ### Widget 23 is a check box for GCC
        self.widgetList.append(Checkbutton(self, text='GCC Command Line', variable=self.advIsGcc))
        self.widgetList[23].grid(row=9, column=3, sticky=W, columnspan=2)
        self.widgetList[23].state(["disabled"])
        self.widgetList[23].grid_remove()

        ### Widget 24 is a label for adding BSP
        #self.widgetList.append(Label(self, text='USB and Board Support:', font=labelFont))
        boardSupportLabel = Label(self, text='Board Support:', font=labelFont)
        self.widgetList.append(boardSupportLabel)
        self.widgetList[24].grid(row=10, column=3, sticky=W, columnspan=2, pady=(5, 0))

        ### Widget 25 is a checkbox for adding BSP
        includeBSPFilesOption = Checkbutton(self, text='Include BSP files', variable=self.advIsBsp)
        self.widgetList.append(includeBSPFilesOption)
        self.widgetList[25].grid(row=11, column=3, sticky=W, columnspan=2)
        self.widgetList[25].state(["!disabled"])
        
        if self.localSDK.isNewVersion():
            boardSupportLabel.grid_remove()
            includeBSPFilesOption.grid_remove()

        ### Widget 26 is a label for the output path entry
        self.widgetList.append(Label(self, text='Project Parent Directory:', \
                                                font=labelFont))
        self.widgetList[26].grid(row=13, column=1, sticky=W, columnspan=4, pady=(5, 0))

        ### Widget 27 is a text entry for the output path
        if self.newProj.osType == 'Windows':
            entryWidth = int(77.0 / WIN_SCALE)
            self.widgetList.append(Entry(self, width=entryWidth))
        else:
            self.widgetList.append(Entry(self, width=71))
        self.newProj.workSpace = self.newProj.sdkPath 
        if self.newProj.osType == 'Windows':
            self.newProj.workSpace = kT.string_replace(self.newProj.workSpace, '/', '\\')
        self.widgetList[27].insert(0, self.newProj.workSpace)
        self.widgetList[27].grid(row=14, column=1, sticky=W, columnspan=4)

        ### Widget 28 is a button for browsing to a directory
        self.dir_opt['title'] = 'Select the directory you want the project to be generated into. '
        self.widgetList.append(Button(self, text='Browse', \
                                      command=lambda: self.proj_set_directory(False, 27)))
        if self.newProj.osType == 'Windows':
            self.widgetList[28].grid(row=14, column=5, sticky=E)
        else:
            self.widgetList[28].grid(row=14, column=4, sticky=E)

        self.widgetList[28].state(["disabled"])

        ### Widget 29 is a checkbox for making a standalone project
        self.widgetList.append(Checkbutton(self, text='Generate standalone project', \
                                           variable=self.advIsStandalone))
        self.widgetList[29].grid(row=15, column=1, sticky=W, columnspan=2, pady=5)

        ### Widget 30 is a help button
        self.widgetList.append(Button(self, text='Help', \
                                      command=lambda: self.advanced_help(master, (Constants.ADV_HELP if self.localSDK.isNewVersion() else ADV_HELP))))
        if self.newProj.osType == 'Windows':
            self.widgetList[30].grid(row=1, column=5, sticky=E, pady=(0, 0))
        else:
            self.widgetList[30].grid(row=1, column=4, sticky=E, pady=(0, 0))
        #self.widgetList[30].state(["disabled"])

        ### Widget 31 is a button to generate the project
        if self.newProj.osType == 'Windows':
            style = Style()
            style.configure("Bold.TButton", font='system 8 bold')
            self.widgetList.append(Button(self, text='Advanced Generate!', style="Bold.TButton", \
                                          command=lambda: self.package_select(master)))
            self.widgetList[31].grid(row=16, column=4, sticky=E+W+N+S, rowspan=2, columnspan=2)
        else:
            self.widgetList.append(Button(self, text='Advanced Generate!',\
                                          command=lambda: self.package_select(master)))
            self.widgetList[31].grid(row=16, column=3, sticky=E+N+S, rowspan=2, columnspan=2)
        self.widgetList[31].state(["!disabled"])

        ### Widget 32 is a label for padding row 13
        self.widgetList.append(Label(self, text='', font=labelFont))
        self.widgetList[32].grid(row=0, column=6, sticky=E+W, padx=5)

        ### Widget 33 is a label for explaining the return button
        self.widgetList.append(Label(self, text='Click here to return to previous menu.'))
        self.widgetList[33].grid(row=17, column=1, columnspan=3, sticky=W)

        ### Widget 34 is a checkbox for adding USB
        self.widgetList.append(Checkbutton(self, text='Include USB', variable=self.advIsUsb))
        self.widgetList[34].grid(row=12, column=3, sticky=W, columnspan=2)
        self.widgetList[34].state(["disabled"])
        self.widgetList[34].grid_remove()

        ### Widget 35 is a radio button for configuring a new project
        self.widgetList.append(Radiobutton(self, text='Device', variable=self.advancedDevType, \
                                           value=0))
        self.widgetList[35].grid(row=3, column=3, sticky=W)

        ### Widget 36 is a radio button for configuring a cloned project
        self.widgetList.append(Radiobutton(self, text='Board', variable=self.advancedDevType, \
                                           value=1))
        self.widgetList[36].grid(row=3, column=3, sticky=E)

        ### Widget 37 is the label for project type
        self.widgetList.append(Label(self, text='Device or Board:', font=labelFont))
        self.widgetList[37].grid(row=2, column=3, sticky=W, pady=(5, 0))

        self.poll_advanced()
        
        #update project to set correct supported tools, path etc.
        self.update_proj()
        return

    def update_tips(self, usageText):
        """Callback method to display help text when user hovers over a widget

        :param usageText: Text string to be displayed in GUI
        """
        try:
            self.widgetList[13].config(text=usageText, justify=LEFT)
        except TclError:
            kT.debug_log("Changed menu", sys.exc_info()[2])
        return

    def poll_advanced(self):
        """Method to poll user selection of advanced menu in order to update

        """
        osName = platform.system()

        ## Check if user updated project name
        try:
            ## Check if user updated project name
            checkName = self.widgetList[3].get()
            if checkName != self.newProj.name:
                if kT.check_proj_name(checkName):
                    self.newProj.name = checkName
                else:
                    self.newProj.name = None
                    if self.prevName != checkName:
                        tkMessageBox.showinfo("Invalid Project Name",\
                                          "No spaces or special characters.")
                        self.prevName = checkName
                        kT.debug_log("Invalid name")
        except AttributeError:
            kT.debug_log("AttributeError", sys.exc_info()[2])
            return

        self._retLoop = self.after(250, self.poll_advanced)

    def launch_basic(self, master):
        """ Show warning that the other menu will not build based on the settings
            in the advanced menu.
        """
        self.newProj.isQuickGenerate = True
        osName = platform.system()
        if self.showWarning.get() == 0:
            popHelp = Toplevel()
            popHelp.grid()
            winH = 0
            winW = 0
            if osName == 'Windows':
                winH = 135 * WIN_SCALE
                winW = 220 * WIN_SCALE
            elif self.newProj.osType == 'Darwin':
                if platform.mac_ver()[0][:5] == '10.10':
                    winH = 135
                    winW = 250
                elif  platform.mac_ver()[0][:5] == '10.11':
                    winH = 135
                    winW = 270
            else:
                winH = 135
                winW = 250
            popHelp.config(height=winH, width=winW)
            if osName == 'Linux':
                img = Image("photo", data=kImg.boardImages['kds_icon.gif']) # Use the .gif in Linux
                popHelp.tk.call('wm', 'iconphoto', popHelp._w, img)
            popHelp.title("Attention!")
            popHelp.geometry('%dx%d+%d+%d' % \
                             (winW, winH, master.winfo_x() + 150, master.winfo_y() + 150))
            popHelp.resizable(width=FALSE, height=FALSE)
            popHelp.configure(background='#E7E7E7')
            helpText = 'You are leaving the advanced menu.' + \
                       '\nBuilding from the basic menu will not' + \
                       '\ninclude the selected advanced options.\n' +\
                       'Are you sure you want to proceed?'
            helpTxt = Label(popHelp, text=helpText, foreground='red', justify=CENTER)
            helpTxt.grid(row=0, column=0, pady=5, padx=5)
            helpLnk = Button(popHelp, \
                             text='Yes', \
                             command=lambda: self.close_and_run(master, popHelp))
            helpLnk.grid(row=1, column=0, sticky=W, pady=5, padx=(5, 0))
            ksdkLnk = Button(popHelp, \
                             text='No', \
                             command=popHelp.destroy)
            ksdkLnk.grid(row=1, column=0, sticky=E, pady=5, padx=(0, 5))
            notAgain = Checkbutton(popHelp, \
                                   text='Do not show me again.', \
                                   variable=self.showWarning, \
                                   underline=0)
            if self.showWarning.get() == 1:
                notAgain.select()
            notAgain.grid(row=2, column=0, sticky=W, padx=5)
        else:
            self.main_gui(master)

    def close_and_run(self, master, window):
        """ Call main GUI and destroy the pop-up.
        """
        self.main_gui(master)
        window.destroy()

    def begin_advanced_gen(self, master, window):
        """
        """

        if window != None:
            window.destroy()

        self.widgetList[1].state(["disabled"])
        self.widgetList[31].grid_remove()
        self.widgetList[31] = Progressbar(self, orient='horizontal', mode='determinate')
        self.widgetList[31].grid(row=16, column=3, sticky=E+W+N+S, rowspan=2, columnspan=4)
        self.widgetList[31].start()
        self.widgetList[31].update()

        kT.debug_log('Advanced build')
        if self.advancedDevType.get():
            if self.update_proj():
                self.isValidConfig.set(1)
            else:
                self.isValidConfig.set(0)
        self.build_advanced(master)

        self.widgetList[31].stop()
        self.widgetList[31].grid_remove()
        if self.newProj.osType == 'Windows':
            style = Style()
            style.configure("Bold.TButton", font='system 8 bold')
            if self.advancedProjType.get():
                self.widgetList[31] = Button(self, text='Advanced Generate!', style="Bold.TButton", \
                                         command=lambda: self.begin_advanced_gen(master, None))
            else:
                if self.advancedDevType.get():
                    self.widgetList[31] = Button(self, text='Advanced Generate!', style="Bold.TButton", \
                                             command=lambda: self.begin_advanced_gen(master, None))
                else:
                    self.widgetList[31] = Button(self, text='Advanced Generate!', style="Bold.TButton", \
                                             command=lambda: self.package_select(master))
            self.widgetList[31].grid(row=16, column=4, sticky=E+W+N+S, rowspan=2, columnspan=2)
        else:
            if self.advancedProjType.get():
                self.widgetList[31] = Button(self, text='Advanced Generate!',\
                                           command=lambda: self.begin_advanced_gen(master, None))
            else:
                if self.advancedDevType.get():
                    self.widgetList[31] = Button(self, text='Advanced Generate!', \
                                             command=lambda: self.begin_advanced_gen(master, None))
                else:
                    self.widgetList[31] = Button(self, text='Advanced Generate!', \
                                             command=lambda: self.package_select(master))
            self.widgetList[31].grid(row=16, column=3, sticky=E+N+S, rowspan=2, columnspan=2)
        self.widgetList[1].state(["!disabled"])
        return

    def build_advanced(self, master):
        """ Build project based on advanced settings.
        """
        self.newProj.isBoardProject = self.advancedDevType.get() != 0
        self.widgetList[31].state(["!disabled"])

        if not self._check_project_name():
            return

        self.widgetList[31].step(1)
        self.widgetList[31].update_idletasks()
        clonedProjectRoot = ''
        if self.advancedProjType.get():
            ## Clone selected project\
            cloneName = self.widgetList[36].get()

            # Add the board
            userBoard = self.localSDK.brdList.index(self.advBrdSelect.get()) + 1
            self.newProj.add_board(userBoard, self.localSDK.brdList)
            ##print self.newProj.board

            sourcePath = ''

            self.widgetList[31].step(1)
            self.widgetList[31].update_idletasks()

            if self.advIsStandalone.get():
                kT.debug_log('Standalone')
                self.newProj.isLinked = False
                ## Check if user updated project name
                checkName = self.widgetList[27].get()
                if checkName != self.newProj.workSpace:
                    if kT.check_wksp_name(checkName):
                        self.newProj.workSpace = checkName
                    else:
                        self.newProj.workSpace = None
                        if self.prevWksp != checkName:
                            tkMessageBox.showinfo("Invalid Output Path",\
                                              "Permitted characters: 0-9a-zA-Z_ :\\/-.")
                            self.prevWksp = checkName
                            kT.debug_log("Invalid name")
                            return False
                self.localSDK.get_drivers()
                maskRet = kT.mask_features(kTool.KsdkTools(), self.newProj.sdkPath, self.newProj.sdkVer, \
                                                             self.localSDK.drvList, self.newProj.device[1], self.newProj.device[2])
                self.newProj.portCount = maskRet[0]
                self.newProj.dmaCount = maskRet[1]
                self.newProj.tsiVersion = maskRet[2]
                self.newProj.add_all_drv(self.localSDK.drvList)

                self.widgetList[31].step(1)
                self.widgetList[31].update_idletasks()

                self.localSDK.get_hal()
                maskRet = kT.mask_features(kTool.KsdkTools(), self.newProj.sdkPath, self.newProj.sdkVer, \
                                                          self.localSDK.halList, self.newProj.device[1], self.newProj.device[2])
                self.newProj.portCount = maskRet[0]
                self.newProj.dmaCount = maskRet[1]
                self.newProj.tsiVersion = maskRet[2]
                self.newProj.add_all_hal(self.localSDK.halList)

                self.widgetList[31].step(1)
                self.widgetList[31].update_idletasks()

                sourcePath = self.newProj.workSpace
            else:
                sourcePath = self.newProj.sdkPath + '/' + self.newProj.parent.getDirectoryStructureHelper().getUserLinkedExamplesPath(self.newProj.board[1])
            
            self.newProj.workSpace = sourcePath
            cloneCheck = self.newProj.proj_clone(cloneName, self)
            if cloneCheck != True:
                if cloneCheck == False:
                    tkMessageBox.showinfo(Texts.PROJECT_EXIST_HEADER, Texts.PROJECT_EXIST_TEXT)
                    return
                else:
                    tkMessageBox.showinfo("Error!","An exception has occured, please restart the tool.")
                    sys.exit()
                    return

            self.widgetList[31].step(5)
            self.widgetList[31].update_idletasks()

            kT.debug_log('Clone')
        else:
            ## Build a new project from scratch
            if len(self.newProj.toolChain) < 1:
                tkMessageBox.showinfo("No Toolchain Selected",\
                                              "Select a toolchain to generate a project.")
                return

            if self.newProj.rtos != 'bm':
                if self.newProj.rtos == 'mqx':
                    if (self.newProj.device[1][1:] in MQX_DEVICES):
                        pass
                    else:
                        tkMessageBox.showinfo("Invalid selection",\
                                              "RTOS support not available at this time for "+ self.newProj.board[3] + ".")
                        return
                else:
                    #FIXME Radka add special detection based on RAM size (from manifest) for KSDK 2.0
                    if not self.localSDK.isNewVersion():
                        if self.newProj.device[1][1:] in RTOS_DEVICES:
                            pass
                        else:
                            tkMessageBox.showinfo("Invalid selection", "RTOS support not available at this time for "+ self.newProj.board[3] + ".")
                            return
            if self.isValidConfig.get():
                kT.debug_log('New')

                if not os.path.isdir(self.newProj.workSpace):
                    os.mkdir(self.newProj.workSpace)

                # Generate main.c, main.h and hardware_init.c if needed
                sourcePath = self.newProj.workSpace + \
                             ('' if self.newProj.workSpace[-1:] == '/' else '/') + \
                             self.newProj.name

                if not os.path.isdir(sourcePath):
                    os.mkdir(sourcePath)
                else:
                    tkMessageBox.showinfo("Project already exists!", "Rename your project.")
                    return

                # Add all drivers for this device
                if self.newProj.libList[0] != 'hal':
                    self.localSDK.get_drivers()
                    maskRet = kT.mask_features(kTool.KsdkTools(), self.newProj.sdkPath, self.newProj.sdkVer, \
                                                                 self.localSDK.drvList, self.newProj.device[1], self.newProj.device[2])
                    self.newProj.portCount = maskRet[0]
                    self.newProj.dmaCount = maskRet[1]
                    self.newProj.tsiVersion = maskRet[2]
                    self.newProj.add_all_drv(self.localSDK.drvList)
                else:
                    self.localSDK.get_hal()
                    maskRet = kT.mask_features(kTool.KsdkTools(), self.newProj.sdkPath, self.newProj.sdkVer, \
                                                                 self.localSDK.halList, self.newProj.device[1], self.newProj.device[2])
                    self.newProj.portCount = maskRet[0]
                    self.newProj.dmaCount = maskRet[1]
                    self.newProj.tsiVersion = maskRet[2]
                    self.newProj.add_all_hal(self.localSDK.halList)
                    ##print self.newProj.halList

                #Get all include paths lists into one list
                includeList = []
                projList = self.newProj.drvList if self.newProj.libList[0] != 'hal' else self.newProj.halList
                index = 0
                isPresent = False
                while index < len(projList):
                    count = 0
                    while count < len(projList[index][2]):
                        isPresent = False
                        newPath = str(\
                                 projList[index][2][count]\
                                     )
                        if len(includeList) > 0:
                            listIndex = 0
                            while listIndex < len(includeList):
                                if newPath == includeList[int(listIndex) - 1]:
                                    isPresent = True
                                listIndex += 1
                        if not isPresent:
                            includeList.append(newPath)
                        count += 1
                    index += 1

                self.newProj.make_main_file(sourcePath, includeList)

                ## Copy over BSP files
                if self.newProj.useBSP:
                    if not os.path.isdir(sourcePath + '/board'):
                        os.mkdir(sourcePath + '/board')
                    bspDir = self.newProj.sdkPath + '/examples/' + self.newProj.board[1]
                    bspList = kT.list_files(bspDir)
                    for f in bspList:
                        if f[-2:] == '.c':
                            shutil.copyfile(bspDir + '/' + f, sourcePath + '/board/' + f)
                        if f[-2:] == '.h':
                            shutil.copyfile(bspDir + '/' + f, sourcePath + '/board/' + f)
                    self.newProj.make_hw_file(sourcePath)

                if self.newProj.isLinked == False:
                    #print 'Standalone'
                    if self.newProj.libList[0] != 'hal':
                        self.localSDK.get_hal()
                        maskRet = kT.mask_features(kTool.KsdkTools(), self.newProj.sdkPath, self.newProj.sdkVer, \
                                                   self.localSDK.halList, self.newProj.device[1], self.newProj.device[2])
                        self.newProj.portCount = maskRet[0]
                        self.newProj.dmaCount = maskRet[1]
                        self.newProj.tsiVersion = maskRet[2]
                        self.newProj.add_all_hal(self.localSDK.halList)
                    self.newProj.copy_device_components(sourcePath, self)

                self.widgetList[31].step(5)
                self.widgetList[31].update_idletasks()

                index = 0

                while index < len(self.newProj.toolChain):
                    if 'iar' in self.newProj.toolChain[index][1]:
                        if self.localSDK.isNewVersion():
                            newIar = kIarNew.KsdkIarNew(self.newProj)
                        else:
                            newIar = kIar.KsdkIar(self.newProj)
                        newIar.gen_ewp(self.newProj)
                        newIar.gen_eww(self.newProj)
                    if 'kds' in self.newProj.toolChain[index][1]:
                        if self.localSDK.isNewVersion():
                            newKds = kKdsNew.KsdkKdsNew(self.newProj)
                        else:
                            newKds = kKds.KsdkKds(self.newProj)
                        newKds.gen_cproject(self.newProj)
                        newKds.gen_project(self.newProj)
                        newKds.gen_working_set(self.newProj)
                        newKds.gen_debug(self.newProj)
                    if 'mdk' in self.newProj.toolChain[index][1]:
                        if self.localSDK.isNewVersion():
                            newMdk = kMdkNew.KsdkMdkNew(self.newProj)
                        else:
                            newMdk = kMdk.KsdkMdk(self.newProj)
                        newMdk.gen_proj(self.newProj)
                        newMdk.gen_wkspace(self.newProj)
                    if 'atl' in self.newProj.toolChain[index][1]:
                        if self.localSDK.isNewVersion():
                            newAtl = kAtlNew.KsdkAtlNew(self.newProj)
                        else:
                            newAtl = kAtl.KsdkAtl(self.newProj)
                        newAtl.gen_cproject(self.newProj)
                        newAtl.gen_project(self.newProj)
                        newAtl.gen_debug(self.newProj)
                        newAtl.gen_settings(self.newProj)
                    index += 1
            else:
                kT.debug_log('Not valid project.')
                return

        self.widgetList[31].step(5)
        self.widgetList[31].update_idletasks()

        #Create window to show USER that project has been generated and where it is.
        popGen = Toplevel()
        if self.newProj.osType == 'Windows':
            winH = 100 * WIN_SCALE
            winW = 600 * WIN_SCALE
        elif self.newProj.osType == 'Darwin':
            if platform.mac_ver()[0][:5] == '10.10':
                winH = 100
                winW = 600
            elif  platform.mac_ver()[0][:5] == '10.11':
                winH = 100
                winW = 660
        else:
            winH = 100
            winW = 600
        popGen.config(height=winH, width=winW)
        popGen.grid()
        if self.newProj.osType == 'Linux':
            img = Image("photo", data=kImg.boardImages['kds_icon.gif']) # Use the .gif in Linux
            popGen.tk.call('wm', 'iconphoto', popGen._w, img)
        popGen.title("Project created")
        popGen.geometry('%dx%d+%d+%d' % (winW, winH, master.winfo_x() + 20, master.winfo_y() + 20))
        #FIXME Radka window about location of generated project is too small, its width should be based on its content 
        popGen.resizable(width=TRUE, height=FALSE)
        popGen.configure(background='#E7E7E7')

        #Text for window
        genString = 'Your project was created in the following location:\n'
        pathString = ''
        pathString += sourcePath if not clonedProjectRoot else clonedProjectRoot
        genString += pathString
        genString += '\nPress the button below to open project location folder.'
        genTxt = Label(popGen, text=genString, justify=LEFT)
        genTxt.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        #Create button to open project folder
        ## IF we are in windows, we need to replace all '/' with '\\'
        tempString = pathString[:]
        pathString = ''
        if self.newProj.osType == 'Windows':
            pathString = kT.string_replace(tempString, '/', '\\')
        else:
            pathString = tempString[:]

        kT.debug_log('This is the path string: ' + pathString)

        genButton = Button(popGen, text='Open Project Folder', command=lambda: self.view_project(pathString, popGen))
        genButton.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        self.newProj.clean_up()

        self.widgetList[31].step(5)
        self.widgetList[31].update_idletasks()

        # support automation test
        self.pop_gen = popGen

        return

    def update_proj(self, *args):

        rtosType = {'0': 'bm', '1': 'mqx', '2': 'freertos', '3': 'ucosii', '4': 'ucosiii'}
        
        enabledState = '!disabled' 
        disabledState = 'disabled'
        areAllToolchainsDisabled = False

        self.localSDK.get_version()
        try:
            self.newProj.name = self.widgetList[3].get()
        except IndexError:
            kT.debug_log('IndexError', sys.exc_info()[2])

        self.newProj.setKsdkPath(self.localSDK.path)
        self.newProj.sdkVer = self.localSDK.version
        self.newProj.useBSP = True if self.advIsBsp.get() else False
        self.newProj.useUSB = True if self.advIsUsb.get() else False
        self.newProj.rtos = rtosType[str(self.advancedRtosType.get())]

        if self.advancedRtosType.get():
            if self.advancedDevType.get() != 1:
                self.advancedDevType.set(1)
            self.advancedLibType.set(1)
            #FIXME Radka
            #self.advIsBsp.set(1)
            #self.newProj.useBSP = True if self.advIsBsp.get() else False
            try:
                kT.debug_log('RTOS Selected.')
                # Check mqx directory to see if toolchains are supported
                if self.newProj.rtos == 'mqx':
                    mqxIdes = kT.list_dirs(self.newProj.sdkPath + '/rtos/mqx/build/')
                    self.widgetList[19].state(["!disabled" if 'kds' in mqxIdes else "disabled"])
                    self.widgetList[20].state(["!disabled" if 'iar' in mqxIdes else "disabled"])
                    self.widgetList[21].state(["!disabled" if 'mdk' in mqxIdes else "disabled"])
                    self.widgetList[22].state(["!disabled" if 'atl' in mqxIdes else "disabled"])

                    self.advIsKds.set(0) if 'kds' not in mqxIdes else None
                    self.advIsIar.set(0) if 'iar' not in mqxIdes else None
                    self.advIsMdk.set(0) if 'mdk' not in mqxIdes else None
                    self.advIsAts.set(0) if 'atl' not in mqxIdes else None
                else:
                    self.widgetList[19].state(["!disabled"])
                    self.widgetList[20].state(["!disabled"])
                    self.widgetList[21].state(["!disabled"])
                    self.widgetList[22].state(["!disabled"])

                self.widgetList[10].state(["disabled"])
                self.widgetList[35].state(["disabled"])
            except IndexError:
                kT.debug_log('IndexError', sys.exc_info()[2])
                return False
        else:
            try:
                self.widgetList[10].state(["!disabled"])
                self.widgetList[35].state(["!disabled"])
                # if it is Clone selected (it is not first option), than toolchains should be disabled
                status = enabledState if not self.advancedProjType.get() else disabledState
                self.widgetList[18].state([status])
                self.widgetList[19].state([status])
                self.widgetList[20].state([status])
                self.widgetList[21].state([status])
                self.widgetList[22].state([status])
                if status == disabledState:
                    areAllToolchainsDisabled = True
            except IndexError:
                kT.debug_log('IndexError', sys.exc_info()[2])
                return False

        kT.debug_log('Lib type change.')
        if not self.advancedProjType.get():
            if self.advancedLibType.get():
                if self.advancedRtosType.get():
                    self.widgetList[25].state(["disabled"])
                else:
                    self.widgetList[25].state(["!disabled"])
            else:
                self.advIsBsp.set(0)
                self.widgetList[25].state(["disabled"])
        else:
            self.widgetList[10].state(["disabled"])

        del self.newProj.libList[:]
        if self.newProj.rtos == 'bm':
            self.newProj.libList.append('platform' if self.advancedLibType.get() else 'hal')
        else:
            self.newProj.libList.append(self.newProj.rtos)

        if self.newProj.useUSB:
            self.newProj.libList.append('usb')

        kT.debug_log(self.newProj.libList)

        var = self.newProj.add_tool(0) if self.advIsGcc.get() else self.newProj.remove_tool(0)
        var = self.newProj.add_tool(1) if self.advIsKds.get() else self.newProj.remove_tool(1)
        var = self.newProj.add_tool(2) if self.advIsAts.get() else self.newProj.remove_tool(2)
        var = self.newProj.add_tool(3) if self.advIsIar.get() else self.newProj.remove_tool(3)
        var = self.newProj.add_tool(4) if self.advIsMdk.get() else self.newProj.remove_tool(4)

        kT.debug_log(var)

        if self.advIsStandalone.get():
            kT.debug_log('Standalone')
            self.newProj.isLinked = False
        else:
            kT.debug_log('Linked')
            self.newProj.isLinked = True

        if self.advancedDevType.get():
            # Add the board
            userBoard = self.localSDK.brdList.index(self.advBrdSelect.get()) + 1
            self.newProj.add_board(userBoard, self.localSDK.brdList)
            kT.debug_log(userBoard)
            #print userBoard
            #print self.newProj.board
        else:
            #print self.advDevSelect.get()
            self.newProj.add_device(self.advDevSelect.get())
            #print self.newProj.device

        self.newProj.get_proj_config()
        
        self._update_project_path()
        
        #update toolchains based on selected device
        if not areAllToolchainsDisabled:
            isKDSSupported = self.localSDK.isToolchainTypeSupported(ToolchainType.KinetisDesignStudio, self.newProj.device)
            isIarSupported = self.localSDK.isToolchainTypeSupported(ToolchainType.IARname, self.newProj.device)
            isAtollicSupported = self.localSDK.isToolchainTypeSupported(ToolchainType.AtollicStudio, self.newProj.device) 
            isKeilSupported = self.localSDK.isToolchainTypeSupported(ToolchainType.KeilMDK, self.newProj.device)
                
            self.widgetList[19].state([enabledState if isKDSSupported else disabledState])
            self.widgetList[20].state([enabledState if isIarSupported else disabledState])
            self.widgetList[21].state([enabledState if isKeilSupported else disabledState])
            self.widgetList[22].state([enabledState if isAtollicSupported else disabledState])

        kT.debug_log(self.newProj.projSummary)

        return True
    
    def _update_project_path(self):
        """
        Updates project path
        """
        # in case the project is linked the path to project has to be updated
        if (self.newProj.board is not None and len(self.newProj.board) == 0) or len(self.widgetList) < 28:
            return
        defaultLinkedPath = self.newProj.sdkPath + '/' + self.newProj.parent.getDirectoryStructureHelper().getUserLinkedExamplesPath(self.newProj.board[1])
        if self.newProj.isLinked:
            self.newProj.workSpace = defaultLinkedPath
            if self.newProj.osType == 'Windows':
                self.newProj.workSpace = kT.string_replace(self.newProj.workSpace, '/', '\\')
            self.widgetList[28].state(["!disabled"])
            self.widgetList[27].state(["!disabled"])
            self.widgetList[27].delete(0, END)
            self.widgetList[27].insert(0, self.newProj.workSpace)
            self.widgetList[27].state(["disabled"])
            self.widgetList[28].state(["disabled"])
        else:
            previousPath = self.widgetList[27].get()
            if (kT.string_replace((kT.string_replace(previousPath, '/', '')), '\\', '') != kT.string_replace(defaultLinkedPath, '/', '')) and (self.newProj.workSpace != previousPath):
                self.newProj.workSpace = previousPath
            else:
                #FIXME Radka remove it after testing, it is for testing purposes
                #self.newProj.workSpace = self.newProj.sdkPath + '/user_projects'
                self.newProj.workSpace = defaultLinkedPath
            if self.newProj.osType == 'Windows':
                self.newProj.workSpace = kT.string_replace(self.newProj.workSpace, '/', '\\')
            self.widgetList[28].state(["!disabled"])
            self.widgetList[27].state(["!disabled"])
            self.widgetList[27].delete(0, END)
            self.widgetList[27].insert(0, self.newProj.workSpace)
            checkName = self.widgetList[27].get()
            if kT.check_wksp_name(checkName):
                self.newProj.workSpace = checkName
            else:
                kT.debug_log('Invalid Workspace')
                self.newProj.workSpace = None
                if self.prevWksp != checkName:
                    tkMessageBox.showinfo("Invalid Output Path",\
                                      "Permitted characters: 0-9a-zA-Z_ :\\/-.")
                    self.prevWksp = checkName
                    kT.debug_log("Invalid name")
                    return False
                
                if checkName != self.newProj.workSpace:
                    kT.debug_log('New Workspace')
                    if kT.check_wksp_name(checkName):
                        self.newProj.workSpace = checkName
                    else:
                        kT.debug_log('Invalid Workspace')
                        self.newProj.workSpace = None
                        if self.prevWksp != checkName:
                            tkMessageBox.showinfo("Invalid Output Path",\
                                              "Permitted characters: 0-9a-zA-Z_ :\\/-.")
                            self.prevWksp = checkName
                            kT.debug_log("Invalid name")
                            return False
                        

    def update_gui(self, *args):
        """Updates advanced GUI based on 'new' or 'clone' selection
        """

        # List of widgets that will be disabled if choosing to clone a project
        disWidgetList = [3, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 25, 29, 34]

        try:
            self.localSDK.get_version()
        except IOError:
            kT.debug_log('IO Error', sys.exc_info()[2])
        try:
            self.newProj.name = self.widgetList[3].get()
        except IndexError:
            kT.debug_log('Index Error', sys.exc_info()[2])
        
        self.newProj.setKsdkPath(self.localSDK.path)
        self.newProj.sdkVer = self.localSDK.version

        labelFont = 'Arial 9 bold'

        if self.prevProjType != self.advancedProjType.get():
            if self.advancedProjType.get():
                if len(self.widgetList) > 36:
                    self.widgetList[35].grid_remove()
                    self.widgetList[36].grid_remove()
                    self.widgetList[37].grid_remove()
                    del self.widgetList[37]
                    del self.widgetList[36]
                    del self.widgetList[35]
                # Disable widgets that aren't applicable to cloning
                for w in disWidgetList:
                    self.widgetList[w].state(["disabled"])
                # Enable build
                self.widgetList[31].config(command=lambda: self.begin_advanced_gen(self.master, None))
                self.widgetList[31].state(["!disabled"])
                ### Widget 7 is the label for the device drop down menu
                self.widgetList[7].config(text='Board:')
                ### Widget 8 is te drop down menu for the devices
                self.widgetList[8].config(textvariable=self.advBrdSelect)
                self.widgetList[8]['values'] = self.localSDK.brdList
                try:
                    self.widgetList[8].current(int(self.currBoard) - 1)
                except IOError:  ## Catch the case where the user hasn't selected anything
                    self.widgetList[8].current(0)
                except ValueError:  ## Catch the case where there is no device given in manifest
                    self.widgetList[8].current(0)
                ### Widget 34 is the label for the clone project drop down menu
                self.widgetList.append(Label(self, text='Project:', font=labelFont))
                self.widgetList[35].grid(row=2, column=3, sticky=W, pady=(5, 0))
                ### Widget 35 is te drop down menu for the clonable projects
                try:
                    self.localSDK.get_projects(self.newProj.board[1])
                except IndexError:
                    self.localSDK.get_projects('frdmk22f')
                self.widgetList.append(Combobox(self, state='readonly'))
                self.widgetList[36]['values'] = self.localSDK.demoLst
                self.widgetList[36].grid(row=3, column=3, columnspan=2, sticky=W+E, pady=(0, 0))
                try:
                    self.widgetList[36].current(0)
                except TclError:
                    kT.debug_log('No list', sys.exc_info()[2])
            else:
                kT.debug_log('Widget list length = %d' %len(self.widgetList))
                if len(self.widgetList) > 35:
                    self.widgetList[35].grid_remove()
                    self.widgetList[36].grid_remove()
                    del self.widgetList[36]
                    del self.widgetList[35]
                ### Widget 35 is a radio button for configuring a new project
                self.widgetList.append(Radiobutton(self, text='Device', variable=self.advancedDevType, \
                                                   value=0))
                try:
                    self.widgetList[35].grid(row=3, column=3, sticky=W)
                except IndexError:
                    self.prevProjType = self.advancedProjType.get()
                    return
                ### Widget 36 is a radio button for configuring a cloned project
                self.widgetList.append(Radiobutton(self, text='Board', variable=self.advancedDevType, \
                                                   value=1))
                self.widgetList[36].grid(row=3, column=3, sticky=E)
                self.advancedDevType.set(0)
                ### Widget 37 is the label for project type
                self.widgetList.append(Label(self, text='Device or Board:', font=labelFont))
                self.widgetList[37].grid(row=2, column=3, sticky=W, pady=(5, 0))
                # Enable widgets that aren't applicable to cloning
                try:
                    for w in disWidgetList:
                        self.widgetList[w].state(["!disabled"])
                    # Disable build
                    self.widgetList[31].config(command=lambda: self.package_select(self.master))
                    self.widgetList[31].state(["!disabled"])
                    ### Widget 7 is the label for the device drop down menu
                    self.widgetList[7].config(text='Device:')
                    ### Widget 8 is te drop down menu for the devices
                    self.widgetList[8].config(textvariable=self.advDevSelect)
                    self.widgetList[8]['values'] = self.localSDK.devList
                except IndexError:
                    kT.debug_log('IndexError', sys.exc_info()[2])
                try:
                    self.newProj.add_board(self.currBoard, self.localSDK.brdList)
                    self.widgetList[8].current(self.localSDK.devList.index(self.newProj.device[0]))
                except IndexError:
                    kT.debug_log('IndexError', sys.exc_info()[2])
                except IOError:  ## Catch the case where the user hasn't selected anything
                    try:
                        self.widgetList[8].current(0)
                    except IndexError:
                        kT.debug_log('IndexError', sys.exc_info()[2])
                except ValueError:  ## Catch the case where there is no device given in manifest
                    try:
                        self.widgetList[8].current(0)
                    except IndexError:
                        kT.debug_log('Index Error', sys.exc_info()[2])
        self.prevProjType = self.advancedProjType.get()
        self.update_proj()
        return

    def update_dev(self, *args):
        """ Update GUI from device to board and vice versa
        """
        try:
            self.localSDK.get_version()
        except IOError:
            kT.debug_log('IO Error', sys.exc_info()[2])
        try:
            self.newProj.name = self.widgetList[3].get()
        except IndexError:
            kT.debug_log('Index Error', sys.exc_info()[2])
        self.newProj.setKsdkPath(self.localSDK.path)
        self.newProj.sdkVer = self.localSDK.version

        if self.advancedDevType.get():

            self.widgetList[34].state(["!disabled"])

            ### Widget 7 is the label for the device drop down menu
            self.widgetList[7].config(text='Board:')

            try:
                self.widgetList[31].config(command=lambda: self.begin_advanced_gen(self.master, None))
            except TclError:
                kT.debug_log('Tcl Error', sys.exc_info()[2])

            ### Widget 8 is te drop down menu for the devices
            self.widgetList[8].config(textvariable=self.advBrdSelect)
            self.widgetList[8]['values'] = self.localSDK.brdList
            try:
                self.widgetList[8].current(int(self.currBoard) - 1)
            except IOError:  ## Catch the case where the user hasn't selected anything
                self.widgetList[8].current(0)
            except ValueError:  ## Catch the case where there is no device given in manifest
                self.widgetList[8].current(0)
        else:
            try:
                self.widgetList[34].state(["disabled"])

                ### Widget 7 is the label for the device drop down menu
                self.widgetList[7].config(text='Device:')

                self.widgetList[31].config(command=lambda: self.package_select(self.master))

                ### Widget 8 is te drop down menu for the devices
                self.widgetList[8].config(textvariable=self.advDevSelect)
                self.widgetList[8]['values'] = self.localSDK.devList
            except IndexError:
                kT.debug_log('IndexError', sys.exc_info()[2])

            try:
                self.newProj.add_board(self.currBoard, self.localSDK.brdList)
                self.widgetList[8].current(self.localSDK.devList.index(self.newProj.device[0]))
            except IndexError:
                kT.debug_log('IndexError', sys.exc_info()[2])
            except IOError:  ## Catch the case where the user hasn't selected anything
                try:
                    self.widgetList[8].current(0)
                except IndexError:
                    kT.debug_log('IndexError', sys.exc_info()[2])
            except ValueError:  ## Catch the case where there is no device given in manifest
                try:
                    self.widgetList[8].current(0)
                except IndexError:
                    kT.debug_log('Index Error', sys.exc_info()[2])
        
        #FIXME Radka add special method for updating path             
        self._update_project_path()

    def package_select(self, master):
        """ Pop-up to prompt user for a package
        """

        #print self.newProj.workSpace

        if self.update_proj():
            self.isValidConfig.set(1)
        else:
            self.isValidConfig.set(0)
            return

        #print self.newProj.workSpace

        if len(self.newProj.toolChain) < 1:
            tkMessageBox.showinfo("No Toolchain Selected",\
                                          "Select a toolchain to generate a project.")
            return

        # Disable generate button
        self.widgetList[31].state(["disabled"])

        #Create package list form selected device
        packageList = []

        tree = ET.parse(self.newProj.sdkPath + '/ksdk_manifest.xml')
        for elem in tree.iter(tag='device'):
            if elem.attrib['full_name'] == self.newProj.device[0]:
                for pack in elem.findall('package'):
                    packageList.append(pack.attrib['name'])

        labelFont = 'Arial 9 bold'

        #Create window to show USER that project has been generated and where it is.
        popPackage = Toplevel()
        winH = 0
        winW = 0
        if self.newProj.osType == 'Windows':
            winH = 75 * WIN_SCALE
            winW = 250 * WIN_SCALE
        elif self.newProj.osType == 'Darwin':
            if platform.mac_ver()[0][:5] == '10.10':
                winH = 75
                winW = 300
            elif  platform.mac_ver()[0][:5] == '10.11':
                winH = 75
                winW = 330
        else:
            winH = 75
            winW = 300
        popPackage.config(height=winH, width=winW)
        popPackage.protocol('WM_DELETE_WINDOW', lambda: self.safe_return(popPackage))
        popPackage.grid()
        if self.newProj.osType == 'Linux':
            img = Image("photo", data=kImg.boardImages['kds_icon.gif']) # Use the .gif in Linux
            popPackage.tk.call('wm', 'iconphoto', popPackage._w, img)
        popPackage.title("Select Device Package.")
        popPackage.geometry('%dx%d+%d+%d' % (winW, winH, master.winfo_x() + 20, master.winfo_y() + 20))
        popPackage.resizable(width=FALSE, height=FALSE)
        popPackage.configure(background='#E7E7E7')

        #Text for window
        genString = 'Package:'
        genTxt = Label(popPackage, text=genString, justify=LEFT, font=labelFont)
        genTxt.grid(row=0, column=0, columnspan=1, sticky=W+E, padx=5, pady=5)

        genBox = Combobox(popPackage, state='readonly')
        genBox.config(textvariable=self.devPackage)
        genBox['values'] = packageList
        genBox.grid(row=1, column=0, sticky=W+E, padx=5)
        genBox.current(0)

        genButton = Button(popPackage, text='Apply', command=lambda: self.begin_advanced_gen(master, popPackage))
        genButton.grid(row=1, column=1, sticky=W+E, padx=5)

        # support automation test
        self.pop_package = popPackage

    def safe_return(self, window):
        """ When pop-up is closed, safely without build
        """

        window.destroy()

        # Enable generate button
        self.widgetList[31].state(["!disabled"])

        tkMessageBox.showinfo("Error", \
                                      'A valid device package must be selected.')

        return

    def update_package(self, *args):
        """ Update project device package
        """

        temp = (self.newProj.device[0],\
                self.newProj.device[1],\
                self.devPackage.get(),\
                self.newProj.device[3],\
                self.newProj.device[4])

        del self.newProj.device

        self.newProj.device = temp

        kT.debug_log(self.newProj.device)

        del temp

        return

    def advanced_help(self, master, helpText):
        """Callback function for 'Help' button to provide a brieft user guide and links to websites

        :param master: Tkinter object
        :param helpText: Text string to be displayed in pop-up window
        """
        osName = platform.system()
        popHelp = Toplevel()
        popHelp.grid()
        winH = 0
        winW = 0
        if osName == 'Windows':
            winH = 300 * WIN_SCALE
            winW = 400 * WIN_SCALE
        elif osName == 'Darwin':
            if platform.mac_ver()[0][:5] == '10.10':
                winH = 300
                winW = 450
            elif  platform.mac_ver()[0][:5] == '10.11':
                winH = 300
                winW = 510
        else:
            winH = 300
            winW = 450
        popHelp.config(height=winH , width=winW)
        if osName == 'Linux':
            img = Image("photo", data=kImg.boardImages['kds_icon.gif']) # Use the .gif in Linux
            popHelp.tk.call('wm', 'iconphoto', popHelp._w, img)
        popHelp.title(PGKSDK_NAME + " Help")
        popHelp.geometry('%dx%d+%d+%d' % (winW, winH, master.winfo_x() + 20, master.winfo_y() + 20))
        popHelp.resizable(width=FALSE, height=FALSE)
        popHelp.configure(background='#E7E7E7')
        ## Display help
        helpTxt = Label(popHelp, text=helpText, justify=LEFT)
        helpTxt.grid(row=0, column=0, rowspan=5, columnspan=2, padx=5, pady=5)

    def clone_update(self, *args):
        """ Update the advanced GUI when the user picks a new board
        """
        if self.advancedProjType.get():
            ##print self.advBrdSelect.get()
            userBoard = self.localSDK.brdList.index(self.advBrdSelect.get()) + 1
            self.newProj.add_board(userBoard, self.localSDK.brdList)
            self.localSDK.get_projects(self.newProj.board[1])
            try:
                self.widgetList[36]['values'] = self.localSDK.demoLst
                self.widgetList[36].current(0)
            except IndexError:
                kT.debug_log('Index Error', sys.exc_info()[2])

    def view_project(self, pathString, window):
        """ Open containing folder and destroy window
        """

        kT.debug_log('This is the project path: ' + pathString)

        if self.newProj.osType == 'Windows':
            subprocess.call(['explorer', pathString])
        elif self.newProj.osType == 'Linux':
            subprocess.Popen(['xdg-open', pathString])
        elif self.newProj.osType == 'Darwin':
            subprocess.Popen(['open', pathString])

        window.destroy()

        return
