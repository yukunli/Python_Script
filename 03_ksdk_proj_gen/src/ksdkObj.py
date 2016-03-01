"""
File:  ksdkObj.py
=================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Class for creating a KSDK object**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.5

Inheritance
+++++++++++
.. inheritance-diagram:: ksdkObj

UML
+++
.. uml:: {{/../../../src/ksdkObj.py

API
+++

"""

## USER MODULES
from ksdkTools import KsdkTools as kT
import directoryStructureHelper

## PYTHON MODULES
import os
import xml.etree.ElementTree as ET
from _elementtree import Element
from manifestMerge import ManifestMerge
from dircache import listdir
import Constants
from directoryStructureHelper import RTOSType

#: List of supported toolchains
toolList = [("GCC Makefile", "armgcc", "gcc"), \
            ("Kinetis Design Studio", "kds", "gcc"), \
            ("Atollic TrueSTUDIO", "atl", "gcc"), \
            ("IAR Embedded Workbench for ARM", "iar", "iar"), \
            ("Keil MDK-ARM", "mdk", "arm")]

#Toolchains
#Name of Keil MDK-ARM toolchain
keilMDKARMname = "Keil MDK-ARM"
#Name of Kinetis Design Studio toolchain
KDSname = "Kinetis Design Studio"
#Name of Atollic TrueSTUDIO toolchain
AtollicStudio = "Atollic TrueSTUDIO"
#Name of IAR toolchain
IARname = "IAR Embedded Workbench for ARM"

# archictecture prefix
ARCHITECTURE_PREFIX = "ARM"
#
ARCHITECTURE_M4 = 'ARM-Cortex-M4'
#
ARCHITECTURE_M0 = 'ARM-Cortex-M0'
#
GNU_TOOL_TYPE = 'GNU'
#
IAR_TOOL_TYPE = 'IAR'
# Keil
REAL_VIEW_TOOL_TYPE = 'RealView'

#
UCOSII_COMPONENT_NAME = 'ucosii'
PROJECT_TEMPLATE_TYPE='project_template'
VERSION = 'version'

LOCATION_URI_KEY = 'locationURI'
NAME_KEY = 'name'

# Prefix of old KSDK version
NEW_KSDK_PREFIX = "2."
# Prefix of supported KSDK version
SUPPORTED_KSDK_PREFIX = set(["1.2", "1.3", "2."])

# Rtos folder 
FOLDER_NAME_RTOS = "rtos"

# name for freeRTOS component
COMPONENT_NAME_FREERTOS = "FreeRTOS"

globalBoardList = []

# Helper class for finding out supported toolchains
class ToolchainType():
    # Kinetis design studio
    KinetisDesignStudio = 1
    # Keil MDK-ARM toolchain
    KeilMDK = 2
    # Atollic TrueSTUDIO toolchain
    AtollicStudio = 3
    # IAR toolchain
    IARname = 4
    # GCC project files
    ARMgcc = 5
    # Not specified
    NotSpecified = 6
    
    @staticmethod
    def getToolchainTypeBaseOnID(toolchainID):
        toolchainType = 0
        if toolchainID == "atl":
            toolchainType = ToolchainType.AtollicStudio
        if toolchainID == "iar":
            toolchainType = ToolchainType.IARname
        if toolchainID == "kds":
            toolchainType = ToolchainType.KinetisDesignStudio
        if toolchainID == "mdk":
            toolchainType = ToolchainType.KeilMDK
        if toolchainID == "armgcc":
            toolchainType = ToolchainType.ARMgcc
        return toolchainType
    
class CortexType():
    M0 = 1
    M3 = 2
    M4 = 3
    M4F = 4
    NotSpecified = 0
    
    @staticmethod
    def getCortexType(textName):
        cortex = CortexType.NotSpecified
        if 'cm0' in textName:
            cortex = CortexType.M0
        if 'cm3' in textName:
            cortex = CortexType.M3
        if 'cm4f' in textName:
            cortex = CortexType.M4F
        elif 'cm4' in textName:
            cortex = CortexType.M4
        return cortex
    
    @staticmethod
    def getArchitectureName(type, isFreertos=False):
        typeName = ''
        if type == CortexType.M0:
            typeName = 'ARM_CM0' if isFreertos else ARCHITECTURE_M0
        if type == CortexType.M3:
            typeName = 'ARM_CM3' if isFreertos else ''
        if (type == CortexType.M4) or (type == CortexType.M4F):
            typeName = 'ARM_CM4F' if isFreertos else ARCHITECTURE_M4
        return typeName
            
        
    

