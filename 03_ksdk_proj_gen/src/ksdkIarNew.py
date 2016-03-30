'''
Created on Dec 9, 2015

@author: B49736
'''

## USER MODULES
from ksdkTools import KsdkTools as kT
from ksdkProj import ksdkProjClass
import iarFiles as iF
import ksdkObj
import ksdkKdsNew
from ksdkObj import CortexType, ToolchainType, LOCATION_URI_KEY

## PYTHON MODULES
import copy
import os
import xml.etree.ElementTree as ET
import ksdkKdsNew
from ksdkKdsNew import KsdkKdsNew
import Constants
from directoryStructureHelper import RTOSType


## Important ewp tags
CDEFINES = {'name': 'CCDefines', 'state': []}
CDEFINES_USB = {'name': 'CCDefines', 'state': ['_DEBUG=1']}
CINCLUDES = {'name': 'CCIncludePath2', 'state': []}
ASMDEFINES = {'name': 'ADefines', 'state': ['DEBUG']}
ASMINCLUDES = {'name': 'AUserIncludes', 'state': []}
LINKOUT = {'name': 'IlinkOutputFile', 'state': '.out'}
LINKDEFINES = {'name': 'IlinkConfigDefines', 'state': ['__stack_size__=', '__heap_size__=']}
LINKDEFINES_USB = {'name': 'IlinkConfigDefines', \
                  'state': ['__ram_vector_table__=1', '__stack_size__=', '__heap_size__=']}
LINKICF = {'name': 'IlinkIcfFile', 'state': ['.icf']}
LINKLIBS_USB = {'name': 'IlinkAdditionalLibs', \
               'state': ['lib/ksdk_xxx_lib/iar/ddd/debug/libksdk_xxx.a', \
                         'usb/usb_core/device/build/iar/usbd_sdk_yyy_zzz/debug/libusbd_zzz.a', \
                         'usb/usb_core/device/build/iar/usbh_sdk_yyy_zzz/debug/libusbh_zzz.a']}

EWP_STARTUP =\
{'name': 'startup',\
 'file': ['devices/' + ksdkKdsNew.DEVICE_NAME_CONSTANT + '/iar/startup_xxx.s', \
          'devices/' + ksdkKdsNew.DEVICE_NAME_CONSTANT + '/system_' + ksdkKdsNew.DEVICE_NAME_CONSTANT + '.c', \
          'devices/' + ksdkKdsNew.DEVICE_NAME_CONSTANT + '/system_' + ksdkKdsNew.DEVICE_NAME_CONSTANT + '.h', \
          ]
}

PROJECT_DIRS = '$PROJ_DIR$'

NAME_KEY_IN_DICT = 'name'
FILE_KEY_IN_DICT = 'file'
EXCLUDED_LIST = 'excluded'


TEMPLATES ={NAME_KEY_IN_DICT: ksdkKdsNew.BOARD_FOLDER_NAME}

DRIVERS = {NAME_KEY_IN_DICT: Constants.DRIVERS_FOLDER}

UTILITIES = {NAME_KEY_IN_DICT: Constants.UTILITIES_FOLDER}

EWW_BATCH_ALL =\
{
    'name': 'all',
    'member': [{'project': '', 'configuration': 'Release'},\
               {'project': '', 'configuration': 'Debug'}]
}

EWW_BATCH_DBG =\
{
    'name': 'Debug',
    'member': [{'project': '', 'configuration': 'Debug'}]
}

EWW_BATCH_RLS =\
{
    'name': 'Release',
    'member': [{'project': '', 'configuration': 'Release'}]
}

EWW_PROJECTS = {'path': []}

