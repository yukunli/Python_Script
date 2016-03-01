"""
File:  ksdkProj.py
==================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Class for KSDK project object**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.5

Inheritance
+++++++++++
.. inheritance-diagram:: ksdkProj

UML
+++
.. uml:: {{/../../../src/ksdkProj.py

API
+++

"""


## USER MODULES
from ksdkTools import KsdkTools as kT
from ksdkObj import *
import ksdkObj as kSdk
import ksdkGUI

## PYTHON MODULES
import os
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import shutil
from distutils.dir_util import copy_tree
import  distutils.dir_util
import time
from Tkinter import *
from ttk import *
import tkMessageBox
import threading
import Constants
import Texts
from directoryStructureHelper import RTOSType
import ksdkObj

#TODO: Add 1.3.0 boards
#NOTE: 1.3.0 will be delivered via mFact system. Therefore, all possible boards need to be in list below.
BOARD_COMPATIBILITY = \
[\
    ('frdmk22f', ['MK02F12810', 'MK22F25612', 'MK22F12810', 'MK22F51212']),\
    ('frdmk64f', ['MK24F12', 'MK63F12', 'MK64F12']),\
    ('frdmk66f', ['MK26F18', 'MK65F18', 'MK66F18']),\
    ('frdmk82f', ['MK80F25615', 'MK81F25615', 'MK82F25615']),\
    ('frdmkv10z', ['MKV10Z', 'MKV10Z7', 'MKV10Z1287']),\
    ('frdmkv31f', ['MKV30F12810', 'MKV31F12810', 'MKV31F25612', 'MKV31F51212']),\
    ('frdmkw019032', ['MKW01Z4']),\
    ('frdmkw01', ['MKW01Z4']),\
    ('frdmkw24', ['MKW21D5', 'MKW22D5', 'MKW24D5']),\
    ('frdmkw40z', ['MKW20Z4', 'MKW30Z4', 'MKW40Z4']),\
    ('frdmkl02z', ['MKL02Z4']),\
    ('frdmkl03z', ['MKL03Z4']),\
    ('frdmkl25z', ['MKL14Z4', 'MKL15Z4', 'MKL24Z4', 'MKL25Z4']),\
    ('frdmkl26z', ['MKL16Z4', 'MKL26Z4']),\
    ('frdmkl27z', ['MKL17Z644', 'MKL27Z644']),\
    ('frdmkl43z', ['MKL13Z644', 'MKL17Z4', 'MKL27Z4', 'MKL33Z4', 'MKL33Z644', 'MKL34Z4', 'MKL43Z4']),\
    ('frdmkl46z', ['MKL36Z4', 'MKL46Z4']),\
    ('mrbkw01', ['MKW01Z4']),\
    ('twrk21d50m', ['MK11DA5', 'MK21DA5']),\
    ('twrk21f120m', ['MK21FA12', 'MK22FA12']),\
    ('twrk22f120m', ['MK02F12810', 'MK22F25612', 'MK22F12810', 'MK22F51212']),\
    ('twrk24f120m', ['MK24F25612']),\
    ('twrk60d100m', ['MK10D10', 'MK20D10', 'MK30D10', 'MK40D10', 'MK50D10', 'MK51D10', 'MK52D10', 'MK53D10', 'MK60D10']),\
    ('twrk64f120m', ['MK24F12', 'MK63F12', 'MK64F12']),\
    ('twrk65f180m', ['MK26F18', 'MK65F18', 'MK66F18']),\
    ('twrk80f150m', ['MK80F25615', 'MK81F25615', 'MK82F25615']),\
    ('twrkl43z48m', ['MKL17Z4', 'MKL27Z4', 'MKL33Z4', 'MKL34Z4', 'MKL43Z4']),\
    ('twrkm34z75m', ['MKM34Z7']),\
    ('twrkv10z32', ['MKV10Z', 'MKV10Z7', 'MKV10Z1287']),\
    ('twrkv11z75m', ['MKV11Z7']),\
    ('twrkv31f120m', ['MKV30F12810', 'MKV31F12810', 'MKV31F25612', 'MKV31F51212']),\
    ('twrkv46f150m', ['MKV40F15', 'MKV43F15', 'MKV44F15', 'MKV45F15', 'MKV46F15', 'MKV42F16', 'MKV44F16', 'MKV46F16']),\
    ('twrkv58f220m', ['MKV56F22', 'MKV58F22']),\
    ('twrkw24d512', ['MKW21D5', 'MKW22D5', 'MKW24D5']),\
    ('usbkw24d512', ['MKW21D5', 'MKW22D5', 'MKW24D5']),\
    ('usbkw40z', ['MKW20Z4', 'MKW30Z4', 'MKW40Z4']),\
    ('usbkw40zk22f', ['MK22F51212'])\
]