##################
##  KSDK Class  ##
##################
class kinetisSDK(object):

    def __init__(self, ksdkPath):
        self.path = ksdkPath
        self.version = ''
        self.brdList = []
        self.devList = []
        self.drvList = []
        self.halList = []
        self.othList = []
        self.libList = []
        self.rtosLst = []
        self.demoLst = []
        self.devPkgList = []
        self.toolchainList = set([])
        self.directoryStructureHelper = None
        self.manifestTreeRoot = None
        self.supportedBoards = []
        self.isFreertos = None
        self.isuCOSII = None
        self.isuCOSIII = None
        
    def setNewKSDKPath(self, ksdkPath):
        if ksdkPath != self.path:
            self.__init__(ksdkPath)
        
        
    def _getRootOfManifest(self):
        """
        Get root of manifest file
        @param path: String ksdkPath
        @return: xml.etree.ElementTree.Element root element of manifest
        """
        if self.manifestTreeRoot is None:
            merger = ManifestMerge(self.path)
            manifestTree = merger.getManifestDocument()
            self.manifestTreeRoot = manifestTree.getroot() if manifestTree is not None else Element('empty')
        return self.manifestTreeRoot
    
    def getListOfSupportedBoardsForDevice(self, deviceFullName):
        """
        Get list of supported boards for device full name given as input parameter
        @param  deviceFullName: full name of device (for example MK10DX128xxx10) 
        """
        if len(self.supportedBoards) == 0:
            for devices in self._getRootOfManifest().findall('devices'):
                for device in devices.findall('device'):
                    if device.get('full_name') == deviceFullName:
                        for evalution_boards in device.findall('evaluation_boards'):
                            for evaluation_board in evalution_boards.findall('evaluation_board'):
                                name = evaluation_board.get('name')
                                if name in self.get_boards():
                                    self.supportedBoards.append(evaluation_board.get('name'))
        return self.supportedBoards
    
    def getBoardInformation(self, boardID, deviceTupple):
        """
        Get tuple containing information about board (boardID, boardName, boardPackage, boardUserName)
        """ 
        for boardsPresent in self._getRootOfManifest().findall('boards'):
            for child in boardsPresent.findall('board'):
                if child.get('user_name') == boardID:
                    brdId = child.get('id')
                    brdName = child.get('name')
                    brdPkg = deviceTupple[2]
                    brdUser = child.get('user_name')
                    return (brdId, brdName, brdPkg, brdUser)
        return ()
    
    def isNewVersion(self):
        """
        Return flag whether version KSDK is at least 2.0
        """
        version = self.get_version()
        if version.find(NEW_KSDK_PREFIX) == 0:
            return True
        return False
    
    def isVersionSupported(self):
        """
        Return flag whether version of KSDK is supported by the tool
        """
        version = self.get_version()
        for prefix in SUPPORTED_KSDK_PREFIX:
            if version.find(prefix) == 0:
                return True
        return False
        
    def _initialize_supported_toolchain(self):
        """
        Get list of supported toolchain:
        """
        if len(self.toolchainList) == 0:
            if self.isNewVersion():
                for tools in self._getRootOfManifest().findall('tools'):
                    for child in tools.findall('tool'):
                        self.toolchainList.add(ToolchainType.getToolchainTypeBaseOnID(child.get('id')))
            else:
                examplesFileRoot = os.path.join(self.path, "examples");
                if os.path.isdir(examplesFileRoot):
                    exampleSubDirs = os.listdir(examplesFileRoot)
                    if len(exampleSubDirs) > 0:
                        demoAppsDir = os.path.join(examplesFileRoot, exampleSubDirs[0], "demo_apps")
                        if os.path.isdir(demoAppsDir):
                            for root, dirs, files in os.walk(demoAppsDir):
                                for d in dirs:
                                    self.toolchainList.add(ToolchainType.getToolchainTypeBaseOnID(d))
                                    
    
    def isToolchainTypeSupported(self, toolchainType = 0, device = None):
        """ Return flag whether toolchain type given as input parameter is supported in manifest
            @param toolchainType: use constant from ToolchainType class: (ToolchainType.KinetisDesignStudio, or ToolchainType.KeilMDK etc.)
            @param device Tupple of four elements describing device (for example ('MK64FN1M0xxx12', 'MK64F12', 'MK64FN1M0VLL12', True, 'cm4'))  
        """
        self._initialize_supported_toolchain()
        isSupportedForDevices = True
        #FIXME Radka load it from manifest but cache it in some way, it is too low
        if device is not None:
            isSupportedForDevices = False
            prefix = self.path + os.sep + 'devices' + os.sep + device[1] + os.sep
            pathToGCC = prefix + 'gcc'
            pathToArm = prefix + 'arm'
            pathToIar = prefix + 'iar'
            if (toolchainType == ToolchainType.KinetisDesignStudio or toolchainType == ToolchainType.AtollicStudio) and os.path.isdir(pathToGCC):
                isSupportedForDevices = True
            if (toolchainType == ToolchainType.KeilMDK) and os.path.isdir(pathToArm):
                isSupportedForDevices = True
            if (toolchainType == ToolchainType.IARname) and os.path.isdir(pathToIar):
                isSupportedForDevices = True
        return toolchainType in self.toolchainList and isSupportedForDevices
        
    
    def get_version(self):
        """ Get KSDK version from manifest file
        """
        if self.version == '':
            for child in self._getRootOfManifest().findall('api'):
                self.version = child.get('version')
        return self.version

    def get_boards(self):
        """ Use ksdk_manifest file to get supported board list
        """
        if len(self.brdList) == 0:
            for boardsPresent in self._getRootOfManifest().findall('boards'):
                for child in boardsPresent:
                    boardName = child.get('name')
                    # manifest could be wrong
                    if not (os.path.isdir(os.path.join(self.path, 'boards', boardName))):
                        continue
                    boardCheck = child.get('user_name')
                    self.brdList.append(str(boardCheck))
        return self.brdList

    def get_drivers(self):
        """ Use ksdk_manifest file to get supported platform driver list
        """
        if len(self.drvList) == 0:
            for driversPresent in self._getRootOfManifest().findall('components'):
                for child in driversPresent:
                    driverCheck = child.get('type')
                    if driverCheck == 'driver':
                        self.drvList.append(str(child.get('name')))
        return

    def get_hal(self):
        """ Use ksdk_manifest file to get support HAL list
        """
        if len(self.halList) == 0:
            for halPresent in self._getRootOfManifest().findall('components'):
                for child in halPresent:
                    halCheck = child.get('type')
                    if halCheck == 'hal':
                        self.halList.append(str(child.get('name')))
        return

    def get_libs(self):
        """ Browse lib folder to get supported library list
        """
        index = 0
        libDir = os.listdir(self.path + '/lib')
        while index < len(libDir):
            if ('hal' in libDir[index]) or ('platform' in libDir[index]) or \
               ('std' in libDir[index]) or ('startup' in libDir[index]):
                self.libList.append(libDir[index])
            else:
                self.rtosLst.append(libDir[index])
            index += 1
        return

    def get_other(self):
        """ Use ksdk_manifest file to get other supported drivers
        """
        if len(self.othList) == 0:
            for otherPresent in self._getRootOfManifest().findall('components'):
                for child in otherPresent:
                    otherCheck = child.get('type')
                    if otherCheck == 'other':
                        self.othList.append(str(child.get('name')))
        return

    def get_devices(self):
        """ Use ksdk_manifest file to get supported devices
        """
        if len(self.devList) == 0:
            for devicesPresent in self._getRootOfManifest().findall('devices'):
                for child in devicesPresent:
                    deviceCheck = child.get('full_name')
                    self.devList.append(str(deviceCheck))
        return

    def get_dev_pkg(self, deviceName):
        """ Use ksdk_manifest file to get supported device packages

        :param deviceName: name of device being used
        """
        #Clear out package list
        self.devPkgList = []
        for devicesPresent in self._getRootOfManifest().findall('devices'):
            for child in devicesPresent:
                deviceCheck = child.get('full_name')
                if deviceCheck == deviceName:
                    for devPkgs in child.findall('package'):
                        devPkgName = devPkgs.get('name')
                        self.devPkgList.append(devPkgName)
        return

    def get_projects(self, boardName):
        """ Use board and ksdk tree to list available projects

        :param boardName: name of board used to find demos

        .. todo::

            Add 1.3.0 support

        """

        if self.version == '':
            self.get_version()

        # Clear out list
        del self.demoLst[:]
        #print self.demoLst[:]

        # Populate demo list with demos to clone
        if self.isVersionSupported():
            dirChk = ['bm', 'freertos', 'mqx', 'ucosii', 'ucosiii']
            exampleDirName = '/boards/' if self.isNewVersion() else '/examples/'
            dirRoot = self.path + exampleDirName + boardName + '/demo_apps'
            #FIXME Radka if path does not exist the program fails
            self.demoLst = kT.list_dirs(dirRoot)
            if 'usb' in self.demoLst:
                self.demoLst.remove('usb')
                usbRoot = dirRoot + '/usb'
                subDir = kT.list_dirs(usbRoot)
                for dirName in subDir:
                    classDir = kT.list_dirs(usbRoot + '/' + dirName)
                    for c in classDir:
                        dList = kT.list_dirs(usbRoot + '/' + dirName + '/' + c)
                        if not any(x in dList for x in dirChk):
                            for d in dList:
                                self.demoLst.append('usb-' + dirName + '-' + c + '-' + d)
                        else:
                            self.demoLst.append('usb-' + dirName + '-' + c)
            if 'lwip' in self.demoLst:
                self.demoLst.remove('lwip')
                lwipRoot = dirRoot + '/lwip'
                subDir = kT.list_dirs(lwipRoot)
                for dirName in subDir:
                    classDir = kT.list_dirs(lwipRoot + '/' + dirName)
                    for c in classDir:
                        self.demoLst.append('lwip-' + dirName + '-' + c)
            
        return
    
    def isMQXSupported(self):
        """
        Return flag whether MQX is supported, in 2.0 and higher version it is not supported.
        1.2 and 1.3 version support MQX if there is folder rtos/mqx in ksdk installation directory. 
        """
        if self.isNewVersion():
            return False
        else:
            mqxDirPath = os.path.join(self.path, FOLDER_NAME_RTOS, "mqx")
            return os.path.exists(mqxDirPath)
        
    def _isRTOSComponentSupported(self, componentName):
        """
        Return flag wheter RTOS component with given name is supported by this KSDK
        """
        if self.isNewVersion():
            for components in self._getRootOfManifest().findall('components'):
                for component in components.findall('component'):
                    if (component.get('name').lower() == componentName.lower() and component.get('type').lower() == "os"):
                        return True
            return False
        else:
            rTOSpath = os.path.join(self.path, FOLDER_NAME_RTOS, componentName)
            return os.path.exists(rTOSpath)
        
    def isFreeRTOSSupported(self):
        """
        Return flag whether FreeRTOS is supported
        1.2 and 1.3 ksdk version support FreeRTOS if there is folder rtos/mqx in ksdk installation directory.
        2.0 and higher version support FreeRTOS if there is component with name FreeRTOS in manifest 
        """
        if self.isFreertos is None:
            self.isFreertos = self._isRTOSComponentSupported(COMPONENT_NAME_FREERTOS)
        return self.isFreertos
        
    def isuCOSIISupported(self):
        """
        Return flag whether uC/OS-II is supported
        1.2 and 1.3 ksdk version support uC/OS-II if there is folder rtos/uCOSII in ksdk installation directory.
        2.0 and higher version support uC/OS-II if there is component with name ????? in manifest 
        """
        if self.isuCOSII is None:
            self.isuCOSII = self._isRTOSComponentSupported("uCOSII")
        return self.isuCOSII
        
    def isuCOSIIISupported(self):
        """
        Return flag whether uC/OS-III is supported
        1.2 and 1.3 ksdk version support uC/OS-III if there is folder rtos/uCOSII in ksdk installation directory.
        2.0 and higher version support uC/OS-III if there is component with name ????? in manifest 
        """
        if self.isuCOSIII is None:
            self.isuCOSIII = self._isRTOSComponentSupported("uCOSIII")
        return self.isuCOSIII
    
    def getDirectoryStructureHelper(self):
        """
        Get instance of DirectoryStructureHelper class
        """
        if self.directoryStructureHelper is None:
            self.directoryStructureHelper = directoryStructureHelper.DirectoryStructureHelper(self.isNewVersion()) 
        return self.directoryStructureHelper
    
    def _getComponent(self, componentName = '', type='', device = ''):
        for components in self._getRootOfManifest().findall(Constants.COMPONENTS_TAG_NAME):
            for component in components.findall(Constants.COMPONET_TAG_NAME):
                if ((component.get('name').lower() == componentName.lower()) and (not type or component.get('type').lower() == type.lower()) and (not device or component.get('device').lower() == device.lower())):
                    return component
        
        return None
    
    def _getPathsFromElem(self, xmlElem):
        """
        @param xmlElem: xml element
        @return list of dictionaries
        """
        pathList = []
        for source in xmlElem.findall('source'):
            sourcePath = source.get('path')
            for files in source.findall('files'):
                fileName = files.get('mask')
                pathList.append({NAME_KEY: fileName, LOCATION_URI_KEY: sourcePath + "/" + fileName})
        return pathList
    
    def _getListOfFileNamesAndPaths(self, componentName = '', componentType = '', device = ''):
        pathList = []
        if componentName:
            xmlElem = self._getComponent(componentName, componentType, device)
            if xmlElem is None:
                return pathList
            else:
                pathList = self._getPathsFromElem(xmlElem)
        else:
            for componets in self._getRootOfManifest().findall(Constants.COMPONENTS_TAG_NAME):
                for component in componets.findall(Constants.COMPONET_TAG_NAME):
                    if (not componentType or component.get('type').lower() == componentType.lower()) and (not device or component.get('device').lower() == device.lower()):
                        pathList += self._getPathsFromElem(component)
        return pathList
    
    def _getFilteredRTOSPaths(self, componentName='', componentType='', architecture=CortexType.NotSpecified, toolType=ToolchainType.NotSpecified, isFreertos= False):
        #FIXME Radka rework according to the template project for each RTOS component
        alluCOSPaths = self._getListOfFileNamesAndPaths(componentName, componentType)
        selecteduCOSPaths = []
        
        toolTypeName = set([])
        if ((toolType == ToolchainType.KinetisDesignStudio) or (toolType == ToolchainType.AtollicStudio)):
            toolTypeName = {'GCC', GNU_TOOL_TYPE}
        if (toolType == ToolchainType.IARname):
            toolTypeName = {IAR_TOOL_TYPE}
        if (toolType == ToolchainType.KeilMDK):
            toolTypeName = {'RVDS', REAL_VIEW_TOOL_TYPE, 'ARM'}
            
        for dictionary in alluCOSPaths:
            filePath = dictionary[LOCATION_URI_KEY]
            if (ARCHITECTURE_PREFIX in filePath) and (architecture != CortexType.NotSpecified):
                architectureName = CortexType.getArchitectureName(architecture, isFreertos)
                if (not (architectureName in filePath)):
                    continue
            
            if toolType != ToolchainType.NotSpecified:
                # only correct files have to be added, GNU for kds or atl project, iar for iar project and real view for keil project 
                test = False
                #FIXME Radka filter files based on tag in manifest
                for t in [GNU_TOOL_TYPE, REAL_VIEW_TOOL_TYPE, IAR_TOOL_TYPE, 'ARM', 'GCC', 'RVDS']:
                    if ((t in filePath) and (not t in toolTypeName) and (((filePath.rfind(t) != filePath.rfind('ARM_')) and (filePath.rfind('ARM_') != -1)) or ((filePath.rfind(t) != filePath.rfind('ARM-')) and (filePath.rfind('ARM-') != -1) ))):
                        test = True
                        break;
                if test:
                    continue
                        
                if (toolType == ToolchainType.KeilMDK) or (toolType == ToolchainType.IARname):
                    if (filePath.find('Template') != -1) and (filePath.find('uC-LIB') == -1):
                        continue
                    #lib_def.h is included in os_cpu_c.c
                    if (filePath.find('lib_') != -1) and (filePath.find('lib_def.h') == -1) and (filePath.find('lib_cfg.h') == -1):
                        continue
                    if (filePath.find('heap_') != -1) and (filePath.find('heap_4') == -1):
                        continue
                    if componentName == UCOSII_COMPONENT_NAME:
                        commonListOfFiles = ['app_cfg.h', 'app_hooks.c', 'fsl_isr_wrapper.S', 'os_cfg.h', 'os_core.c', 'os_cpu.h', \
                                             'os_cpu_a.asm', 'os_cpu_c.c', 'os_dbg.c', 'os_flag.c', 'os_mbox.c', 'os_mem.c', 'os_mutex.c', 'os_q.c', 'os_sem.c', 'os_task.c', 'os_time.c', 'os_tmr.c', 'lib_def.h', 'cpu_def.h', 'cpu.h', 'lib_cfg.h']
                        containsCorrectFiles = False
                        for f in commonListOfFiles:
                            if filePath.endswith(f):
                                containsCorrectFiles = True
                                break
                        if not containsCorrectFiles:
                            continue
            selecteduCOSPaths.append(dictionary)
        return selecteduCOSPaths
      
    def getMapOfuCOSIIPaths(self, architecture=CortexType.NotSpecified, toolType=ToolchainType.NotSpecified, boardName=''):
        selecteduCOSIIPaths = self._getFilteredRTOSPaths(UCOSII_COMPONENT_NAME, 'os', architecture, toolType)
        return selecteduCOSIIPaths    
        
    def getuCOSIIDirectoriesPaths(self, architecture=CortexType.NotSpecified, toolType=ToolchainType.NotSpecified, boardName=''):
        setOfDictionaries = self.getMapOfuCOSIIPaths(architecture, toolType, boardName)
        setOfPaths = set([])
        for dictionary in setOfDictionaries:
            filePath = dictionary[LOCATION_URI_KEY] 
            index = filePath.rfind("/")
            directoryPath = filePath[:index]
            setOfPaths.add(directoryPath)
        return setOfPaths
    
    def getuCOSIIIDirectoriesPaths(self, architecture=CortexType.NotSpecified, toolType=ToolchainType.NotSpecified, boardName=''):
        #FIXME Radka refactor
        setOfDictionaries = self.getMapOfuCOSIIIPaths(architecture, toolType, boardName)
        setOfPaths = set([])
        for dictionary in setOfDictionaries:
            filePath = dictionary[LOCATION_URI_KEY] 
            index = filePath.rfind("/")
            directoryPath = filePath[:index]
            setOfPaths.add(directoryPath)
        return setOfPaths
    
    def getMapOfuCOSIIIPaths(self, architecture=CortexType.NotSpecified, toolType=ToolchainType.NotSpecified, boardName=''):
        selecteduCOSIIIPaths = self._getFilteredRTOSPaths('ucosiii', 'os', architecture, toolType)
        return selecteduCOSIIIPaths
    
    def getFreertosDirectoriesPaths(self, architecture=CortexType.NotSpecified, toolType=ToolchainType.NotSpecified, boardName=''):
        #FIXME Radka refactor
        setOfDictionaries = self.getMapOfFreertosPaths(architecture, toolType, boardName)
        setOfPaths = set([])
        for dictionary in setOfDictionaries:
            filePath = dictionary[LOCATION_URI_KEY] 
            index = filePath.rfind("/")
            directoryPath = filePath[:index]
            setOfPaths.add(directoryPath)
        return setOfPaths
    
    def isRTOSTemplateCorrect(self, rtosType):
        """
        @param RTOSType: type of RTOS
        @return boolean whether template for this type of rtos is correct or not 
        """
        if rtosType == RTOSType.FreeRTOS:
            comp = self._getComponent('freertos', PROJECT_TEMPLATE_TYPE)
            if comp is not None:
                version = comp.get(VERSION)
            if version != '1.0.0':
                return True
            else:
                return False
        elif rtosType == RTOSType.uCOSII:
            comp = self._getComponent('ucosii', PROJECT_TEMPLATE_TYPE)
            if comp is not None:
                version = comp.get(VERSION)
            if version != '1.0.0':
                return True
            else:
                return False
        elif rtosType == RTOSType.uCOSIII:
            comp = self._getComponent('ucosiii', PROJECT_TEMPLATE_TYPE)
            if comp is not None:
                version = comp.get(VERSION)
            if version != '1.0.0':
                return True
            else:
                return False
        else:
            return False;   
    
    def getMapOfFreertosPaths(self, architecture=CortexType.NotSpecified, toolType = ToolchainType.NotSpecified, boardName=''):
        freertos = 'freertos'
        selectedFreertosPaths = self._getFilteredRTOSPaths(freertos, 'os', architecture, toolType, True)
        return selectedFreertosPaths
    
    def getRTOSTemplateFileLocationsAndNames(self, rtosTYpe):
        """
        @param rtosType RTOSType:
        @return list of dictinaries in which there are names, and locations, only correct template files, loaded from manifest:   
        """
        if rtosTYpe == RTOSType.FreeRTOS:
            freertos = 'freertos'
            comp = self._getComponent(freertos, PROJECT_TEMPLATE_TYPE)
            if comp is not None:
                version = comp.get(VERSION)
                if version != '1.0.0':
                    return self._getListOfFileNamesAndPaths(freertos, PROJECT_TEMPLATE_TYPE)
        elif rtosTYpe == RTOSType.uCOSII:
            ucosii = 'ucosii'
            comp = self._getComponent(ucosii, PROJECT_TEMPLATE_TYPE)
            if comp is not None:
                return self._getListOfFileNamesAndPaths(ucosii, PROJECT_TEMPLATE_TYPE)
        elif rtosTYpe == RTOSType.uCOSIII:
            ucosiii = 'ucosiii'
            comp = self._getComponent(ucosiii, PROJECT_TEMPLATE_TYPE)
            if comp is not None:
                version = comp.get(VERSION)
                result = self._getListOfFileNamesAndPaths(ucosiii, PROJECT_TEMPLATE_TYPE)
                if version != '1.0.0':
                    return result
                else:
                    for d in result:
                        if d[NAME_KEY] == 'os_cfg.h':
                            result.remove(d)
                            return result
        return []
    
    def getRTOSTemplateFilesNames(self, rtosType):
        """
        @param rtosType RTOSType:
        @retun list of names of template files for given rtos 
        """
        if rtosType == RTOSType.FreeRTOS:
            return ['FreeRTOSConfig.h']
        elif rtosType == RTOSType.uCOSII:
            return ['app_cfg.h', 'app_hooks.c', 'cpu_cfg.h', 'os_cfg.h']
        elif rtosType == RTOSType.uCOSIII:
            return ['app_cfg.h', 'os_app_hooks.c', 'os_app_hooks.h', 'cpu_cfg.h', 'os_cfg.h', 'os_cfg_app.h']
        return []
    
    def getBoardFilesList(self):
        return ['board.c', 'board.h', 'pin_mux.c', 'pin_mux.h', 'clock_config.c', 'clock_config.h']
    
    def getBoardFilesForBoardProjects(self, addTemplates = True, addDrivers = True, boardName = '', device = '', rtosType = ''):
        """
        @param addTemplates: flag whether templates should be returned (board.c, board.h...etc.)
        @param addDrivers: flag whether drivers should be return   
        @param boardName: String name of board used to get files for hello_word application 
        @param device: String device name
        @return list of dictinaries in which locationURI is key to relative path to disc and name is name of file 
        """
        listOfDict = []
        if addTemplates:
            for f in self.getBoardFilesList():
                listOfDict.append({NAME_KEY: f, LOCATION_URI_KEY: 'boards/' + boardName + '/demo_apps/hello_world/' + f})
        
        if addDrivers:
            #FIXME Radka remove it when it is clear what to do with drivers
