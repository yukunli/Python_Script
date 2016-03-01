'''
Created on Dec 9, 2015

@author: B49736
'''
## USER MODULES
from ksdkTools import KsdkTools as kT
from ksdkProj import ksdkProjClass
import mdkFiles as mF
import ksdkKdsNew
import ksdkObj
from ksdkObj import CortexType, ToolchainType
import ksdkIarNew

## PYTHON MODULES
import copy
import os
import xml.etree.ElementTree as ET
import Constants
from test.test_linecache import FILENAME
from directoryStructureHelper import RTOSType

## Important ewp tags
CDEFINES = {'name': 'Define', 'state': []}
CDEFINES_USB = {'name': 'Define', 'state': ['_DEBUG=1']}
CINCLUDES = {'name': 'IncludePath', 'state': []}
ASMDEFINES = {'name': 'ADefines', 'state': ['DEBUG']}
ASMINCLUDES = {'name': 'AUserIncludes', 'state': []}
LINKOUT = {'name': 'OutputName', 'state': ''}
LINKDEFINES = {'name': 'Misc', 'state': ['__stack_size__=', '__heap_size__=']}
LINKDEFINES_USB = {'name': 'Misc', \
                  'state': ['__ram_vector_table__=1', '__stack_size__=', '__heap_size__=']}
LINKSCF = {'name': 'ScatterFile', 'state': []}


PROJ_STARTUP =\
{'GroupName': 'startup',\
  'FileName': ['startup_xxx.s', \
               'system_xxx.c', \
               'system_xxx.h', \
               ksdkKdsNew.LINKER_NAME_CONSTANT],\
  'FileType': ['2', '1', '5', '5'],
  'FilePath': ['devices/xxx/arm/startup_xxx.s', \
               'devices/xxx/system_xxx.c', \
               'devices/xxx/system_xxx.h', \
               'devices/xxx/arm/' + ksdkKdsNew.LINKER_NAME_CONSTANT]
}

TEMPLATES = {'GroupName': ksdkKdsNew.BOARD_FOLDER_NAME}
DRIVERS = {'GroupName': Constants.DRIVERS_FOLDER}
UTILITIES = {'GroupName': Constants.UTILITIES_FOLDER}

FILENAME = 'FileName'
FILEPATH = 'FilePath'
FILETYPE = 'FileType'


