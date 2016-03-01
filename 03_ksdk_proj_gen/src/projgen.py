"""
File:  projgen.py
=================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Main file for KSDK project creation GUI**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.5

TODO
++++
.. todolist:: 

API
+++

"""

## USER MODULES
from ksdkGUI import PgGui, PGKSDK_VERSION, PGKSDK_NAME
import ksdkGUI as kGUI
import ksdkImg as kImg

## PYTHON MODULES
from Tkinter import *
from ttk import *
import tkMessageBox
import re
import sys
import os
import platform
if platform.system() == 'Windows':
    import _winreg


def main(argv):
    """ Main file for KSDK Project Generator

    .. todo::

        test on Linux, OSX

    .. todo::

        go over comments for documentation; params, etc...

    """

    osName = platform.system()
    root = Tk()                                                # Call Tkinter object 'root'
    s = Style()

    #tkMessageBox.showinfo("Error", 'Path: ' + os.getcwd())
        
    # Set ttk style for the OS
    if osName == 'Linux':
        themeName = 'alt'
    elif osName == 'Windows':
        themeName = 'vista'
    elif osName == 'Darwin':
        themeName = 'aqua'
        
    themeNames = s.theme_names()
    if themeNames.count(themeName) == 1:
        s.theme_use(themeName)
    elif len(themeNames) > 0:
        s.theme_use(themeNames[0])

    if osName == 'Windows':                                     # Check if running on Windows
        try:
            root.iconbitmap(default='./kds_icon.ico')           # Use the .ico file if in Windows
        except TclError:
            root.iconbitmap(default=None)
    elif osName == 'Linux':
        img = Image("photo", data=kImg.boardImages['kds_icon.gif']) # Use the .gif file if in Linux
        root.tk.call('wm', 'iconphoto', root._w, img)

    root.title(PGKSDK_NAME + ' -- ' + PGKSDK_VERSION)   # Set title of Tkinter window

    if osName == 'Darwin':
        root.configure(background='#E7E7E7')

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    if osName == 'Windows':

        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop\\WindowMetrics")
        value = _winreg.QueryValueEx(key, "AppliedDPI")[0]

        #print "DPI value: " + str(value)

        if value == 96:
            kGUI.WIN_SCALE = 1.0
        elif value == 120:
            kGUI.WIN_SCALE = 1.25
        elif value == 144:
            kGUI.WIN_SCALE = 1.5
        elif value == 192:
            kGUI.WIN_SCALE = 2.0
        else:
            kGUI.WIN_SCALE = value / 96.0

        #print "DPI scale: " + str(kGUI.WIN_SCALE)

        
        windowWidth = (570 * kGUI.WIN_SCALE)
        windowHeight = (450 * kGUI.WIN_SCALE)

        # Get x & y location for centering the window
        xLocation = screenWidth / 2 - windowWidth / 2
        yLocation = screenHeight / 2 - windowHeight / 2

        root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, xLocation, yLocation))
    elif osName == 'Linux':

        windowWidth = 605
        windowHeight = 420

        # Get x & y location for centering the window
        xLocation = screenWidth / 2 - windowWidth / 2
        yLocation = screenHeight / 2 - windowHeight / 2

        root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, xLocation, yLocation))
    else:

        #print "Mac Version"

        macVer = platform.mac_ver()[0]

        #print macVer[:5]

        if macVer[:5] == '10.10':
            windowWidth = 620
            windowHeight = 480
        elif macVer[:5] == '10.11':
            windowWidth = 680
            windowHeight = 480            

        # Get x & y location for centering the window
        xLocation = screenWidth / 2 - windowWidth / 2
        yLocation = screenHeight / 2 - windowHeight / 2

        root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, xLocation, yLocation))

    root.resizable(width=FALSE, height=FALSE)
    gui = PgGui(master=root)
    gui.mainloop()

    try:
        root.destroy()                                          # Destroy the Tkinter object 'root'
    except TclError:
        sys.exit()

#########################
##  Call main routine  ##
#########################
if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit()