#             listOfDict += self._getListOfFileNamesAndPaths('common', 'driver', device = device)
#             listOfDict += self._getListOfFileNamesAndPaths('clock', 'driver', device = device)
#             listOfDict += self._getListOfFileNamesAndPaths('smc', 'driver', device = device)
#             listOfDict += self._getListOfFileNamesAndPaths('gpio', 'driver', device = device)
#             listOfDict += self._getListOfFileNamesAndPaths('port', 'driver', device = device)
#             listOfDict += self._getListOfFileNamesAndPaths('uart', 'driver', device = device)
#             listOfDict += self._getListOfFileNamesAndPaths('lpuart', 'driver', device = device)
#             listOfDict += self._getListOfFileNamesAndPaths('lpsci', 'driver', device = device)
            listOfDict += self._getListOfFileNamesAndPaths('', 'driver', device)
            debugConsole = [d for d in self._getListOfFileNamesAndPaths('debug_console', device = device) if d[NAME_KEY].find('fsl_debug_console') != -1 ]
            listOfDict += debugConsole
        if rtosType:
            objectToRemove = []
            for d in listOfDict:
                if (d[NAME_KEY].find('_ucosii') != -1) or (d[NAME_KEY].find('_ucosiii') != -1) or (d[NAME_KEY].find('_freertos') != -1):
                    if rtosType == Constants.RTOS_NONE:
                        objectToRemove.append(d)
                    elif (not d[NAME_KEY].endswith(rtosType + '.c')) and (not d[NAME_KEY].endswith(rtosType + '.h')):
                        objectToRemove.append(d)
            for d in objectToRemove:
                listOfDict.remove(d)
        return listOfDict
    
    
    def getDriversExcludedFromBuild(self, device):
        """
        @param device: String device name
        @return list of dictinaries in which locationURI is key to relative path to disc and name is name of file 
        """
        result = []
        return result
        #FIXME Radka remove when it is clear what to do with drivers