class KsdkMdkNew(object):
    """ Class for generating Keil MDK-ARM projects

        .. todo:: Edit class to make it a child of ksdkProjClass
    """
    def __init__(self, ksdkProj):
        """ Init class

        :param ksdkProj: Instance of a KSDK project
        """

        self.parent = ksdkProj.workSpace
        self.userName = ksdkProj.userName
        self.date = ksdkProj.date
        self.name = ksdkProj.name
        self.isLinked = ksdkProj.isLinked
        self.device = ksdkProj.device
        self.parentProject = ksdkProj

        self.projRelPath = ''

        ## Determine if this is a USB or standard project
        self.projType = 'usb' if ksdkProj.useUSB else 'std'

        # Create local copies of the tag dictionaries
        if self.projType == 'std':
            self.cDefines = copy.deepcopy(CDEFINES)
            self.linkDefines = copy.deepcopy(LINKDEFINES)
        else:
            self.cDefines = copy.deepcopy(CDEFINES_USB)
            self.linkDefines = copy.deepcopy(LINKDEFINES_USB)
            #self.linkLibs = copy.deepcopy(LINKLIBS_USB)

        self.cIncludes = copy.deepcopy(CINCLUDES)
        self.linkOut = copy.deepcopy(LINKOUT)
        self.linkScf = copy.deepcopy(LINKSCF)
        self.asmDefines = copy.deepcopy(ASMDEFINES)
        self.asmIncludes = copy.deepcopy(ASMINCLUDES)
        
        #add board templates
        TEMPLATES[FILENAME] = [n for n in self.parentProject.parent.getBoardFilesList()]
        TEMPLATES[FILEPATH] = ['../' + n for n in TEMPLATES[FILENAME]]
        TEMPLATES[FILETYPE] = [('5' if n.endswith('.h') else '1') for n in TEMPLATES[FILENAME]]
        self.templates = TEMPLATES
            
        #add drivers
        excludedDriversDicts = self.parentProject.parent.getDriversExcludedFromBuild(device = ksdkProj.device[1])
        excludedDriversNameList = [d[ksdkObj.NAME_KEY] for d in excludedDriversDicts]
        allDriversListOfDicts = self.parentProject.parent.getBoardFilesForBoardProjects(False, True, boardName = self.parentProject.board[1], device = ksdkProj.device[1], rtosType = ksdkProj.rtos) + excludedDriversDicts
        DRIVERS[FILEPATH] = [d[ksdkObj.LOCATION_URI_KEY] for d in allDriversListOfDicts if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.DRIVERS_FOLDER) != -1)]
        DRIVERS[FILENAME] = [d[ksdkObj.NAME_KEY] for d in allDriversListOfDicts if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.DRIVERS_FOLDER) != -1)]
        DRIVERS[FILETYPE] = [('5' if n.endswith('.h') else '1') for n in DRIVERS[FILENAME]]
        DRIVERS[ksdkIarNew.EXCLUDED_LIST] = [n for n in DRIVERS[FILENAME] if n in excludedDriversNameList]
        self.drivers = DRIVERS
        
        #add utilities
        UTILITIES[FILEPATH] = [d[ksdkObj.LOCATION_URI_KEY] for d in allDriversListOfDicts if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.UTILITIES_FOLDER) != -1)]
        UTILITIES[FILENAME] = [d[ksdkObj.NAME_KEY] for d in allDriversListOfDicts if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.UTILITIES_FOLDER) != -1)]
        UTILITIES[FILETYPE] = [('5' if n.endswith('.h') else '1') for n in UTILITIES[FILENAME]]
        UTILITIES[ksdkIarNew.EXCLUDED_LIST] = [n for n in UTILITIES[FILENAME] if n in excludedDriversNameList]
        self.utilities = UTILITIES
        

        self.projStartup = copy.deepcopy(PROJ_STARTUP)
        
        PROJ_SOURCES = {'GroupName': 'sources','FileName': ['main.c'],'FileType': ['1'],'FilePath': ['../main.c']}

        if self.parentProject.isQuickGenerate:
            PROJ_SOURCES[FILENAME].append('main.h')
            PROJ_SOURCES[FILETYPE].append('5')
            PROJ_SOURCES[FILEPATH].append('../main.h')
        
        listOfCMSISDict = self.parentProject.parent.getCMSISFiles(ksdkProj.device[1])
        cmsisFileNames = [d[ksdkObj.NAME_KEY] for d in listOfCMSISDict]
        cmsisFileTypes = ["1" if f.endswith(".c") else "5" for f in cmsisFileNames]
        cmsisFilePaths = [d[ksdkObj.LOCATION_URI_KEY] for d in listOfCMSISDict]
        
        PROJ_CMSIS =\
        {'GroupName': 'CMSIS', 'FileName': cmsisFileNames, 'FileType': cmsisFileTypes, 'FilePath': cmsisFilePaths
        }
        
        self.projCMSISFiles = PROJ_CMSIS
        
        fileTypeList = []
        
        listOfDicts = []
        folderName = ''
        
        #FIXME Radka refactor
        
        self.archType = CortexType.getCortexType(self.device[4])
        toolType = ToolchainType.KeilMDK
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                listOfDicts = self.parentProject.parent.getMapOfFreertosPaths(self.archType, toolType, self.parentProject.board[1])
                folderName = ksdkKdsNew.FREERTOS_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.FreeRTOS):
                    PROJ_SOURCES[FILENAME].append(name)
                    PROJ_SOURCES[FILETYPE].append('1' if name.endswith('.c') else '5')
                    PROJ_SOURCES[FILEPATH].append('../' + name)
            elif ksdkProj.rtos == 'ucosii':
                listOfDicts = self.parentProject.parent.getMapOfuCOSIIPaths(self.archType, toolType, self.parentProject.board[1])
                folderName = ksdkKdsNew.UCOSII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSII):
                    PROJ_SOURCES[FILENAME].append(name)
                    PROJ_SOURCES[FILETYPE].append('1' if name.endswith('.c') else '5')
                    PROJ_SOURCES[FILEPATH].append('../' + name)
            elif ksdkProj.rtos == 'ucosiii':
                listOfDicts = self.parentProject.parent.getMapOfuCOSIIIPaths(self.archType, toolType, self.parentProject.board[1])
                folderName = ksdkKdsNew.UCOSIII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSIII):
                    PROJ_SOURCES[FILENAME].append(name)
                    PROJ_SOURCES[FILETYPE].append('1' if name.endswith('.c') else '5')
                    PROJ_SOURCES[FILEPATH].append('../' + name)
                
        
        self.projSources = copy.deepcopy(PROJ_SOURCES)
        
        filePathList = [dictionary[ksdkObj.LOCATION_URI_KEY] for dictionary in listOfDicts]
        fileNameList = [dictionary[ksdkObj.NAME_KEY] for dictionary in listOfDicts]
        for dictionary in listOfDicts:
            if dictionary[ksdkObj.NAME_KEY].endswith('.c'):
                fileTypeList.append('1')
            elif dictionary[ksdkObj.NAME_KEY].endswith('.h'):
                fileTypeList.append('5')
            else:
                fileTypeList.append('2')
        
        self.projRtos = {'GroupName': folderName, 'FileName':fileNameList, 'FileType':fileTypeList, 'FilePath':filePathList }

        #self.wsProjects = copy.deepcopy(WKSPACE_PROJECTS)

        return

    def gen_proj(self, ksdkProj):
        """ Generate the uvprojx files for Keil project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        mdkPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/mdk'

        relPath = ''
        if self.isLinked:
            tempStr = kT.get_rel_path(mdkPath, ksdkProj.sdkPath) + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../'

        self.projRelPath = relPath

        ## Configure linker option
        self.linkScf['state'] = self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getLinkerPath(ksdkProj.device, 'arm', False)

        ## Set a define for the device
        self.cDefines['state'].append('CPU_' + ksdkProj.device[2])
        
        if ksdkProj.rtos != 'bm':
            param = self.parentProject.parent.getSmartcardParam(ksdkProj.device[1])
            if param is not None:
                self.cDefines['state'].append(param)
            if ksdkProj.rtos == 'freertos':
                self.cDefines['state'].append('FSL_RTOS_FREE_RTOS')
            elif ksdkProj.rtos == 'ucosii':
                self.cDefines['state'].append('FSL_RTOS_UCOSII')
            elif ksdkProj.rtos == 'ucosiii':
                self.cDefines['state'].append('FSL_RTOS_UCOSIII')

        ## Add C include paths necessary for project
        self.cIncludes['state'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getCMSISIncludeDirectory(False))
         
        self.cIncludes['state'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory())
        self.cIncludes['state'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1])
        self.cIncludes['state'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1] + os.sep + Constants.DRIVERS_FOLDER)
        self.cIncludes['state'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1] + os.sep + Constants.UTILITIES_FOLDER)
        
        self.cIncludes['state'].append("../../")
        
        # in project root, there are application files in case of rtos, so it has to be added to cIncludes
        self.cIncludes['state'].append("../")

        # Add rtos paths
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.cIncludes['state'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getFreertosDirectoriesPaths(self.archType, ToolchainType.KeilMDK, self.parentProject.board[1]))
                #FIXME Radka find out why
                self.asmIncludes['state'].append('..')
            elif ksdkProj.rtos == 'ucosii':
                self.cIncludes['state'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getuCOSIIDirectoriesPaths(self.archType, ToolchainType.KeilMDK, self.parentProject.board[1]))
            elif ksdkProj.rtos == 'ucosiii':
                self.cIncludes['state'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getuCOSIIIDirectoriesPaths(self.archType, ToolchainType.KeilMDK, self.parentProject.board[1]))

        # Add relative paths to files
        prePend = self.projRelPath + '{0}'
        self.projStartup['FileName'] = [f.replace('xxx', ksdkProj.device[1]) for f in self.projStartup['FileName']]
        self.projStartup['FilePath'] = [f.replace('xxx', ksdkProj.device[1]) for f in self.projStartup['FilePath']]
        
        self.projStartup['FileName'] = [f.replace(ksdkKdsNew.LINKER_NAME_CONSTANT, ksdkProj.device[0] + '_flash.scf') for f in self.projStartup['FileName']]
        self.projStartup['FilePath'] = [f.replace(ksdkKdsNew.LINKER_NAME_CONSTANT, ksdkProj.device[0] + '_flash.scf') for f in self.projStartup['FilePath']]
        
        for d in [self.projCMSISFiles, self.projStartup, self.drivers, self.utilities]:
            d[FILEPATH] = [prePend.format(f) for f in d[FILEPATH]]

        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                index = 0
                while index < len(self.projRtos['FilePath']):
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'xxx',\
                                                ksdkProj.device[1][1:])
                    self.projRtos['FilePath'][index] = self.projRelPath + self.projRtos['FilePath'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.projRtos['FilePath']):
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'ccc',\
                                                archType)
                    self.projRtos['FilePath'][index] = self.projRelPath + self.projRtos['FilePath'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosiii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.projRtos['FilePath']):
                    self.projRtos['FilePath'][index] = kT.string_replace(self.projRtos['FilePath'][index],\
                                                'ccc',\
                                                archType)
                    self.projRtos['FilePath'][index] = self.projRelPath + self.projRtos['FilePath'][index]
                    index += 1

        kT.debug_log(self.projStartup['FileName'])
        kT.debug_log(self.projStartup['FilePath'])


        projMem = self.get_memory_loc(ksdkProj)
        #print 'Memory loc/size: ' + str(projMem)

        peDebug = "PEMicro\\Pemicro_ArmCortexInterface.dll"
        cmDebug = "BIN\\CMSIS_AGDI.dll"

        tree = ET.ElementTree(ET.fromstring(mF.mdk_formatted_uvprojx))
        for elem in tree.iter(tag='TargetName'):
            if 'Debug' in elem.text:
                elem.text = self.name + ' Debug'
            else:
                elem.text = self.name + ' Release'
        for elem in tree.iter(tag='Device'):
            elem.text = self.device[0]
        for elem in tree.iter(tag='OutputName'):
            elem.text = self.name + '.out'
        for elem in tree.iter(tag='Driver'):
            elem.text = cmDebug if (self.device[4] == 'cm4') else peDebug
        for elem in tree.iter(tag='AdsCpuType'):
            elem.text = "\"Cortex-M4\"" if (self.device[4] == 'cm4') else "\"Cortex-M0+\""
        for elem in tree.iter(tag='RvdsVP'):
            elem.text = '2' if self.device[3] else '1'
        for elem in tree.iter(tag='Ir1Chk'):
            elem.text = '1'
        for elem in tree.iter(tag='Im1Chk'):
            elem.text = '1'
        for elem in tree.iter(tag='Im2Chk'):
            elem.text = '0' if (projMem[4] == '') else '1'
        for elem in tree.iter(tag='IRAM'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[2]
            for child in elem.findall('Size'):
                child.text = projMem[3]
        for elem in tree.iter(tag='IROM'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[0]
            for child in elem.findall('Size'):
                child.text = projMem[1]
        for elem in tree.iter(tag='OCR_RVCT4'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[0]
            for child in elem.findall('Size'):
                child.text = projMem[1]
        for elem in tree.iter(tag='OCR_RVCT9'):
            for child in elem.findall('StartAddress'):
                child.text = projMem[2]
            for child in elem.findall('Size'):
                child.text = projMem[3]
        for elem in tree.iter(tag='OCR_RVCT10'):
            for child in elem.findall('StartAddress'):
                child.text = '0x0' if (projMem[4] == '') else projMem[4]
            for child in elem.findall('Size'):
                child.text = '0x0' if (projMem[5] == '') else projMem[5]
        for elem in tree.iter(tag='Cads'):
            for child in elem.findall('VariousControls'):
                for defs in child.findall('Define'):
                    temp = defs.text
                    for d in self.cDefines['state']:
                        temp += ', ' + d
                    defs.text = temp
                for incl in child.findall('IncludePath'):
                    temp = incl.text
                    for i in self.cIncludes['state']:
                        temp += '; ' + i
                    incl.text = temp
        for elem in tree.iter(tag='Aads'):
            if ksdkProj.rtos == 'freertos':
                for child in elem.findall('VariousControls'):
                    for incl in child.findall('IncludePath'):
                        incl.text = self.asmIncludes['state'][0]
        for elem in tree.iter(tag='ScatterFile'):
            elem.text = self.linkScf['state']
        for elem in tree.iter(tag='Groups'):   
            listOfDicts = [self.projStartup, self.projCMSISFiles, self.drivers, self.utilities, self.templates, self.projSources]
            if ksdkProj.rtos != 'bm':
                listOfDicts.append(self.projRtos)                
            for d in listOfDicts:
                group = ET.SubElement(elem, 'Group')
                name = ET.SubElement(group, 'GroupName')
                name.text = d['GroupName']
                files = ET.SubElement(group, 'Files')
                index = 0
                while index < len(d['FileName']):
                    newFile = ET.SubElement(files, 'File')
                    fileName = ET.SubElement(newFile, 'FileName')
                    fileType = ET.SubElement(newFile, 'FileType')
                    filePath = ET.SubElement(newFile, 'FilePath')
                    fileNameText = d['FileName'][index]
                    fileName.text = fileNameText
                    fileType.text = d['FileType'][index]
                    filePath.text = d['FilePath'][index]
                    #add flag to drivers which should be excluded
                    if (d == self.drivers) or (d == self.utilities):
                        if fileNameText.endswith('.c'):
                            dictToFindExcludedDrivers = self.drivers if d == self.drivers else self.utilities
                            if fileNameText in dictToFindExcludedDrivers[ksdkIarNew.EXCLUDED_LIST]:
                                fileOption = ET.SubElement(newFile, 'FileOption')
                                commonProperty = ET.SubElement(fileOption, 'CommonProperty')
                                includeInBuild = ET.SubElement(commonProperty, 'IncludeInBuild')
                                alwaysBuild = ET.SubElement(commonProperty, 'AlwaysBuild')
                                includeInBuild.text = 0
                                alwaysBuild.text =0
                    index += 1

        root = tree.getroot()
        prettyRoot = kT.pretty_xml(root, "UTF-8")

        # Write data to file
        if not os.path.isdir(mdkPath):
            os.makedirs(mdkPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(mdkPath + '/' + self.name + '.uvprojx', "UTF-8")

        if 'MKL' in self.device[0]:
            setPath = mdkPath + '/pemicro_connection_settings.ini'
            setContent = mF.pemicro_connection_settings_ini
            setContent = kT.string_replace(setContent, 'dev_name', self.device[0][1:].replace('xxx', 'M'))
            with open(setPath, 'wb+') as f:
                f.write(setContent)
                f.close()

        return

    def gen_wkspace(self, ksdkProj):
        """ Generate the uvmpw files for Keil project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        mdkPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/mdk'

        relPath = ''
        if self.isLinked:
            tempStr = ksdkProj.sdkPath + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../'

        self.projRelPath = relPath