##################
##  Proj Class  ##
##################
class ksdkProjClass(kSdk.kinetisSDK):

    def __init__(self, prjName, ksdkVer, ksdkPath, osName, userName, date):
        """ Init KSDK project class
        """
        kSdk.kinetisSDK.__init__(self, ksdkPath)
        self.osType = osName
        self.userName = userName
        self.date = date
        self.name = prjName
        self.sdkPath = ksdkPath   #Path of KSDK for project
        self.sdkVer = ksdkVer    #Version of KSDK being used
        self.board = ()         #Tuple containing board information
        self.useBSP = False      #Boolean for tracking if BSP is being used
        self.useUSB = False      #Boolean for tracking if USB is used
        self.toolChain = []         #Tuple containing tool chain information
        self.device = ()         #Tuple containing device information
        self.drvList = []         #List of peripheral drivers tuples
        self.halList = []         #List of hal component tuples
        self.othList = []         #List of other component tuples
        self.libList = []         #List of libraries used
        self.rtos = ''         #name of RTOS used (if one is used)
        self.isLinked = True       #Boolean for if project is linked or standalone
        self.workSpace = ''
        self.projSummary = ''
        self.portCount = 0
        self.dmaCount = 0
        self.tsiVersion = 0
        self.directoryStructureHelper = self.getDirectoryStructureHelper()
        self.parent = kSdk.kinetisSDK(ksdkPath)
        self.isBoardProject = False
        self.isQuickGenerate = True
        
    def setKsdkPath(self, ksdkPath):
        """ Sets ksdk path to project
        """
        if ksdkPath != self.sdkPath:
            newParent = kSdk.kinetisSDK(ksdkPath)
            self.parent = newParent
            self.directoryStructureHelper = newParent.getDirectoryStructureHelper()
            self.sdkPath = ksdkPath

    def clean_up(self):
        """ Cleans up project information to avoid including previous data
        """

        self.board = ()         #Tuple containing board information
        self.useBSP = False      #Boolean for tracking if BSP is being used
        self.useUSB = False      #Boolean for tracking if USB is used
        self.toolChain = []         #Tuple containing tool chain information
        self.device = ()         #Tuple containing device information
        self.drvList = []         #List of peripheral drivers tuples
        self.halList = []         #List of hal component tuples
        self.libList = []         #List of libraries used
        self.rtos = ''         #name of RTOS used (if one is used)
        self.isLinked = True       #Boolean for if project is linked or standalone
        self.workSpace = ''
        self.projSummary = ''
        self.isBoardProject = False

    def get_proj_config(self):
        """ Summarize project configuration into string
        """
        self.projSummary = "\n###############################################"
        self.projSummary += "\n\n" + self.name + " configuration details\n"
        self.projSummary += "\nKSDK Path: " + self.sdkPath + "\n"
        self.projSummary += "\nToolchains:\n"
        for tools in self.toolChain:
            self.projSummary += "\t" + tools[0] + "\n"
        if self.useBSP == True:
            self.projSummary += "\nBoard selection: " + self.board[3] + "\n"
        self.projSummary += "\nDevice selection\n\n"
        self.projSummary += "                   Name: " + self.device[1] + "\n"
        self.projSummary += "                Package: " + self.device[2] + "\n"
        self.projSummary += "                   Core: Cortex-M" + self.device[4][2:] + "\n"
        self.projSummary += "            FPU present? " + str(self.device[3]) + "\n"
        self.projSummary += "\nLibrary selection\n"
        count = 0
        while count < len(self.libList):
            self.projSummary += "\t\t" + self.libList[count]
            count += 1
        self.projSummary += "\n\n\t\tRTOS: " + self.rtos + "\n"
        self.projSummary += "###############################################"
        return

    def add_board(self, boardSelection, boardList):
        """ Map user's board selection back to the boards list to get names for project dependencies

        :param boardSelection: index of board list from GUI
        :param boardList: list of boards in KSDK installation
        """
        root = self.parent._getRootOfManifest()
        brdId = ''
        brdName = ''
        brdPkg = ''
        brdUser = ''
        for boardsPresent in root.findall('boards'):
            for child in boardsPresent:
                if child.get('user_name') == boardList[int(boardSelection) - 1]:
                    brdId = child.get('id')
                    brdName = child.get('name')
                    brdPkg = child.get('package')
                    brdUser = child.get('user_name')
        self.board = (brdId, brdName, brdPkg, brdUser)
        #Now add the device using the package from the board
        devFullName = ''
        devName = ''
        devPkg = ''
        devHasFPU = False
        devCore = ''
        for devicesPresent in root.findall('devices'):
            for deviceType in devicesPresent.findall('device'):
                for package in deviceType.findall('package'):
                    deviceCheck = package.get('name')
                    if str(deviceCheck) == str(self.board[2]):
                        devFullName = deviceType.get('full_name')
                        devName = deviceType.get('name')
                        devPkg = deviceCheck
                        for core in deviceType.findall('core'):
                            devHasFPU = True if core.get('fpu') == "true" else False
                            devCore = core.get('name')
        self.device = (devFullName, devName, devPkg, devHasFPU, devCore)
        return

    def add_device(self, fullName):
        """ Populate device tuple from device fullName

        :param fullName: name of the device to add
        """
        devFullName = ''
        devName = ''
        devPkg = ''
        devHasFPU = False
        devCore = ''

        root = self.parent._getRootOfManifest()
        for elem in root.iter(tag='device'):
            if elem.attrib['full_name'] == fullName:
                #print elem.attrib['full_name']
                for opt in elem.findall('core'):
                    devHasFPU = True if opt.attrib['fpu'] == "true" else False
                    devCore = opt.attrib['name']
                for pack in elem.findall('package'):
                    devPkg = pack.attrib['name']
                devFullName = elem.attrib['full_name']
                devName = elem.attrib['name']
                self.device = (devFullName, devName, devPkg, devHasFPU, devCore)

        # Add board so a template can be included for BSP
        if self.parent.isNewVersion():
            supportedBoardList = self.parent.getListOfSupportedBoardsForDevice(self.device[0])
            if len(supportedBoardList) > 0:
                self.board = self.parent.getBoardInformation(supportedBoardList[0], self.device)
        else:
            for b in BOARD_COMPATIBILITY:
                    if self.device[1] in b[1]:
                        #print b[1]
                        tree = ET.parse(self.sdkPath + '/ksdk_manifest.xml')
                        root = tree.getroot()
                        for boardsPresent in root.findall('boards'):
                            for child in boardsPresent.findall('board'):
                                #print b[0]
                                if child.get('name') == b[0]:
                                    brdId = child.get('id')
                                    brdName = child.get('name')
                                    brdPkg = self.device[2]
                                    brdUser = child.get('user_name')
                                    self.board = (brdId, brdName, brdPkg, brdUser)
                                    return
        return

    def add_tool(self, toolSelect):
        """ Add toolchain to the project

        :param toolSelect: index of toolList to be added from project
        """
        toolName = kSdk.toolList[int(toolSelect)][0]
        toolCode = kSdk.toolList[int(toolSelect)][1]
        toolComp = kSdk.toolList[int(toolSelect)][2]
        tempTool = (toolName, toolCode, toolComp)
        if tempTool not in self.toolChain:
            self.toolChain.append((toolName, toolCode, toolComp))
        del tempTool
        return

    def remove_tool(self, toolSelect):
        """ Remove toolchain to the project

        :param toolSelect: index of toolList to be removed from project
        """
        toolName = kSdk.toolList[int(toolSelect)][0]
        toolCode = kSdk.toolList[int(toolSelect)][1]
        toolComp = kSdk.toolList[int(toolSelect)][2]
        tempTool = (toolName, toolCode, toolComp)
        if tempTool in self.toolChain:
            self.toolChain.remove((toolName, toolCode, toolComp))
        del tempTool
        return

    def add_all_drv(self, driverList):
        """Add all drivers to project paths

        :param driverList: list of drivers
        """
        root = self.parent._getRootOfManifest()
        drvName = ''
        includePaths = []
        sourcePaths = []
        includeFiles = []
        sourceFiles = []
        index = 0
        #print driverList
        while index < len(driverList):
            for driversPresent in root.findall('components'):
                for componentType in driversPresent.findall('component'):
                    if componentType.get('type') == 'driver':
                        if componentType.get('name') == driverList[index]:
                            drvName = componentType.get('name')
                            # HACK: for K80 lmem_cache to lmem
                            if drvName == 'lmem_cache':
                                drvName = 'lmem'
                            for sources in componentType.findall('source'):
                                for files in sources.findall('files'):
                                    #print 'File: ' + files.get('mask')
                                    if '_dma_' in files.get('mask'):
                                        #print 'DMA'
                                        if self.dmaCount > 0:
                                            if sources.get('type') == 'src':
                                                sourcePaths.append(str(sources.get('path')))
                                                sourceFiles.append(str(files.get('mask')))
                                            elif sources.get('type') == 'c_include':
                                                includePaths.append(str(sources.get('path')))
                                                includeFiles.append(str(files.get('mask')))
                                    else:
                                        if sources.get('type') == 'src':
                                            sourcePaths.append(str(sources.get('path')))
                                            sourceFiles.append(str(files.get('mask')))
                                        elif sources.get('type') == 'c_include':
                                            includePaths.append(str(sources.get('path')))
                                            includeFiles.append(str(files.get('mask')))

            #New tuple for each driver containing name and paths
            newDrvTuple = (drvName, sourcePaths[:], includePaths[:], \
                                    sourceFiles[:], includeFiles[:])

            #Append drvList with new tuple for
            self.drvList.append(newDrvTuple)
            del sourcePaths[:]
            del includePaths[:]
            del sourceFiles[:]
            del includeFiles[:]
            del newDrvTuple
            index += 1
        #print self.drvList #Debugging
        return

    def add_all_hal(self, halList):
        """ Add all HAL components to the project

        :param halList: list of HAL components to be added
        """
        root = self.parent._getRootOfManifest()
        halName = ''
        includePaths = []
        sourcePaths = []
        includeFiles = []
        sourceFiles = []
        index = 0
        while index < len(halList):
            for halPresent in root.findall('components'):
                for componentType in halPresent.findall('component'):
                    if componentType.get('type') == 'hal':
                        if componentType.get('name') == halList[index]:
                            halName = componentType.get('name')
                            # HACK: for K80 lmem_cache to lmem
                            if halName == 'lmem_cache':
                                halName = 'lmem'
                            for sources in componentType.findall('source'):
                                for files in sources.findall('files'):
                                    if sources.get('type') == 'src':
                                        if '$|device|' in sources.get('path'):
                                            tempPath = kT.string_replace(str(sources.get('path')), '$|device|', self.device[1])
                                            sourcePaths.append(tempPath)
                                        else:
                                            sourcePaths.append(str(sources.get('path')))
                                        sourceFiles.append(str(files.get('mask')))
                                    elif sources.get('type') == 'c_include':
                                        if '$|device|' in sources.get('path'):
                                            tempPath = kT.string_replace(str(sources.get('path')), '$|device|', self.device[1])
                                            includePaths.append(tempPath)
                                        else:
                                            includePaths.append(str(sources.get('path')))
                                        includeFiles.append(str(files.get('mask')))

            #New tuple for each hal component containing name and paths
            newHalTuple = (halName, sourcePaths[:], includePaths[:], \
                                    sourceFiles[:], includeFiles[:])

            #Append halList with new tuple for
            self.halList.append(newHalTuple)
            del sourcePaths[:]
            del includePaths[:]
            del sourceFiles[:]
            del includeFiles[:]
            del newHalTuple
            index += 1
        #print self.halList #Debugging
        return

    def make_main_file(self, sourcePath, includeList):
        """ Generate the main.c and main.h files for the project

        :param sourcePath: directory to which main files will be added
        :param includeList: list of drivers to be added
        """
        
        if self.parent.isNewVersion():
            self.make_main_board_template_rtos_files_new_version(sourcePath)
            return
        
        includeString = ''

        if self.useBSP == True:
            includeString += '#include "board.h"\n'
        else:
            includeString += '#include "fsl_device_registers.h"\n'

        if not self.parent.isNewVersion():
            if self.libList[0] != 'hal':
                includeString += '#include "fsl_debug_console.h"\n'
                includeString += '#include "fsl_clock_manager.h"\n'
                includeString += '#include "fsl_interrupt_manager.h"\n'
                includeString += '#include "fsl_power_manager.h"\n'
            if self.rtos != 'bm':
                includeString += '#include "fsl_os_abstraction.h"\n'

        # TODO: find more elegant approach to removing _dma_ versions of drivers from edma parts
        # Check for eDMA driver
        isEdmaPart = False
        index = 0
        while index < len(self.drvList):
            if self.drvList[index][0] == 'edma':
                isEdmaPart = True
            index += 1

        #print includeList

        #Build include string
        index = 0
        projList = self.drvList if self.libList[0] != 'hal' else self.halList
        while index < len(includeList):
            currDir = os.listdir(self.sdkPath + '/' + includeList[index])
            count = 0
            #print currDir
            while count < len(currDir):
                #Get driver includes
                subIdx = 0
                while subIdx < len(projList):
                    #print projList[subIdx][0]
                    checkString = 'fsl_' + projList[subIdx][0] + '_'
                    if checkString in currDir[count]:
                        #print currDir[count]
                        if currDir[count][-2:] == '.h':
                            if includeString.find(currDir[count]) < 0:
                                if currDir[count].find('driver') > -1:

                                    ##                Added to fix K80 application build issues                ##
                                    if currDir[count] == 'fsl_smartcard_emvsim_driver.h':
                                        includeString += '#if defined(FSL_FEATURE_SOC_EMVSIM_COUNT)\n'
                                        includeString += '#if (FSL_FEATURE_SOC_EMVSIM_COUNT >= 1)\n'

                                    if currDir[count] == 'fsl_smartcard_uart_driver.h':
                                        includeString += '#if defined(FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT)\n'
                                        includeString += '#if (FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT == 1)\n'

                                    if currDir[count] == 'fsl_smartcard_direct_driver.h':
                                        includeString += '#if USING_DIRECT_INTERFACE\n'

                                    if currDir[count] == 'fsl_smartcard_ncn8025_driver.h':
                                        includeString += '#if USING_NCN8025_INTERFACE\n'
                                    ##############################################################################

                                    if isEdmaPart == True:
                                        if currDir[count].find('_dma_') < 0:
                                            includeString += '#include "' + currDir[count] + '"\n'
                                    else:
                                        if currDir[count].find('_edma_') < 0:
                                            if currDir[count].find('_dma_') > 0:
                                                if self.dmaCount > 0:
                                                    includeString += '#include "' + currDir[count] + '"\n'
                                            else:
                                                includeString += '#include "' + currDir[count] + '"\n'

                                    ##                Added to fix K80 application build issues                ##
                                    if (currDir[count] == 'fsl_smartcard_direct_driver.h') or\
                                       (currDir[count] == 'fsl_smartcard_ncn8025_driver.h'):
                                        includeString += '#endif\n'

                                    if currDir[count] == 'fsl_smartcard_emvsim_driver.h':
                                        includeString += '#endif\n#endif\n'

                                    if currDir[count] == 'fsl_smartcard_uart_driver.h':
                                        includeString += '#endif\n#endif\n'
                                    ##############################################################################

                                if currDir[count].find('hal') > -1:
                                    if currDir[count].find('tsi_v') > -1:
                                        #print 'Current directory: ' + currDir[count]
                                        if currDir[count].find('tsi_v' + str(self.tsiVersion)) > -1:
                                            #print 'TSI version: ' + str(self.tsiVersion)
                                            includeString += '#include "' + currDir[count] + '"\n'
                                    else:
                                        includeString += '#include "' + currDir[count] + '"\n'
                    subIdx += 1
                count += 1
            index += 1

        #print includeString

        mainString = "/*\n"\
                     " * Copyright (c) " + time.strftime("%Y") + ", Freescale Semiconductor, Inc.\n"\
                     " * All rights reserved.\n"\
                     " *\n"\
                     " * Redistribution and use in source and binary forms, with or without modification,\n"\
                     " * are permitted provided that the following conditions are met:\n"\
                     " *\n"\
                     " * o Redistributions of source code must retain the above copyright notice, this list\n"\
                     " *   of conditions and the following disclaimer.\n"\
                     " *\n"\
                     " * o Redistributions in binary form must reproduce the above copyright notice, this\n"\
                     " *   list of conditions and the following disclaimer in the documentation and/or\n"\
                     " *   other materials provided with the distribution.\n"\
                     " *\n"\
                     " * o Neither the name of Freescale Semiconductor, Inc. nor the names of its\n"\
                     " *   contributors may be used to endorse or promote products derived from this\n"\
                     " *   software without specific prior written permission.\n"\
                     " *\n"\
                     " * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND\n"\
                     " * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n"\
                     " * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"\
                     " * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR\n"\
                     " * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n"\
                     " * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"\
                     " * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\n"\
                     " * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"\
                     " * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"\
                     " * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n"\
                     " *\n"
        mainString += " *\n"
        #TODO: Edit for 1.3.0 compatibility
        if (self.sdkVer == '1.2.0') or (self.sdkVer == '1.3.0'):
            mainString += " * [File Name]     main.c\n"
        if self.useBSP == True:
            mainString += " * [Platform]      " + self.board[3] + "\n"
        else:
            mainString += " * [Platform]      " + self.device[2] + "\n"
        mainString += " * [Project]       " + self.name + "\n" \
                    " * [Version]       1.00\n" \
                    " * [Author]        " + self.userName + "\n" \
                    " * [Date]          " + self.date + "\n" \
                    " * [Language]      'C'\n" \
                    " * [History]       1.00 - Original Release\n" \
                    " *\n" \
                    " */\n\n" \
                    "//-----------------------------------------------------------------------\n" \
                    "// Standard C/C++ Includes\n" \
                    "//-----------------------------------------------------------------------\n\n"
        if self.useBSP == True:
            mainString += "#include <stdio.h>\n"
        mainString += "//-----------------------------------------------------------------------\n"\
                    "// KSDK Includes\n" \
                    "//-----------------------------------------------------------------------\n"
        mainString += "#include \"main.h\"\n"
        mainString += "//-----------------------------------------------------------------------\n"\
                    "// Application Includes\n" \
                    "//-----------------------------------------------------------------------\n\n"
        mainString += "//-----------------------------------------------------------------------\n" \
                      "// Function Prototypes\n" \
                      "//-----------------------------------------------------------------------\n\n"
                      
        if not self.parent.isNewVersion():
            if self.rtos != 'bm':
                if self.rtos == 'mqx':
                    mainString += "void main_task(uint32_t param);\n"
                mainString += "void task_example(task_param_t param);\n"
        mainString += "//-----------------------------------------------------------------------\n" \
                      "// Constants\n" \
                      "//-----------------------------------------------------------------------\n\n"             
        if not self.parent.isNewVersion():
            if self.rtos != 'bm':
                if self.rtos == 'mqx':
                    mainString += "#define MAIN_TASK              8U\n\n"\
                                  "const TASK_TEMPLATE_STRUCT  MQX_template_list[] =\n"\
                                  "{\n"\
                                  "   { MAIN_TASK, main_task, 0xC00, 20, \"main_task\", MQX_AUTO_START_TASK},\n"\
                                  "   { 0L,        0L,        0L,    0L,  0L,         0L }\n"\
                                  "};\n"
                mainString += "#define TASK_EXAMPLE_PRIO            6U\n"\
                              "#define TASK_EXAMPLE_STACK_SIZE   1024U\n"
            mainString += "//-----------------------------------------------------------------------\n" \
                          "// Typedefs\n" \
                          "//-----------------------------------------------------------------------\n\n"\
                          "//-----------------------------------------------------------------------\n" \
                          "// Global Variables\n" \
                          "//-----------------------------------------------------------------------\n\n"\
                          "//-----------------------------------------------------------------------\n" \
                          "// Macros\n" \
                          "//-----------------------------------------------------------------------\n\n"
            if self.rtos != 'bm':
                mainString += "OSA_TASK_DEFINE(task_example, TASK_EXAMPLE_STACK_SIZE);\n"
        mainString += "//-----------------------------------------------------------------------\n" \
                      "// Main Function\n" \
                      "//-----------------------------------------------------------------------\n\n"
        if self.rtos == 'mqx':
            mainString += "void main_task(uint32_t param)\n"
        else:
            mainString += "int main(void)\n"
        mainString += "{\n"
        if self.useBSP == True:
            if self.rtos != 'bm':
                mainString += "\n"\
                              "    osa_status_t result = kStatus_OSA_Error;\n"
            mainString += "\n"\
                            "    // Configure board specific pin muxing\n"\
                            "    hardware_init();\n"\
                            "\n"\
                            "    // Initialize UART terminal\n"\
                            "    dbg_uart_init();\n"\
                            "\n"
            if self.rtos != 'bm':
                mainString += "    OSA_Init();\n\n"\
                              "    result = OSA_TaskCreate(task_example,\n"\
                              "                    (uint8_t *)\"example\",\n"\
                              "                    TASK_EXAMPLE_STACK_SIZE,\n"\
                              "                    task_example_stack,\n"\
                              "                    TASK_EXAMPLE_PRIO,\n"\
                              "                    (task_param_t)0,\n"\
                              "                    false,\n"\
                              "                    &task_example_task_handler);\n"\
                              "    if (result != kStatus_OSA_Success)\n"\
                              "    {\n"\
                              "        PRINTF(\"Failed to create example task\\r\\n\");\n"
                if self.rtos == 'mqx':
                    mainString += "        return;\n"
                else:
                    mainString += "        return -1;\n"
                mainString += "    }\n\n"
            else:
                mainString += "    PRINTF(\"\\r\\nRunning the " + self.name + " project.\\r\\n\");\n\n"
            if self.rtos != 'bm':
                mainString += "    OSA_Start();\n\n"
            mainString += "    for (;;)                                         // Forever loop\n" \
               "    {\n" \
               "        __asm(\"NOP\");\n"\
               "    }\n\n" \
               "\n" \
               "}\n"
               
            if not self.parent.isNewVersion():
                if self.rtos != 'bm':
                    mainString += "//-----------------------------------------------------------------------\n" \
                                  "// Task Functions\n" \
                                  "//-----------------------------------------------------------------------\n\n"\
                                  "void task_example(task_param_t param)\n"\
                                  "{\n"\
                                  "    PRINTF(\"\\r\\nRunning the " + self.name + " project.\\r\\n\");\n\n"\
                                  "    while(1)\n"\
                                  "    {\n"\
                                  "        \n"\
                                  "    }\n"\
                                  "}\n"
            mainString += "////////////////////////////////////////////////////////////////////////////////\n"\
                          "// EOF\n" \
                          "////////////////////////////////////////////////////////////////////////////////\n"
        else:
            mainString += "\n"\
               "    for (;;)                                                    // Forever loop\n" \
               "    {\n" \
               "        __asm(\"NOP\");\n"\
               "    }\n\n" \
               "\n" \
               "}\n" \
               "////////////////////////////////////////////////////////////////////////////////\n"\
               "// EOF\n" \
               "////////////////////////////////////////////////////////////////////////////////\n"

        headerString = "/*\n"\
                       " * Copyright (c) " + time.strftime("%Y") + ", Freescale Semiconductor, Inc.\n"\
                       " * All rights reserved.\n"\
                       " *\n"\
                       " * Redistribution and use in source and binary forms, with or without modification,\n"\
                       " * are permitted provided that the following conditions are met:\n"\
                       " *\n"\
                       " * o Redistributions of source code must retain the above copyright notice, this list\n"\
                       " *   of conditions and the following disclaimer.\n"\
                       " *\n"\
                       " * o Redistributions in binary form must reproduce the above copyright notice, this\n"\
                       " *   list of conditions and the following disclaimer in the documentation and/or\n"\
                       " *   other materials provided with the distribution.\n"\
                       " *\n"\
                       " * o Neither the name of Freescale Semiconductor, Inc. nor the names of its\n"\
                       " *   contributors may be used to endorse or promote products derived from this\n"\
                       " *   software without specific prior written permission.\n"\
                       " *\n"\
                       " * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND\n"\
                       " * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n"\
                       " * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"\
                       " * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR\n"\
                       " * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n"\
                       " * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"\
                       " * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\n"\
                       " * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"\
                       " * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"\
                       " * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n"\
                       " *\n"

        headerString += " *\n"
        headerString += " * [File Name]     main.h\n"
        if self.useBSP == True:
            headerString += " * [Platform]      " + self.board[3] + "\n"
        else:
            headerString += " * [Platform]      " + self.device[2] + "\n"
        headerString += " * [Project]       " + self.name + "\n" \
               " * [Version]       1.00\n" \
               " * [Author]        " + self.userName + "\n" \
               " * [Date]          " + self.date + "\n" \
               " * [Language]      'C'\n" \
               " * [History]       1.00 - Original Release\n" \
               " *\n" \
               " */\n\n" \
               "//-----------------------------------------------------------------------\n" \
               "// KSDK Includes\n" \
               "//-----------------------------------------------------------------------\n" \
               "" + includeString + "\n" \
               "////////////////////////////////////////////////////////////////////////////////\n"\
               "// EOF\n" \
               "////////////////////////////////////////////////////////////////////////////////\n"

        #Turn mainString into a c file
        with open(sourcePath + '/main.c', "wb") as f:
            f.write(mainString)
            f.close()

        #Turn headerString into a h file
        with open(sourcePath + '/main.h', "wb") as f:
            f.write(headerString)
            f.close()
    
    
    def make_main_board_template_rtos_files_new_version(self, sourcePath):
        """
        Create main.c (in quick generation also main.h) and board template - board.*, pin_mux.*, clock_config.*
        @param sourcePath: path to project 
        """

        if self.rtos == 'bm':
            mainString = Constants.QUICK_MAIN_C if self.isQuickGenerate else Constants.ADVANCED_MAIN_C
            mainString = mainString.replace(Constants.PROJECT_NAME_PLACEHOLDER, self.name)
        elif self.rtos == 'freertos':
            mainString = Constants.MAIN_FREERTOS_C
        elif self.rtos == 'ucosii':
            mainString = Constants.MAIN_UCOSII_C
        elif self.rtos == 'ucosiii':
            mainString = Constants.MAIN_UCOSIII_C
            
        
        with open(sourcePath + '/main.c', "wb") as f:
            f.write(mainString)
            f.close()

        
        if self.isQuickGenerate:
            with open(sourcePath + '/main.h', "wb") as f:
                driversName = [d[ksdkObj.NAME_KEY] for d in self.parent.getBoardFilesForBoardProjects(False, True, self.board[1], self.device[1], '') if d[ksdkObj.NAME_KEY].endswith('.h') \
                                and not d[ksdkObj.NAME_KEY].endswith('_freertos.h') and not d[ksdkObj.NAME_KEY].endswith('_ucosii.h') and not d[ksdkObj.NAME_KEY].endswith('_ucosiii.h')]
                driversIncludes = ''
                for name in driversName:
                    driversIncludes += "#include \"" + name + "\"\n"
                f.write(Constants.QUICK_MAIN_H.replace(Constants.DRIVERS_PLACE_HOLDER, driversIncludes))
                f.close()
                                 
        #add template files to the project in case it is project for processor
        if not self.isBoardProject:
            tempDict = {'board.c': Constants.BOARD_C, 'board.h':Constants.BOARD_H, 'clock_config.c':Constants.CLOCK_CONFIG_C, 'clock_config.h': Constants.CLOCK_CONFIG_H, 'pin_mux.c':Constants.PIN_MUX_C, 'pin_mux.h':Constants.PIN_MUX_H}
            for d in self.parent.getBoardFilesList():
                with open(sourcePath + '/' + d, "wb") as f:
                    f.write(tempDict[d])
                    f.close()
        else:
            listOfDictionaries = self.parent.getBoardFilesForBoardProjects(True, False, self.board[1], self.device[1], self.rtos)
            for d in listOfDictionaries:
                filePath = os.path.join(self.sdkPath, d[kSdk.LOCATION_URI_KEY])
                if os.path.isfile(filePath):
                    shutil.copyfile(filePath, os.path.join(sourcePath, d[kSdk.NAME_KEY]))
                    
        #add rtos application files
        if self.rtos == 'freertos':
            if not self.parent.isRTOSTemplateCorrect(RTOSType.FreeRTOS):
                with open(sourcePath + '/FreeRTOSConfig.h', "wb") as f:
                    f.write(Constants.FREERTOS_CONFIG_H)
                    f.close()
            else:
                for d in self.parent.getRTOSTemplateFileLocationsAndNames(RTOSType.FreeRTOS):
                    filePath = os.path.join(self.sdkPath, d[kSdk.LOCATION_URI_KEY])
                    if os.path.isfile(filePath):
                        shutil.copyfile(filePath, os.path.join(sourcePath, d[kSdk.NAME_KEY])) 
        elif self.rtos == 'ucosii':
            for d in self.parent.getRTOSTemplateFileLocationsAndNames(RTOSType.uCOSII):
                filePath = os.path.join(self.sdkPath, d[kSdk.LOCATION_URI_KEY])
                if os.path.isfile(filePath):
                    shutil.copyfile(filePath, os.path.join(sourcePath, d[kSdk.NAME_KEY]))
        elif self.rtos == 'ucosiii':
            if not self.parent.isRTOSTemplateCorrect(RTOSType.uCOSIII):
                with open(sourcePath + '/os_cfg.h', "wb") as f:
                    f.write(Constants.UCOSIII_OS_CFG_H)
                    f.close()
            for d in self.parent.getRTOSTemplateFileLocationsAndNames(RTOSType.uCOSIII):
                filePath = os.path.join(self.sdkPath, d[kSdk.LOCATION_URI_KEY])
                if os.path.isfile(filePath):
                    shutil.copyfile(filePath, os.path.join(sourcePath, d[kSdk.NAME_KEY])) 
        
                    
                

    def make_hw_file(self, sourcePath):
        """ Create hardware_init file for project

        :param sourcePath: absolute path to which hardware_init will be added
        """
        if self.parent.isNewVersion():
            return

        ports = ['PORTA_IDX', 'PORTB_IDX', 'PORTC_IDX', 'PORTD_IDX', 'PORTE_IDX']

        mainString = "/*\n"\
                     " * Copyright (c) " + time.strftime("%Y") + ", Freescale Semiconductor, Inc.\n"\
                     " * All rights reserved.\n"\
                     " *\n"\
                     " * Redistribution and use in source and binary forms, with or without modification,\n"\
                     " * are permitted provided that the following conditions are met:\n"\
                     " *\n"\
                     " * o Redistributions of source code must retain the above copyright notice, this list\n"\
                     " *   of conditions and the following disclaimer.\n"\
                     " *\n"\
                     " * o Redistributions in binary form must reproduce the above copyright notice, this\n"\
                     " *   list of conditions and the following disclaimer in the documentation and/or\n"\
                     " *   other materials provided with the distribution.\n"\
                     " *\n"\
                     " * o Neither the name of Freescale Semiconductor, Inc. nor the names of its\n"\
                     " *   contributors may be used to endorse or promote products derived from this\n"\
                     " *   software without specific prior written permission.\n"\
                     " *\n"\
                     " * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND\n"\
                     " * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n"\
                     " * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"\
                     " * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR\n"\
                     " * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n"\
                     " * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"\
                     " * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\n"\
                     " * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"\
                     " * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"\
                     " * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n"\
                     " *\n"

        mainString += " *\n" \
                     " * [File Name]     hardware_init.c\n"
        if self.useBSP == True:
            mainString += " * [Platform]      " + self.board[3] + "\n"
        else:
            mainString += " * [Platform]      " + self.device[2] + "\n"
        mainString += " * [Project]       " + self.name + "\n" \
               " * [Version]       1.00\n" \
               " * [Author]        " + self.userName + "\n" \
               " * [Date]          " + self.date + "\n" \
               " * [Language]      'C'\n" \
               " * [History]       1.00 - Original Release\n" \
               " *\n" \
               " */\n\n" \
               "//-----------------------------------------------------------------------\n" \
               "// KSDK Includes\n" \
               "//-----------------------------------------------------------------------\n" \
               "#include \"board.h\"\n"\
               "#include \"pin_mux.h\"\n"\
               "#include \"fsl_clock_manager.h\"\n"\
               "#include \"fsl_debug_console.h\"\n"\
               "//-----------------------------------------------------------------------\n" \
               "// Hardware Initialization\n" \
               "//-----------------------------------------------------------------------\n" \
               "void hardware_init(void)\n"\
               "{\n"\
               "\n"\
               "    /* enable clock for PORTs */\n"
        index = 0
        while index < self.portCount:
            mainString += "    CLOCK_SYS_EnablePortClock(" + ports[index] + ");\n"
            index += 1
        mainString += "\n"\
               "    /* Init board clock */\n"\
               "    BOARD_ClockInit();\n"\
               "}\n"\
               "////////////////////////////////////////////////////////////////////////////////\n"\
               "// EOF\n" \
               "////////////////////////////////////////////////////////////////////////////////\n"

        #Turn headerString into a h file
        with open(sourcePath + '/hardware_init.c', "wb") as f:
            f.write(mainString)
            f.close()

    def fast_build_GCC(self):
        """ Quick Generate GCC project
        """
        if self.parent.isNewVersion():
            return self._fast_build_GCC_new_version()
        #print self.sdkVer
        exampleFolderName = '/examples/'
        # Make sure the new project folder is present
        projectPath = self.sdkPath + '/' + self.parent.getDirectoryStructureHelper().getUserLinkedExamplesPath(self.board[1]) + '/' + self.name

        # Get list of files in folder
        origDir = self.sdkPath + exampleFolderName + self.board[1] + '/demo_apps/hello_world/armgcc/'
        newDir = projectPath + '/armgcc/'
        if not os.path.isdir(origDir):
            return
        armGccFiles = [f for f in os.listdir(origDir) if os.path.isfile(os.path.join(origDir, f))]
        os.makedirs(newDir)

        index = 0
        while index < len(armGccFiles):
            shutil.copyfile(origDir + armGccFiles[index], newDir + armGccFiles[index])
            index += 1

        try:
            kT.replace_name_in_file(newDir + 'CMakeLists.txt', 'hello_world', self.name)
            kT.replace_name_in_file(newDir + 'CMakeLists.txt', 'fsl_lptmr_irq.c', 'main.h')
            if self.board[1] == 'frdmk64f':
                kT.replace_name_in_file(newDir + 'CMakeLists.txt', 'CPU_MK64FN1M0VMD12', 'CPU_MK64FN1M0VLL12')
        except IOError:
            return False

        # Add driver source include paths to the project
        if not self.parent.isNewVersion():
            with open(newDir + 'CMakeLists.txt', "r+b") as f:
                newContent = ''
                for line in f:
                    if 'drivers/inc)' in line:
                        index = 0
                        while index < len(self.drvList):
                            line += '    INCLUDE_DIRECTORIES(${ProjDirPath}' + \
                                    '/../../../../../platform/drivers/src/' + \
                                    self.drvList[index][0] + ')\n'
                            index += 1
                        line += '    INCLUDE_DIRECTORIES(${ProjDirPath}/..)\n'
                        line += '    INCLUDE_DIRECTORIES(${ProjDirPath}/../board)\n'
                    newContent += line
                f.truncate(0)
                f.seek(0)
                f.write(newContent)
                f.close()

        boardFiles = ['gpio_pins.c', 'gpio_pins.h', 'pin_mux.c', 'pin_mux.h', 'board.c', 'board.h']

        # Edit board support paths
        for b in boardFiles:
            oldStr = "${ProjDirPath}/../../../" + b
            newStr = "${ProjDirPath}/../board/" + b
            kT.replace_name_in_file(newDir + 'CMakeLists.txt', oldStr, newStr)
        return True
    
    def _fast_build_GCC_new_version(self):
        """ Quick Generate GCC project for KSDK 2.0
        """
        #print self.sdkVer
        exampleFolderName = '/boards/'
        # Make sure the new project folder is present
        projectPath = self.sdkPath + '/' + self.parent.getDirectoryStructureHelper().getUserLinkedExamplesPath(self.board[1]) + '/' + self.name

        # Get list of files in folder
        origDir = self.sdkPath + exampleFolderName + self.board[1] + '/demo_apps/hello_world/armgcc/'
        newDir = projectPath + '/armgcc/'
        if not os.path.isdir(origDir):
            return
        armGccFiles = [f for f in os.listdir(origDir) if os.path.isfile(os.path.join(origDir, f))]
        os.makedirs(newDir)

        index = 0
        while index < len(armGccFiles):
            shutil.copyfile(origDir + armGccFiles[index], newDir + armGccFiles[index])
            index += 1

        try:
            kT.replace_name_in_file(newDir + 'CMakeLists.txt', 'hello_world.c', 'main.c')
            kT.replace_name_in_file(newDir + 'CMakeLists.txt', 'hello_world', self.name)
        except IOError:
            return False
        
        listOfDriverDicts = self.parent.getBoardFilesForBoardProjects(False, True, self.board[1], self.device[1], Constants.RTOS_NONE)
        linesWithDriver = ["\"${ProjDirPath}/../../../../../" + d[kSdk.LOCATION_URI_KEY] + "\"\n" for d in listOfDriverDicts]
        
        # Add driver source include paths to the project
        with open(newDir + 'CMakeLists.txt', "r+b") as f:
            newContent = ''
            for line in f:
                    #add also main.h file
                if 'main.c' in line:
                    mainHLine = line.replace('main.c', 'main.h')
                    newContent += line + mainHLine
                elif 'add_executable' in line:
                    allDrivers = ''
                    for l in linesWithDriver:
                        allDrivers += l
                    newContent += line + allDrivers
                else:
                    newContent += line
            f.truncate(0)
            f.seek(0)
            f.write(newContent)
            f.close()

        boardFiles = self.parent.getBoardFilesList()

        # Edit board support paths
        for b in boardFiles:
            oldStr = "${ProjDirPath}/../../../" + b
            newStr = "${ProjDirPath}/../board/" + b
            kT.replace_name_in_file(newDir + 'CMakeLists.txt', oldStr, newStr)
        return True 

    def proj_clone(self, cloneName, status):
        """ Clone existing KSDK project

        :param cloneName: name of the project to clone
        """       
        # in new version of KSDK it is implemented in another function
        #FIXME Radka path can be changed by user (Browse button when it is standalone version, it should not be static)
        # fix it also for 1.3, for 2.0 it is fixed      
        if self.parent.isNewVersion():
            return self._proj_clone_for_new_ksdk_version(cloneName, status)
        subDir = kT.string_replace(cloneName, '-', '/')
        exampleDirName = '/examples/'
        cloneDir = self.sdkPath + exampleDirName + self.board[1] + '/demo_apps/' + subDir
        if '/lwip/' in cloneDir:
            newTree = kT.string_replace(cloneDir, 'demo_apps', 'user_apps')
            if self.isLinked == False:
                oldLocation = self.sdkPath + '/examples'
                newLocation = self.workSpace + ('' if self.workSpace[-1:] == '/' else '/') + '/clones'
                newTree = kT.string_replace(newTree, oldLocation, newLocation)
            # Check for duplication
            if os.path.isdir(newTree):
                return False
            copy_tree(cloneDir, newTree)
        if '/usb/' in cloneDir:
            newTree = kT.string_replace(cloneDir, 'demo_apps', 'user_apps')
            if self.isLinked == False:
                oldLocation = self.sdkPath + '/examples'
                newLocation = self.workSpace + ('' if self.workSpace[-1:] == '/' else '/') + '/clones'
                #newTree = kT.string_replace(newTree, oldLocation, newLocation)
                newTree = newTree.replace(oldLocation, newLocation)
            # Check for duplication
            if os.path.isdir(newTree):
                return False
            copy_tree(cloneDir, newTree)
        chkStr = ['/usb/', '/lwip/']
        if not any(x in cloneDir for x in chkStr):
            newTree = kT.string_replace(cloneDir, 'demo_apps', 'user_apps')
            if self.isLinked == False:
                oldLocation = self.sdkPath + '/examples'
                #print self.workSpace
                newLocation = self.workSpace + ('' if (self.workSpace[-1:] == '/') else '/') + 'clones'
                #print oldLocation
                #print newLocation
                #newTree = kT.string_replace(newTree, oldLocation, newLocation)
                newTree = newTree.replace(oldLocation, newLocation)
                #print newTree
            # Check for duplication
            if os.path.isdir(newTree):
                return False
            try:
                copy_tree(cloneDir, newTree)
            except IOError:
                kT.debug_log('Error', sys.exc_info()[2])
                return 'Bad'
        if self.isLinked == False:
            self.copy_all_components(self.workSpace, cloneName, status)
            #threads = []
            #t = threading.Thread(target=self.copy_all_components, args=(self.workSpace, cloneName, status))
            #threads.append(t)
            #t.start()
        return True
    
    def _proj_clone_for_new_ksdk_version(self, cloneName, status):
        """ Clone existing KSDK project

        :param cloneName: name of the project to clone
        """           
        exampleDirName = '/boards/'
        subDir = kT.string_replace(cloneName, '-', '/')
        cloneDir = self.sdkPath + exampleDirName + self.board[1] + '/demo_apps/' + subDir
        newTree = self.workSpace + os.sep + subDir
        if os.path.isdir(newTree):
            return False
        try:
            copy_tree(cloneDir, newTree)
        except IOError:
            kT.debug_log('Error', sys.exc_info()[2])
            tkMessageBox.showinfo("Error!","An exception has occured, please restart the tool.")
            return
        if self.isLinked == False:
            self.copy_all_components(newTree, cloneName, status)
        return True

    def copy_all_components(self, destParent, cloneName, status):
        """ Copies all device related components to create a standalone project

        """
        # For new version KSDK (2.0) and higher different method is called
        if self.parent.isNewVersion():
            self.copy_all_components_for_new_ksdk_version(destParent, cloneName, status)
            return
        
        status.widgetList[31].step(5)
        status.widgetList[31].update()

        if ('rtos' in cloneName) or ('usb' in cloneName):
            libList = ['freertos', 'hal', 'mqx', 'platform', 'startup', 'ucosii', 'ucosiii']
        else:
            libList = ['hal', 'platform', 'startup']

        libPaths = []

        for l in libList:
            for t in kSdk.toolList:
                libPath = self.sdkPath + '/lib/ksdk_' + l + '_lib/'
                libPaths.append(libPath + t[1] + '/' + self.device[1][1:] + '/')

        platformPaths = []
        # CMSIS
        platformPaths.append(self.sdkPath + '/platform/CMSIS/Include')
        # Device
        platformPaths.append(self.sdkPath + '/platform/devices')
        platformPaths.append(self.sdkPath + '/platform/devices/' + self.device[1])
        platformPaths.append(self.sdkPath + '/platform/devices/' + self.device[1] + '/include')
        for t in kSdk.toolList:
            tempPath = self.sdkPath + '/platform/devices/' + self.device[1] + '/linker/' + t[2]
            if not tempPath in platformPaths:
                platformPaths.append(tempPath)
        platformPaths.append(self.sdkPath + '/platform/devices/' + self.device[1] + '/startup')
        for t in kSdk.toolList:
            tempPath = self.sdkPath + '/platform/devices/' + self.device[1] + '/startup/' + t[2]
            if not tempPath in platformPaths:
                platformPaths.append(tempPath)
        # Drivers
        platformPaths.append(self.sdkPath + '/platform/drivers/inc')
        for d in self.drvList:
            if os.path.isdir(self.sdkPath + '/platform/drivers/src/' + d[0]):
                platformPaths.append(self.sdkPath + '/platform/drivers/src/' + d[0])
                if d[0] == 'smartcard':
                    platformPaths.append(self.sdkPath + '/platform/drivers/src/' + d[0] + '/interface')
        # HAL
        platformPaths.append(self.sdkPath + '/platform/hal/inc')
        for d in self.halList:
            if os.path.isdir(self.sdkPath + '/platform/hal/src/' + d[0]):
                platformPaths.append(self.sdkPath + '/platform/hal/src/' + d[0])
                if d[0] == 'sim':
                    platformPaths.append(self.sdkPath + '/platform/hal/src/' + d[0] + '/' + self.device[1])
        # OSA
        platformPaths.append(self.sdkPath + '/platform/osa/inc')
        platformPaths.append(self.sdkPath + '/platform/osa/src')
        # System
        platformPaths.append(self.sdkPath + '/platform/system/inc')
        platformPaths.append(self.sdkPath + '/platform/system/src/clock')
        platformPaths.append(self.sdkPath + '/platform/system/src/clock/' + self.device[1])
        platformPaths.append(self.sdkPath + '/platform/system/src/hwtimer')
        platformPaths.append(self.sdkPath + '/platform/system/src/interrupt')
        platformPaths.append(self.sdkPath + '/platform/system/src/power')
        # Utilities
        platformPaths.append(self.sdkPath + '/platform/utilities/inc')
        platformPaths.append(self.sdkPath + '/platform/utilities/src')

        rtosPaths = []
        if ('rtos' in cloneName) or ('usb' in cloneName):
            # FreeRTOS paths
            rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/config/' + self.device[1][1:])
            rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/include')
            rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/port')
            rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/src')
            # MQX paths
            rtosPaths.append(self.sdkPath + '/rtos/mqx/build/atl/workspace_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/build/iar/workspace_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/build/kds/workspace_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/build/mdk/workspace_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/config/board/' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/config/mcu/' + self.device[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/config/common')
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/armgcc/mqx_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/atl/mqx_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/bat/')
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/iar/mqx_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/kds/mqx_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/mdk/mqx_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/source')
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/armgcc/mqx_stdlib_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/atl/mqx_stdlib_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/bat')
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/iar/mqx_stdlib_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/kds/mqx_stdlib_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/mdk/mqx_stdlib_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/source')
            rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/armgcc/nshell_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/atl/nshell_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/bat')
            rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/iar/nshell_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/kds/nshell_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/mdk/nshell_' + self.board[1])
            rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/source')
            # uC/OSII Paths
            rtosPaths.append(self.sdkPath + '/rtos/uCOSII')
            # uC/OSIII Paths
            rtosPaths.append(self.sdkPath + '/rtos/uCOSIII')

        status.widgetList[31].step(5)
        status.widgetList[31].update()

        usbPaths = []
        if 'usb' in cloneName:
            usbPaths.append(self.sdkPath + '/usb/adapter')
            usbPaths.append(self.sdkPath + '/usb/facility')
            usbPaths.append(self.sdkPath + '/usb/usb_core/include')
            usbPaths.append(self.sdkPath + '/usb/usb_core/hal')
            strIndices = kT.get_all_indices(cloneName, '-')
            startIdx = strIndices[0] + 1
            endIdx = strIndices[1]
            typeName = cloneName[startIdx:endIdx]
            typeInitial = ''
            if typeName != 'otg':
                #Need to check for 1.3.0
                if self.sdkVer == '1.2.0':
                    typeInitial = cloneName[startIdx:startIdx + 1]
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName)
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/include/' + self.board[1])
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/bsp/' + self.board[1])
                    className = kT.list_dirs(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/classes')
                    for c in className:
                        usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/classes/' + c)
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/controller')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/bat')
                    status.widgetList[31].step(5)
                    status.widgetList[31].update()
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                elif self.sdkVer == '1.3.0':
                    typeInitial = cloneName[startIdx:startIdx + 1]
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName)
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/include/' + self.device[1])
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/bsp/' + self.device[1])
                    className = kT.list_dirs(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/classes')
                    for c in className:
                        usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/classes/' + c)
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/controller')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/mdk/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/mdk/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/mdk/' + self.device[1] + '/')
                    status.widgetList[31].step(5)
                    status.widgetList[31].update()
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/mdk/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/mdk/' + self.device[1] + '/')
            else:
                if self.sdkVer == '1.2.0':
                    typeInitial = 'otg'
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName)
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/include/' + self.board[1])
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/bsp/' + self.board[1])
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/driver')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/include')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/otg')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/armgcc/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/atl/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/bat')
                    status.widgetList[31].step(5)
                    status.widgetList[31].update()
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/iar/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/kds/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_bm')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_freertos')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_mqx')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosii')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/build/mdk/usb' + typeInitial + '_sdk_' + self.board[1] + '_ucosiii')
                elif self.sdkVer == '1.3.0':
                    typeInitial = 'otg'
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName)
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/include/' + self.device[1])
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/bsp/' + self.device[1])
                    className = kT.list_dirs(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/classes')
                    for c in className:
                        usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/classes/' + c)
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/sources/controller')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/bm/mdk/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/freertos/mdk/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/mqx/mdk/' + self.device[1] + '/')
                    status.widgetList[31].step(5)
                    status.widgetList[31].update()
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosii/mdk/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/armgcc/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/atl/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/iar/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/kds/' + self.device[1] + '/')
                    usbPaths.append(self.sdkPath + '/usb/usb_core/' + typeName + '/lib/ucosiii/mdk/' + self.device[1] + '/')

        mWarePaths = []
        mWarePaths.append(self.sdkPath + '/middleware')
        mWarePaths.append(self.sdkPath + '/utilities')

        status.widgetList[31].step(5)
        status.widgetList[31].update()

        #print libPaths
        for l in libPaths:
            libDest = destParent + l[len(self.sdkPath):]
            if not os.path.isdir(libDest):
                os.makedirs(libDest)
            #print l
            #print libDest
            fileList = kT.list_files(l)
            for f in fileList:
                filePath = l + '/' + f
                if os.path.exists(filePath):
                    shutil.copyfile(filePath, libDest + f)
                status.widgetList[31].step(1)
                status.widgetList[31].update()

        for p in platformPaths:
            #print p
            platDest = destParent + '/' + p[len(self.sdkPath):]
            if not os.path.isdir(platDest):
                os.makedirs(platDest)
            fileList = kT.list_files(p)
            for f in fileList:
                shutil.copyfile(p + '/' + f, platDest + '/' + f)
                status.widgetList[31].step(1)
                status.widgetList[31].update()

        for r in rtosPaths:
            rtosDest = destParent + '/' + r[len(self.sdkPath):]
            try:
                copy_tree(r, rtosDest)
            except:
                kT.debug_log('Folder ' + rtosDest + ' not found.')
            status.widgetList[31].step(1)
            status.widgetList[31].update()

        for u in usbPaths:
            usbDest = destParent + '/' + u[len(self.sdkPath):]
            copy_tree(u, usbDest)
            status.widgetList[31].step(1)
            status.widgetList[31].update()

        for m in mWarePaths:
            mWareDest = destParent + '/' + m[len(self.sdkPath):]
            myThreads = []
            t = threading.Thread(target=copy_tree, args=(m, mWareDest))
            myThreads.append(t)
            mon_t = threading.Thread(target=self.my_thread_monitor, args=(myThreads, 1))
            t.start()
            mon_t.start()
            #copy_tree(m, mWareDest)
            status.widgetList[31].step(5)
            status.widgetList[31].update()

        # Copy board files
        boardFiles = kT.list_files(self.sdkPath + '/examples/' + self.board[1])
        for b in boardFiles:
            shutil.copyfile(self.sdkPath + '/examples/' + self.board[1] + '/' + b, destParent + '/clones/' + self.board[1] + '/' + b)

        # Copy Licenses and SW content registers
        shutil.copyfile(self.sdkPath  + '/LA_OPT_FSL_OPEN_3RD_PARTY_IP.htm', destParent + '/LA_OPT_FSL_OPEN_3RD_PARTY_IP.htm')
        shutil.copyfile(self.sdkPath  + '/LA_OPT_HOST_TOOL.htm', destParent + '/LA_OPT_HOST_TOOL.htm')
        status.widgetList[31].step(5)
        status.widgetList[31].update()
        #TODO: Edit for 1.3.0 compatibility
        if self.sdkVer == '1.2.0':
            try:
                shutil.copyfile(self.sdkPath  + '/SW-Content-Register-KSDK-1.2.0.txt', destParent + '/SW-Content-Register-KSDK-1.2.0.txt')
            except IOError:
                pass
            try:
                shutil.copyfile(self.sdkPath  + '/SW-Content-Register-MQX-for-KSDK-1.2.0.txt', destParent + '/SW-Content-Register-MQX-for-KSDK-1.3.0.txt')
            except IOError:
                pass
        elif self.sdkVer == '1.3.0':
            try:
                shutil.copyfile(self.sdkPath  + '/SW-Content-Register-KSDK-1.3.0.txt', destParent + '/SW-Content-Register-KSDK-1.3.0.txt')
            except IOError:
                pass
            try:
                shutil.copyfile(self.sdkPath  + '/SW-Content-Register-MQX-for-KSDK-1.3.0.txt', destParent + '/SW-Content-Register-MQX-for-KSDK-1.3.0.txt')
            except IOError:
                pass

        return
    
    def copy_all_components_for_new_ksdk_version(self, destParent, cloneName, status):
        """ Copies all device related components to create a standalone project

        """
        #destination parent is a new empty folder so it is not necessary to check whether is it possible to make new dirs
        platformFilesPaths = []
        status.widgetList[31].step(5)
        status.widgetList[31].update()
        platformDirsPaths = []
        # CMSIS
        for d in self.parent.getCMSISFiles(self.device[1]):
            filePath = d[LOCATION_URI_KEY]
            if filePath.find('CMSIS') != -1:
                platformFilesPaths.append(self.sdkPath + os.sep + filePath)
        os.makedirs(destParent + os.sep + Constants.CMSIS_FOLDER + os.sep + 'Include')
        # Device
        devicesPath = self.parent.getDirectoryStructureHelper().getDevicesDirectory(True, True)
        
        for t in kSdk.toolList:
            tempPath = self.sdkPath + devicesPath + self.device[1] + os.sep + t[2]
            if not os.path.isdir(tempPath):
                continue
            if not tempPath in platformDirsPaths:
                platformDirsPaths.append(tempPath)
            for system in self.parent.getDirectoryStructureHelper().getListOfStartupFiles(self.device[1], t[2], True):
                systemPath = self.sdkPath + system
                if not systemPath in platformFilesPaths:
                    platformFilesPaths.append(systemPath)
        
        platformFilesPaths.append(self.sdkPath + self.parent.getDirectoryStructureHelper().getDevicesDirectory(True,True) +  self.device[1] + "/fsl_device_registers.h")
        platformFilesPaths.append(self.sdkPath + self.parent.getDirectoryStructureHelper().getDevicesDirectory(True, True) + self.device[1] + os.sep + self.device[1] + ".h")
        platformFilesPaths.append(self.sdkPath + self.parent.getDirectoryStructureHelper().getDevicesDirectory(True, True) + self.device[1] + os.sep + self.device[1] + "_features.h")
        
        for d in (self.parent.getBoardFilesForBoardProjects(False, True, self.board[1], self.device[1], self.rtos) + self.parent.getDriversExcludedFromBuild(self.device[1])):
            platformFilesPaths.append(self.sdkPath + os.sep + d[kSdk.LOCATION_URI_KEY])
        os.makedirs(destParent +  os.sep + directoryStructureHelper.DEVICES_FOLDER_NAME + os.sep + self.device[1] + os.sep + Constants.DRIVERS_FOLDER)
        os.makedirs(destParent + os.sep + directoryStructureHelper.DEVICES_FOLDER_NAME + os.sep +  self.device[1] + os.sep + Constants.UTILITIES_FOLDER)

        rtosPaths = []
        if ('rtos' in cloneName) or ('usb' in cloneName):
            # FreeRTOS paths
            rtosPaths.extend([self.sdkPath + "/" + f for f in self.parent.getFreertosDirectoriesPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])
            # uC/OSII Paths
            rtosPaths.extend([self.sdkPath + "/" + f for f in self.parent.getuCOSIIDirectoriesPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])
            # uC/OSIII Paths
            rtosPaths.extend([self.sdkPath + "/" + f for f in self.parent.getuCOSIIIDirectoriesPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        
        #FIXME Radka fix it for usb if it requires some changes
        usbPaths = []

        mWarePaths = []
        mWarePaths.append(self.sdkPath + '/middleware')

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        
        for p in platformDirsPaths:
            #print p
            platDest = destParent + '/' + p[len(self.sdkPath):]
            if not os.path.isdir(platDest):
                os.makedirs(platDest)
            fileList = kT.list_files(p)
            for f in fileList:
                shutil.copyfile(p + '/' + f, platDest + '/' + f)
            status.widgetList[31].step(0.5)
            status.widgetList[31].update()

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        
        for p in platformFilesPaths:
            platDest = os.path.join(destParent, p[len(self.sdkPath) + 1:])
            shutil.copyfile(p, platDest)  

        for r in rtosPaths:
            rtosDest = destParent + '/' + r[len(self.sdkPath):]
            try:
                copy_tree(r, rtosDest)
            except:
                kT.debug_log('Folder ' + rtosDest + ' not found.')
            status.widgetList[31].step(1)
            status.widgetList[31].update()

        for u in usbPaths:
            usbDest = destParent + '/' + u[len(self.sdkPath):]
            copy_tree(u, usbDest)
            status.widgetList[31].step(1)
            status.widgetList[31].update()

        for m in mWarePaths:
            mWareDest = destParent + '/' + m[len(self.sdkPath):]
            myThreads = []
            t = threading.Thread(target=copy_tree, args=(m, mWareDest))
            myThreads.append(t)
            mon_t = threading.Thread(target=self.my_thread_monitor, args=(myThreads, 1))
            t.start()
            mon_t.start()
            #copy_tree(m, mWareDest)
            status.widgetList[31].step(5)
            status.widgetList[31].update()

        status.widgetList[31].step(5)
        status.widgetList[31].update()

        return
    
    def copy_device_components_for_new_ksdk_version(self, destParent, status):
        """ Copies all device related components to create a standalone project

        """
        status.widgetList[31].step(5)
        status.widgetList[31].update()

        platformDirsPaths = []
        filesPaths = []
        # CMSIS
        for d in self.parent.getCMSISFiles(self.device[1]):
            filePath = d[LOCATION_URI_KEY]
            if filePath.find('CMSIS') != -1:
                filesPaths.append(self.sdkPath + os.sep + filePath)
        os.makedirs(destParent + os.sep + Constants.CMSIS_FOLDER + os.sep + 'Include')
        # Device
        devicesPath = self.directoryStructureHelper.getDevicesDirectory(True, True)

        for t in self.toolChain:
            tempPath = self.sdkPath + devicesPath + self.device[1] + os.sep + t[2]
            if not tempPath in platformDirsPaths:
                platformDirsPaths.append(tempPath)
            for system in self.directoryStructureHelper.getListOfStartupFiles(self.device[1], t[2], True):
                systemPath = self.sdkPath + system
                if not systemPath in filesPaths:
                    filesPaths.append(systemPath)
        
        filesPaths.append(self.sdkPath + self.directoryStructureHelper.getDevicesDirectory(True,True) +  self.device[1] + "/fsl_device_registers.h")
        filesPaths.append(self.sdkPath + self.directoryStructureHelper.getDevicesDirectory(True, True) + self.device[1] + os.sep + self.device[1] + ".h")
        filesPaths.append(self.sdkPath + self.directoryStructureHelper.getDevicesDirectory(True, True) + self.device[1] + os.sep + self.device[1] + "_features.h")
         
        
        for d in (self.parent.getBoardFilesForBoardProjects(False, True, self.board[1], self.device[1], self.rtos) + self.parent.getDriversExcludedFromBuild(self.device[1])):
            filesPaths.append(self.sdkPath + os.sep + d[kSdk.LOCATION_URI_KEY])
        os.makedirs(destParent +  os.sep + directoryStructureHelper.DEVICES_FOLDER_NAME + os.sep + self.device[1] + os.sep + Constants.DRIVERS_FOLDER)
        os.makedirs(destParent + os.sep + directoryStructureHelper.DEVICES_FOLDER_NAME + os.sep +  self.device[1] + os.sep + Constants.UTILITIES_FOLDER)
        
        status.widgetList[31].step(5)
        status.widgetList[31].update()

        rtosDirs = []
        if self.rtos != 'bm':
            if self.rtos == 'freertos':
                filesPaths.extend([self.sdkPath + "/" + fileDict[LOCATION_URI_KEY] for fileDict in self.parent.getMapOfFreertosPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])
                rtosDirs.extend([self.sdkPath + "/" + dirPath for dirPath in self.parent.getFreertosDirectoriesPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])
            elif self.rtos == 'ucosii':
                filesPaths.extend([self.sdkPath + "/" + fileDict[LOCATION_URI_KEY] for fileDict in self.parent.getMapOfuCOSIIPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])
                rtosDirs.extend([self.sdkPath + "/" + dirPath for dirPath in self.parent.getuCOSIIDirectoriesPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])
            elif self.rtos == 'ucosiii':
                filesPaths.extend([self.sdkPath + "/" + fileDict[LOCATION_URI_KEY] for fileDict in self.parent.getMapOfuCOSIIIPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])
                rtosDirs.extend([self.sdkPath + "/" + dirPath for dirPath in self.parent.getuCOSIIIDirectoriesPaths(CortexType.NotSpecified, ToolchainType.NotSpecified, self.board[1])])

        status.widgetList[31].step(5)
        status.widgetList[31].update()

        status.widgetList[31].step(5)
        status.widgetList[31].update()

        for p in platformDirsPaths:
            #print p
            platDest = destParent + '/' + p[len(self.sdkPath):]
            if not os.path.isdir(platDest):
                os.makedirs(platDest)
            fileList = kT.list_files(p)
            for f in fileList:
                shutil.copyfile(p + '/' + f, platDest + '/' + f)
            status.widgetList[31].step(0.5)
            status.widgetList[31].update()

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        
        #create directories where files are going to be added
        for r in rtosDirs:
            platDest = destParent + '/' + r[len(self.sdkPath):]
            if not (os.path.exists(platDest) and os.path.isdir(platDest)):
                os.makedirs(platDest) 
        
        for p in filesPaths:
            platDest = os.path.join(destParent, p[len(self.sdkPath) + 1:])
            shutil.copyfile(p, platDest)


        status.widgetList[31].step(5)
        status.widgetList[31].update()
        
        return
 

    def copy_device_components(self, destParent, status):
        """ Copies all device related components to create a standalone project


        """
        # in KSDK 2.0 and higher version the different method is called because of changes in directory structure
        if self.parent.isNewVersion():
            self.copy_device_components_for_new_ksdk_version(destParent, status)
            return

        libPaths = []
        if self.rtos == 'bm':
            libPath = self.sdkPath + '/lib/ksdk_' + self.libList[0] + '_lib/'
            for t in self.toolChain:
                libPaths.append(libPath + t[1] + '/' + self.device[1][1:] + '/')
        else:
            libPath = self.sdkPath + '/lib/ksdk_' + self.rtos + '_lib/'
            for t in self.toolChain:
                libPaths.append(libPath + t[1] + '/' + self.device[1][1:] + '/')

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        #print "Copt Comp. Update 1"

        platformPaths = []
        # CMSIS
        platformPaths.append(self.sdkPath + '/platform/CMSIS/Include')
        # Device
        platformPaths.append(self.sdkPath + '/platform/devices')
        platformPaths.append(self.sdkPath + '/platform/devices/' + self.device[1])
        platformPaths.append(self.sdkPath + '/platform/devices/' + self.device[1] + '/include')
        for t in self.toolChain:
            tempPath = self.sdkPath + '/platform/devices/' + self.device[1] + '/linker/' + t[2]
            if not tempPath in platformPaths:
                platformPaths.append(tempPath)
        platformPaths.append(self.sdkPath + '/platform/devices/' + self.device[1] + '/startup')
        for t in self.toolChain:
            tempPath = self.sdkPath + '/platform/devices/' + self.device[1] + '/startup/' + t[2]
            if not tempPath in platformPaths:
                platformPaths.append(tempPath)
                
            
        # Drivers
        platformPaths.append(self.sdkPath + '/platform/drivers/inc')
        for d in self.drvList:
            if os.path.isdir(self.sdkPath + '/platform/drivers/src/' + d[0]):
                #if d[0] == 'lmem_cache':
                #    platformPaths.append(self.sdkPath + '/platform/drivers/src/lmem')
                #else:
                platformPaths.append(self.sdkPath + '/platform/drivers/src/' + d[0])
                if d[0] == 'smartcard':
                    platformPaths.append(self.sdkPath + '/platform/drivers/src/' + d[0] + '/interface')
        # HAL
        platformPaths.append(self.sdkPath + '/platform/hal/inc')
        for d in self.halList:
            if os.path.isdir(self.sdkPath + '/platform/hal/src/' + d[0]):
                platformPaths.append(self.sdkPath + '/platform/hal/src/' + d[0])
                if d[0] == 'sim':
                    platformPaths.append(self.sdkPath + '/platform/hal/src/' + d[0] + '/' + self.device[1])
        # OSA
        platformPaths.append(self.sdkPath + '/platform/osa/inc')
        platformPaths.append(self.sdkPath + '/platform/osa/src')
        # System
        platformPaths.append(self.sdkPath + '/platform/system/inc')
        platformPaths.append(self.sdkPath + '/platform/system/src/clock')
        platformPaths.append(self.sdkPath + '/platform/system/src/clock/' + self.device[1])
        platformPaths.append(self.sdkPath + '/platform/system/src/hwtimer')
        platformPaths.append(self.sdkPath + '/platform/system/src/interrupt')
        platformPaths.append(self.sdkPath + '/platform/system/src/power')
        # Utilities
        platformPaths.append(self.sdkPath + '/platform/utilities/inc')
        platformPaths.append(self.sdkPath + '/platform/utilities/src')

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        #print "Copt Comp. Update 2"

        rtosPaths = []
        if self.rtos != 'bm':
            if self.rtos == 'freertos':
                rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/config/' + self.device[1][1:])
                rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/include')
                rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/port')
                rtosPaths.append(self.sdkPath + '/rtos/FreeRTOS/src')
            elif self.rtos == 'mqx':
                tools = kT.list_dirs(self.sdkPath + '/rtos/mqx/build')
                for t in tools:
                    rtosPaths.append(self.sdkPath + '/rtos/mqx/build/' + t + '/workspace_' + self.board[1])
                rtosPaths.append(self.sdkPath + '/rtos/mqx/config/board/' + self.board[1])
                rtosPaths.append(self.sdkPath + '/rtos/mqx/config/common')
                rtosPaths.append(self.sdkPath + '/rtos/mqx/config/mcu/' + self.device[1])
                rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/bat/')
                for t in self.toolChain:
                    rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/build/' + t[1] + '/mqx_' + self.board[1])
                rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx/source')
                rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/bat')
                for t in self.toolChain:
                    rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/build/' + t[1] + '/mqx_stdlib_' + self.board[1])
                rtosPaths.append(self.sdkPath + '/rtos/mqx/mqx_stdlib/source')
                rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/bat')
                for t in self.toolChain:
                    rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/build/' + t[1] + '/nshell_' + self.board[1])
                rtosPaths.append(self.sdkPath + '/rtos/mqx/nshell/source')
            elif self.rtos == 'ucosii':
                rtosPaths.append(self.sdkPath + '/rtos/uCOSII')
            elif self.rtos == 'ucosiii':
                rtosPaths.append(self.sdkPath + '/rtos/uCOSIII')

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        #print "Copt Comp. Update 3"

        #print libPaths
        for l in libPaths:
            libDest = destParent + l[len(self.sdkPath):]
            if not os.path.isdir(libDest):
                os.makedirs(libDest)
            #print l
            #print libDest
            fileList = kT.list_files(l)
            for f in fileList:
                shutil.copyfile(l + '/' + f, libDest + f)
            # Edit library project for package needs
            self.lib_set_package(libDest)

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        #print "Copt Comp. Update 4"

        for p in platformPaths:
            #print p
            platDest = destParent + '/' + p[len(self.sdkPath):]
            if not os.path.isdir(platDest):
                os.makedirs(platDest)
            fileList = kT.list_files(p)
            for f in fileList:
                shutil.copyfile(p + '/' + f, platDest + '/' + f)
            status.widgetList[31].step(0.5)
            status.widgetList[31].update()

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        #print "Copt Comp. Update 5"

        for r in rtosPaths:
            rtosDest = destParent + '/' + r[len(self.sdkPath):]
            copy_tree(r, rtosDest)

        status.widgetList[31].step(5)
        status.widgetList[31].update()
        #print "Copt Comp. Update 6"

        # Copy Licenses and SW content registers
        #TODO: Edit for 1.3.0 compatibility
        shutil.copyfile(self.sdkPath  + '/LA_OPT_FSL_OPEN_3RD_PARTY_IP.htm', destParent + '/LA_OPT_FSL_OPEN_3RD_PARTY_IP.htm')
        shutil.copyfile(self.sdkPath  + '/LA_OPT_HOST_TOOL.htm', destParent + '/LA_OPT_HOST_TOOL.htm')
        if self.sdkVer == '1.2.0':
            try:
                shutil.copyfile(self.sdkPath  + '/SW-Content-Register-KSDK-1.2.0.txt', destParent + '/SW-Content-Register-KSDK-1.2.0.txt')
            except IOError:
                tkMessageBox.showinfo("Missing File",\
                                      "SW-Content-Register for this KSDK not found, please copy to project directory.")
            if self.rtos == 'mqx':
                try:
                    shutil.copyfile(self.sdkPath  + '/SW-Content-Register-MQX-for-KSDK-1.2.0.txt', destParent + '/SW-Content-Register-MQX-for-KSDK-1.2.0.txt')
                except IOError:
                    tkMessageBox.showinfo("Missing File",\
                                      "SW-Content-Register for MQX not found, please copy to project directory.")
        elif self.sdkVer == '1.3.0':
            try:
                shutil.copyfile(self.sdkPath  + '/SW-Content-Register-KSDK-1.3.0.txt', destParent + '/SW-Content-Register-KSDK-1.3.0.txt')
            except IOError:
                tkMessageBox.showinfo("Missing File",\
                                      "SW-Content-Register for this KSDK not found, please copy to project directory.")
            if self.rtos == 'mqx':
                try:
                    shutil.copyfile(self.sdkPath  + '/SW-Content-Register-MQX-for-KSDK-1.3.0.txt', destParent + '/SW-Content-Register-MQX-for-KSDK-1.3.0.txt')
                except IOError:
                    tkMessageBox.showinfo("Missing File",\
                                      "SW-Content-Register for MQX not found, please copy to project directory.")

        return

    def lib_set_package(self, projectPath):
        """ Configure library project for the selected package

            :param projectPath: path of lib project to edit

        """

        #print projectPath

        if 'kds' in projectPath:
            # Open cproject and edit CPU_xxx
            tree = ET.parse(projectPath + '.cproject')
            root = tree.getroot()
            for child in root.findall('storageModule'):
                for config in child.findall('cconfiguration'):
                    for module in config.findall('storageModule'):
                        if module.get('moduleId') == "cdtBuildSystem":
                            for configure in module.findall('configuration'):
                                for folder in configure.findall('folderInfo'):
                                    for toolC in folder.findall('toolChain'):
                                        for tool in toolC.findall('tool'):
                                            if tool.get('name') == "Cross ARM C Compiler":
                                                for label in tool.findall('option'):
                                                    if label.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.defs":
                                                        for options in label.findall('listOptionValue'):
                                                            if 'CPU_' in options.get('value'):
                                                                options.set('value', 'CPU_' + self.device[2])
            tree.write(projectPath + '.cproject', "UTF-8")
            kT.cdt_fix_post_xml(projectPath)
            # Open project and remove unused files
            inPackage = False
            tree = ET.parse(projectPath + '.project')
            root = tree.getroot()
            for child in root.findall('name'):
                child.text = child.text[:child.text.rfind('_')] + self.device[2]
            for child in root.findall('linkedResources'):
                for link in child.findall('link'):
                    for name in link.findall('name'):
                        for fileType in link.findall('type'):
                            if fileType.text == '1':
                                if 'drivers' in name.text:
                                    for d in self.drvList:
                                        if name.text.find(d[0]) > -1:
                                            inPackage = True
                                            break
                                elif 'hal' in name.text:
                                    for h in self.halList:
                                        if name.text.find(h[0]) > -1:
                                            inPackage = True
                                            break
                                else:
                                    inPackage = True
                        if inPackage == False:
                            #print name.text
                            child.remove(link)
                        else:
                            inPackage = False

            tree.write(projectPath + '.project', "UTF-8")
        elif 'iar' in projectPath:
            # Open ewp edit CPOU_xxx and remove unused files
            fileName = ''
            if self.rtos == 'bm':
                fileName = 'ksdk_' + self.libList[0] + '_lib'
            else:
                fileName = 'ksdk_' + self.rtos + '_lib'
            tree = ET.parse(projectPath + '/' + fileName + '.ewp')
            for elem in tree.iter(tag='option'):
                for child in elem.findall('name'):
                    if child.text == 'CCDefines':
                        for state in elem.findall('state'):
                            if 'CPU_' in state.text:
                                state.text = 'CPU_' + self.device[2]
            inPackage = False
            safeNames = ['osa', 'platform', 'hal', 'drivers', 'power', 'system', 'clock', 'interrupt', 'hwtimer']
            for elem in tree.iter(tag='group'):
                for child in elem.findall('name'):
                    #print child.text
                    for d in self.drvList:
                        if d[0] in child.text:
                            inPackage = True
                            #print d[0] + ' in driver list'
                            break
                    for h in self.halList:
                        if h[0] in child.text:
                            inPackage = True
                            #print h[0] + ' in hal list'
                            break
                    for s in safeNames:
                        if s in child.text:
                            inPackage = True
                            #print s + ' in platform'
                            break
                    if inPackage == False:
                        elem.remove(child)
                    else:
                        inPackage = False
            tree.write(projectPath + '/' + fileName + '.ewp', "UTF-8")
        elif 'mdk' in projectPath:
            # Open uvprojx edit CPOU_xxx and remove unused files
            fileName = ''
            if self.rtos == 'bm':
                fileName = 'ksdk_' + self.libList[0] + '_lib'
            else:
                fileName = 'ksdk_' + self.rtos + '_lib'
            tree = ET.parse(projectPath + '/' + fileName + '.uvprojx')
            for elem in tree.iter(tag='Cads'):
                for child in elem.findall('VariousControls'):
                    for defs in child.findall('Define'):
                        temp = defs.text
                        if 'CPU_' in temp:
                            #TODO: Make sure this edits CPU_xxx not anything else with _
                            if self.rtos != 'bm':
                                index1 = temp.find('CPU_')
                                index2 = temp[index1:].find(',')
                                temp.replace(temp[index1:index2], 'CPU_' + self.device[2])
                            else:
                                temp = temp[:temp.rfind('_') + 1] + self.device[2]
                            #print temp
                            defs.text = temp
            inPackage = False
            for elem in tree.iter(tag='Groups'):
                for child in elem.findall('Group'):
                    for name in child.findall('GroupName'):
                        if 'drivers' in name.text:
                            for d in self.drvList:
                                if d[0] in name.text:
                                    #print name.text + ' in platform.'
                                    inPackage = True
                                    break
                        if 'hal' in name.text:
                            for h in self.halList:
                                if h[0] in name.text:
                                    #print name.text + ' in platform.'
                                    inPackage = True
                                    break
                        if 'osa' in name.text:
                            #print name.text + ' in platform.'
                            inPackage = True
                        if 'system' in name.text:
                            #print name.text + ' in platform.'
                            inPackage = True
                        if inPackage == False:
                            #print name.text + ' not in platform'
                            elem.remove(child)
                        else:
                            inPackage = False
            tree.write(projectPath + '/' + fileName + '.uvprojx', "UTF-8")

        return

    @staticmethod
    def my_thread_monitor(myThreads, numThreads):
        """ Very crude thread monitor
        """
        while True:
            for t in range(numThreads):
                if myThreads[t].is_alive() == False:
                    kT.debug_log("Thread {0} complete.".format(str(myThreads[t])))
                    return