#         result += self._getListOfFileNamesAndPaths('', 'driver', device)
#         result += self._getListOfFileNamesAndPaths('', 'utilities', device)
#         return [r for r in result if r not in self.getBoardFilesForBoardProjects(False, True, '', device)]
    
    def getCMSISFiles(self, device = ''):
        """
        @return list of dictinaries in which locationURI is key to relative path to disc and name is name of file 
        """
        result = []
        result += self._getListOfFileNamesAndPaths('Include_common', 'CMSIS', '')
        postfix = ''
        for devS in self._getRootOfManifest().findall('devices'):
            for dev in devS.findall('device'):
                if dev.get('name') == device:
                    coreElem = dev.find('core')
                    if coreElem is not None:
                        postfix = coreElem.get('name')
        result += self._getListOfFileNamesAndPaths('Include_core_' + postfix, 'CMSIS', '')
        result += self._getListOfFileNamesAndPaths(device + '_CMSIS', 'CMSIS', '')
        return result
    
    def getSmartcardParam(self, device):
        """
        @param device String: device name (for example MKS22F12 etc.)
        @return String with name of param for smartcard or None if no param should be added
        """
        comp = self._getComponent('smartcard', 'driver', device)
        if comp is not None:
            if comp.get('version') != '2.1.0':
                return None
            if self._getComponent('smartcard_phy_emvsim', 'driver', device) is not None:
                return 'USING_PHY_EMVSIM'
            if self._getComponent('smartcard_phy_ncn8025', 'driver', device) is not None:
                return 'USING_PHY_NCN8025'
            if self._getComponent('smartcard_phy_gpio', 'driver', device) is not None:
                return 'USING_PHY_GPIO'
        return None

        
         
            
        
        
             