# 
        tree = ET.ElementTree(ET.fromstring(mF.mdk_formatted_uvmpw))
# 
        root = tree.getroot()

        prettyRoot = kT.pretty_xml(root, "UTF-8")

        # Write data to file
        if not os.path.isdir(mdkPath):
            os.makedirs(mdkPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(mdkPath + '/' + self.name + '.uvmpw', "UTF-8")

        return


    def get_memory_loc(self, ksdkProj):
        """ Get memory local and return tuple of memory information from scatter file
        """

        scatPath = ksdkProj.sdkPath + self.parentProject.parent.getDirectoryStructureHelper().getLinkerPath(ksdkProj.device, 'arm', True)

        textStart = ''
        textSize = ''
        dataStart1 = ''
        dataSize1 = ''
        dataStart2 = ''
        dataSize2 = ''

        with open(scatPath, 'rb') as f:
            for newLine in f:
                if '#define m_interrupts_start' in newLine:
                    temp = newLine.rfind('0x')
                    textStart = newLine[temp:(temp + 10)]
                if '#define m_text_size' in newLine:
                    #print newLine
                    temp = newLine.rfind('0x')
                    #print 'Text size line: ' + str(temp)
                    #print 'Text size: ' + newLine[temp:temp + 10]
                    tempInt = int(newLine[temp:temp + 10], 16)
                    #print 'Text size int: ' + str(tempInt)
                    tempInt += int("0x410", 16)
                    textSize = hex(tempInt)
                if '#define m_interrupts_ram_start' in newLine:
                    temp = newLine.rfind('0x')
                    dataStart1 = newLine[temp:(temp + 10)]
                if '#define m_data_2_start' in newLine:
                    temp = newLine.rfind('0x')
                    dataStart2 = newLine[temp:(temp + 10)]
                if '#define m_data_size' in newLine:
                    temp = newLine.rfind('0x')
                    dataSize1 = newLine[temp:(temp + 10)]
                if '#define m_data_2_size' in newLine:
                    temp = newLine.rfind('0x')
                    dataSize2 = newLine[temp:(temp + 10)]
            f.close()

        return (textStart, textSize, dataStart1, dataSize1, dataStart2, dataSize2)