class KsdkIarNew(object):
    """ Class for generating IAR EWARM projects

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
        self.wsRelPath = ''

        ## Determine if this is a USB or standard project
        self.projType = 'usb' if ksdkProj.useUSB else 'std'

        # Create local copies of the tag dictionaries
        if self.projType == 'std':
            self.cDefines = copy.deepcopy(CDEFINES)
            self.linkDefines = copy.deepcopy(LINKDEFINES)
        else:
            self.cDefines = copy.deepcopy(CDEFINES_USB)
            self.linkDefines = copy.deepcopy(LINKDEFINES_USB)
            self.linkLibs = copy.deepcopy(LINKLIBS_USB)

        self.cIncludes = copy.deepcopy(CINCLUDES)
        self.asmDefines = copy.deepcopy(ASMDEFINES)
        self.asmIncludes = copy.deepcopy(ASMINCLUDES)
        self.linkOut = copy.deepcopy(LINKOUT)
        self.linkIcf = copy.deepcopy(LINKICF)
        
        #add board templates
        TEMPLATES['file'] = [PROJECT_DIRS + '/../' + t for t in self.parentProject.parent.getBoardFilesList()]
            
        #add drivers
        allDriversListOfDicts = self.parentProject.parent.getBoardFilesForBoardProjects(False, True, boardName = self.parentProject.board[1], device = ksdkProj.device[1], rtosType = ksdkProj.rtos) + self.parentProject.parent.getDriversExcludedFromBuild(device = ksdkProj.device[1])
        allExcludedDriversPaths = [d[ksdkObj.LOCATION_URI_KEY] for d in self.parentProject.parent.getDriversExcludedFromBuild(device = ksdkProj.device[1])]
        DRIVERS[FILE_KEY_IN_DICT] = [d[ksdkObj.LOCATION_URI_KEY] for d in allDriversListOfDicts if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.DRIVERS_FOLDER) != -1)]
        DRIVERS[EXCLUDED_LIST] = [(True if f in allExcludedDriversPaths else False) for f in DRIVERS[FILE_KEY_IN_DICT]]
        UTILITIES[FILE_KEY_IN_DICT] = [d[ksdkObj.LOCATION_URI_KEY] for d in allDriversListOfDicts if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.UTILITIES_FOLDER) != -1)]
        UTILITIES[EXCLUDED_LIST] = [(True if f in allExcludedDriversPaths else False) for f in UTILITIES[FILE_KEY_IN_DICT]]
        
        self.templates = TEMPLATES 
        self.drivers = DRIVERS
        self.utilities = UTILITIES
        self.linkerFile = 'devices/' + ksdkProj.device[1] + '/iar/' + ksdkProj.device[0] + '_flash.icf'
        
        self.ewpStartup = copy.deepcopy(EWP_STARTUP)
        
        EWP_SOURCES = {'name': 'sources', 'file': [PROJECT_DIRS + '/../main.c']}

        #add main.h only for quick generation
        if self.parentProject.isQuickGenerate:
            EWP_SOURCES[FILE_KEY_IN_DICT].append(PROJECT_DIRS + '/../main.h')
        
        
        listOfCMSISDict = self.parentProject.parent.getCMSISFiles(ksdkProj.device[1])
        cmsisFilePaths = [d[ksdkObj.LOCATION_URI_KEY] for d in listOfCMSISDict]        
        PROJ_CMSIS =\
        {NAME_KEY_IN_DICT: 'CMSIS', 'file': cmsisFilePaths }
        
        self.projCMSISFiles = PROJ_CMSIS
        self.archType = CortexType.getCortexType(self.device[4])
        toolType = ToolchainType.IARname
        if ksdkProj.rtos != 'bm':
            mapOfFiles = []
            folderName = ''
            if ksdkProj.rtos == 'freertos':
                mapOfFiles = self.parentProject.parent.getMapOfFreertosPaths(self.archType, toolType, self.parentProject.board[1])
                folderName = ksdkKdsNew.FREERTOS_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.FreeRTOS):
                    EWP_SOURCES[FILE_KEY_IN_DICT].append(PROJECT_DIRS + '/../' + name)
            elif ksdkProj.rtos == 'ucosii':
                mapOfFiles = self.parentProject.parent.getMapOfuCOSIIPaths(self.archType, toolType, self.parentProject.board[1])
                folderName = ksdkKdsNew.UCOSII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSII):
                    EWP_SOURCES[FILE_KEY_IN_DICT].append(PROJECT_DIRS + '/../' + name)
            elif ksdkProj.rtos == 'ucosiii':
                mapOfFiles = self.parentProject.parent.getMapOfuCOSIIIPaths(self.archType, toolType, self.parentProject.board[1])
                folderName = ksdkKdsNew.UCOSIII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSIII):
                    EWP_SOURCES[FILE_KEY_IN_DICT].append(PROJECT_DIRS + '/../' + name)
                
            self.ewpRtos = {NAME_KEY_IN_DICT: folderName, FILE_KEY_IN_DICT: [dictionary[ksdkObj.LOCATION_URI_KEY] for dictionary in mapOfFiles]}
            
            
        self.ewpSources = copy.deepcopy(EWP_SOURCES)

        # Copy dictionaries for .eww batch buildss
        self.wsBatchAll = copy.deepcopy(EWW_BATCH_ALL)
        self.wsBatchDbg = copy.deepcopy(EWW_BATCH_DBG)
        self.wsBatchRls = copy.deepcopy(EWW_BATCH_RLS)

        # Copy project path dictionary
        self.projPaths = copy.deepcopy(EWW_PROJECTS)
        return

    def gen_ewp(self, ksdkProj):
        """ Generate the ewp files for IAR project

        :param ksdkProj: Instance of a KSDK project
        """

        iarPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/iar'
        if self.isLinked:
            self.projRelPath = '$PROJ_DIR$/' + kT.get_rel_path(iarPath, ksdkProj.sdkPath) + '/'
        else:
            self.projRelPath = '$PROJ_DIR$/../'

        # Populate ksdkProj specifics to dictionaries

        ## Set name of out file
        self.linkOut['state'] = self.name + '.out'

        ## Configure linker option
        self.linkIcf['state'] = self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getLinkerPath(ksdkProj.device, 'iar', False)

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
        self.cIncludes['state'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1] + os.sep + Constants.UTILITIES_FOLDER)
        self.cIncludes['state'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1] + os.sep + Constants.DRIVERS_FOLDER)



        self.cIncludes['state'].append("$PROJ_DIR$/../../..")
        
        # in project root, there are application files in case of rtos, so it has to be added to cIncludes
        self.cIncludes['state'].append("$PROJ_DIR$/../")

        # Add rtos paths
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.cIncludes['state'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getFreertosDirectoriesPaths(self.archType, ToolchainType.IARname, self.parentProject.board[1]))
                #FIXME Radka find out why
                self.asmIncludes['state'].append('$PROJ_DIR$/..')
            elif ksdkProj.rtos == 'ucosii':
                self.cIncludes['state'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getuCOSIIDirectoriesPaths(self.archType, ToolchainType.IARname, self.parentProject.board[1]))
            elif ksdkProj.rtos == 'ucosiii':
                self.cIncludes['state'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getuCOSIIIDirectoriesPaths(self.archType, ToolchainType.IARname, self.parentProject.board[1]))



        # Add relative paths to files
        index = 0
        while index < len(self.ewpStartup['file']):
            self.ewpStartup['file'][index] = kT.string_replace(self.ewpStartup['file'][index], ksdkKdsNew.DEVICE_NAME_CONSTANT, ksdkProj.device[1])
            self.ewpStartup['file'][index] = self.projRelPath + self.ewpStartup['file'][index]
            index += 1
        
        
        for d in [self.projCMSISFiles, self.drivers, self.utilities]:
            d[FILE_KEY_IN_DICT] = [self.projRelPath + f for f in d[FILE_KEY_IN_DICT]]
        
        #add relative path to linker file    
        self.linkerFile = self.projRelPath + self.linkerFile

        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                index = 0
                while index < len(self.ewpRtos['file']):
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'xxx',\
                                                ksdkProj.device[1][1:])
                    self.ewpRtos['file'][index] = self.projRelPath + self.ewpRtos['file'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.ewpRtos['file']):
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'ccc',\
                                                archType)
                    self.ewpRtos['file'][index] = self.projRelPath + self.ewpRtos['file'][index]
                    index += 1
            elif ksdkProj.rtos == 'ucosiii':
                archType = 'ARM-Cortex-M4' if (self.device[4] == 'cm4') else 'ARM-Cortex-M0'
                index = 0
                while index < len(self.ewpRtos['file']):
                    self.ewpRtos['file'][index] = kT.string_replace(self.ewpRtos['file'][index],\
                                                'ccc',\
                                                archType)
                    self.ewpRtos['file'][index] = self.projRelPath + self.ewpRtos['file'][index]
                    index += 1

        kT.debug_log(self.ewpStartup['file'])


        # Configure linker stack and heap
        if self.projType == 'usb':
            if ksdkProj.rtos == 'bm':
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['state'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['state'][1] = '__stack_size__=0x1000'
            else:
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['state'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['state'][1] = '__stack_size__=0x1000'

        if ksdkProj.rtos == 'freertos':
            self.linkDefines['state'][0] = '__stack_size__=0x1000'
            self.linkDefines['state'][1] = '__heap_size__=0x1000'
            self.linkDefines['state'].append('__ram_vector_table__=1')
        elif ksdkProj.rtos == 'ucosii':
            self.linkDefines['state'][0] = '__stack_size__=0x1000'
            self.linkDefines['state'][1] = '__heap_size__=0x1000'
            self.linkDefines['state'].append('__ram_vector_table__=1')
        elif ksdkProj.rtos == 'ucosiii':
            self.linkDefines['state'][0] = '__stack_size__=0x1000'
            self.linkDefines['state'][1] = '__heap_size__=0x1000'
            self.linkDefines['state'].append('__ram_vector_table__=1')
            

        tree = ET.ElementTree(ET.fromstring(iF.iar_formatted_ewp))

        for elem in tree.iter(tag='option'):
            for child in elem.findall('name'):
                if child.text == 'OGChipSelectEditMenu':
                    projDev = ET.Element('state')
                    projDev.text = ksdkProj.device[0] + '\tFreescale ' + ksdkProj.device[0]
                    elem.append(projDev)
                if child.text == 'FPU':
                    projFPU = ET.Element('state')
                    projFPU.text = '5' if self.device[3] else '0'
                    elem.append(projFPU)
                if child.text == 'GFPUCoreSlave':
                    projFPU = ET.Element('state')
                    projFPU.text = '39' if self.device[3] else '35'
                    elem.append(projFPU)
                if child.text == 'GBECoreSlave':
                    projBE = ET.Element('state')
                    projBE.text = '39' if self.device[3] else '35'
                    elem.append(projBE)
                if child.text == 'CCDefines':
                    for d in self.cDefines['state']:
                        projCDef = ET.Element('state')
                        projCDef.text = d
                        elem.append(projCDef)
                if child.text == 'IlinkConfigDefines':
                    if ksdkProj.rtos != 'bm':
                        for d in self.linkDefines['state']:
                            projLDef = ET.Element('state')
                            projLDef.text = d
                            elem.append(projLDef)
                if child.text == 'IlinkOverrideProgramEntryLabel':
                    if ksdkProj.rtos == 'mqx':
                        for s in elem.findall('state'):
                            s.text = '1'
                            #print s.text
                if child.text == 'IlinkOutputFile':
                    projOut = ET.Element('state')
                    projOut.text = self.linkOut['state']
                    elem.append(projOut)
                if child.text == 'IlinkIcfFile':
                    projIcf = ET.Element('state')
                    projIcf.text = self.linkIcf['state']
                    elem.append(projIcf)
                if child.text == 'CCIncludePath2':
                    for i in self.cIncludes['state']:
                        projInc = ET.Element('state')
                        projInc.text = i
                        elem.append(projInc)
                if child.text == 'AUserIncludes':
                    #print "ASM Inlcudes"
                    if ksdkProj.rtos == 'freertos':
                        asmInc = ET.Element('state')
                        asmInc.text = self.asmIncludes['state'][0]
                        elem.append(asmInc)

        # Add file groups to ewp file
        root = tree.getroot()
        
        #add linker file to the root of project
        linkerFile = ET.SubElement(root, 'file')
        linkerFileName = ET.SubElement(linkerFile, 'name')
        linkerFileName.text = self.linkerFile
        
        for d in [self.ewpStartup, self.projCMSISFiles, self.templates, self.drivers, self.utilities, self.ewpSources]:
            group = ET.SubElement(root, 'group')
            groupName = ET.SubElement(group, 'name')
            groupName.text = d[NAME_KEY_IN_DICT]
            for f in d[FILE_KEY_IN_DICT]:
                file = ET.SubElement(group, 'file')
                fileFName = ET.SubElement(file, 'name')
                fileFName.text = f
                #exclude some drivers and utilities
                if (d == self.drivers) or (d == self.utilities):
                    if f.endswith('.c'):
                        dictToFindExcluded = self.drivers if d == self.drivers else self.utilities
                        if dictToFindExcluded[EXCLUDED_LIST][d[FILE_KEY_IN_DICT].index(f)]:
                            exc = ET.SubElement(file, 'excluded')
                            conf = ET.SubElement(exc, 'configuration')
                            conf.text = 'Debug'

        if ksdkProj.rtos != 'bm':
            rtosGrp = ET.SubElement(root, 'group')
            rtosName = ET.SubElement(rtosGrp, 'name')
            rtosName.text = self.ewpRtos['name']
            for f in self.ewpRtos['file']:
                rtosFile = ET.SubElement(rtosGrp, 'file')
                rtosFName = ET.SubElement(rtosFile, 'name')
                rtosFName.text = f

        prettyRoot = kT.pretty_xml(root, "iso-8859-1")

        # Write data to file
        if not os.path.isdir(iarPath):
            os.makedirs(iarPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(iarPath + '/' + self.name + '.ewp', "iso-8859-1")

        # Gen ewd while we are here
        tree = ET.ElementTree(ET.fromstring(iF.iar_formatted_ewd))

        for elem in tree.iter(tag='option'):
            for child in elem.findall('name'):
                if child.text == 'OCDynDriverList':
                    for state in elem.findall('state'):
                        state.text = 'CMSISDAP_ID' if (self.device[4] == 'cm4') else 'PEMICRO_ID'
                if child.text == 'CMSISDAPResetList':
                    for state in elem.findall('state'):
                        state.text = '5' if (self.device[4] == 'cm4') else '10'
                if child.text == 'CMSISDAPInterfaceRadio':
                    for state in elem.findall('state'):
                        state.text = '1' if (self.device[4] == 'cm4') else '0'
                if child.text == 'CMSISDAPSelectedCPUBehaviour':
                    for state in elem.findall('state'):
                        state.text = '' if (self.device[4] == 'cm4') else '0'

        tree.write(iarPath + '/' + self.name + '.ewd', "iso-8859-1")

        return

    def gen_eww(self, ksdkProj):
        """ Generate the eww files for IAR project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        iarPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/iar'
        if self.isLinked:
            self.wsRelPath = '$WS_DIR$/' + kT.get_rel_path(iarPath, ksdkProj.sdkPath) + '/'
        else:
            self.wsRelPath = '$WS_DIR$/../'

        # Populate dictionaries with ksdkProj info
        ## All
        self.wsBatchAll['member'][0]['project'] = self.name
        self.wsBatchAll['member'][1]['project'] = self.name

        ## Release
        self.wsBatchRls['member'][0]['project'] = self.name
        ## Debug
        self.wsBatchDbg['member'][0]['project'] = self.name

        # Create tree
        tree = ET.ElementTree()

        # Set root
        root = ET.Element('workspace')

        # Create subelements for batch builds
        batch = ET.SubElement(root, 'batchBuild')

        ## All
        batchDefAll = ET.SubElement(batch, 'batchDefinition')
        batchName = ET.SubElement(batchDefAll, 'name')
        batchName.text = self.wsBatchAll['name']
        for m in self.wsBatchAll['member']:
            batchMember = ET.SubElement(batchDefAll, 'member')
            batchProj = ET.SubElement(batchMember, 'project')
            batchProj.text = m['project']
            batchConfig = ET.SubElement(batchMember, 'configuration')
            batchConfig.text = m['configuration']

        ## Release
        batchDefRls = ET.SubElement(batch, 'batchDefinition')
        batchName = ET.SubElement(batchDefRls, 'name')
        batchName.text = self.wsBatchRls['name']
        for m in self.wsBatchRls['member']:
            batchMember = ET.SubElement(batchDefRls, 'member')
            batchProj = ET.SubElement(batchMember, 'project')
            batchProj.text = m['project']
            batchConfig = ET.SubElement(batchMember, 'configuration')
            batchConfig.text = m['configuration']

        ## Debug
        batchDefDbg = ET.SubElement(batch, 'batchDefinition')
        batchName = ET.SubElement(batchDefDbg, 'name')
        batchName.text = self.wsBatchDbg['name']
        for m in self.wsBatchDbg['member']:
            batchMember = ET.SubElement(batchDefDbg, 'member')
            batchProj = ET.SubElement(batchMember, 'project')
            batchProj.text = m['project']
            batchConfig = ET.SubElement(batchMember, 'configuration')
            batchConfig.text = m['configuration']

        # Edit dictionary to add ksdkProj info
        self.projPaths['path'].append('$WS_DIR$/' + self.name + '.ewp')

        # Populate project paths
        for p in self.projPaths['path']:
            proj = ET.SubElement(root, 'project')
            projPath = ET.SubElement(proj, 'path')
            projPath.text = p

        # Format data to make it more readable
        prettyRoot = kT.pretty_xml(root, "iso-8859-1")

        # Write data to file
        if not os.path.isdir(iarPath):
            os.mkdir(iarPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(iarPath + '/' + self.name + '.eww', "iso-8859-1")

        return
