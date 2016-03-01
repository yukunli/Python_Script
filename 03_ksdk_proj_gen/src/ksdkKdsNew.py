'''
Created on Dec 9, 2015

@author: B49736
'''
## USER MODULES
from ksdkTools import KsdkTools as kT
from ksdkProj import ksdkProjClass
import kdsFiles as kF
import ksdkObj

## PYTHON MODULES
import copy
import os
import xml.etree.ElementTree as ET
from ksdkObj import ToolchainType, CortexType
from mhlib import Folder
import Constants
from directoryStructureHelper import RTOSType

## Important ewp tags
CDEFINES = {'valueType': 'definedSymbols', 'listOptionValue': []}
CDEFINES_USB = {'valueType': 'definedSymbols', 'listOptionValue': ['_DEBUG=1']}
CINCLUDES = {'valueType': 'includePath', 'listOptionValue': []}

ASMDEFINES = {'valueType': 'definedSymbols', 'listOptionValue': ['DEBUG']}
ASMINCLUDES = {'valueType': 'includePath', 'listOptionValue': []}

LINKOUT = {'name': 'IlinkOutputFile', 'state': '.out'}
LINKDEFINES = {'name': 'IlinkConfigDefines', 'state': ['__stack_size__=', '__heap_size__=']}
LINKDEFINES_USB = {'name': 'IlinkConfigDefines', \
                  'state': ['__ram_vector_table__=1', '__stack_size__=', '__heap_size__=']}


LINKLD = {'valueType': 'stringList', 'listOptionValue': []}
# LINKLIBS = {'valueType': 'userObjs', \
#            'listOptionValue': ['lib/ksdk_xxx_lib/kds/ddd/debug/libksdk_xxx.a']}
LINKLIBS_USB = {'valueType': 'userObjs', \
               'listOptionValue': ['lib/ksdk_xxx_lib/kds/ddd/debug/libksdk_xxx.a', \
                         'usb/usb_core/device/build/kds/usbd_sdk_yyy_zzz/debug/libusbd_zzz.a', \
                         'usb/usb_core/device/build/kds/usbh_sdk_yyy_zzz/debug/libusbh_zzz.a']}

WS_PROJECTS = {'name': '', \
               'path': '', \
               'open': 'true', \
       'activeconfig': ['debug', 'release'], \
    'buildreferences': [{'config': 'debug', 'text': 'false'}, {'config': 'release', 'text': 'false'}]}

PROJECT_KSDK = 'PROJECT_KSDK'

DEVICE_NAME_CONSTANT = "xxx"

LINKER_NAME_CONSTANT = "yyy_linker"

NAME = 'name'
TYPE = 'type'
LOCATIONURI = 'locationURI'

PROJECT_DIRECTORY_PREFIX = 'devices/' + DEVICE_NAME_CONSTANT + "/"

KSDK_DIRECTORY_PREFIX = 'devices/' + DEVICE_NAME_CONSTANT + "/"

BOARD_FOLDER_NAME = 'board'

TEMPLATES =\
[\
 {NAME: BOARD_FOLDER_NAME, TYPE: '2', LOCATIONURI: 'virtual:/virtual'},\
]

FREERTOS_DIRECTORY_NAME = "freertos"
UCOSII_DIRECTORY_NAME = 'ucosii'
UCOSIII_DIRECTORY_NAME = 'ucosiii'

class KsdkKdsNew(object):
    """ Class for generating KDS projects

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
            #self.linkLibs = copy.deepcopy(LINKLIBS)
        else:
            self.cDefines = copy.deepcopy(CDEFINES_USB)
            self.linkDefines = copy.deepcopy(LINKDEFINES_USB)
            self.linkLibs = copy.deepcopy(LINKLIBS_USB)

        self.cIncludes = copy.deepcopy(CINCLUDES)
        self.linkOut = copy.deepcopy(LINKOUT)
        self.linkLd = copy.deepcopy(LINKLD)

        self.asmDefines = copy.deepcopy(ASMDEFINES)
        self.asmIncludes = copy.deepcopy(ASMINCLUDES)
        

        #add board templates
        templateNames = self.parentProject.parent.getBoardFilesList()
        for t in templateNames:
            TEMPLATES.append({NAME: BOARD_FOLDER_NAME + '/' + t, TYPE:'1', LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + t})
        
        #FIXME Radka load from manifest    
        PROJ_STARTUP =\
        [\
         {'name': 'startup', 'type': '2', 'locationURI': 'virtual:/virtual'}, \
         {'name': 'startup/startup_xxx.S', 'type': '1', 'locationURI': 'PROJECT_KSDK/' + KSDK_DIRECTORY_PREFIX + 'gcc/startup_xxx.S'}, \
         {'name': 'startup/system_xxx.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/' + KSDK_DIRECTORY_PREFIX + 'system_xxx.c'}, \
         {'name': 'startup/system_xxx.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/' + KSDK_DIRECTORY_PREFIX + 'system_xxx.h'}, \
         {'name': LINKER_NAME_CONSTANT, 'type': '1', 'locationURI': 'PROJECT_KSDK/' + KSDK_DIRECTORY_PREFIX + '/gcc/' + LINKER_NAME_CONSTANT}, \
         {'name': Constants.DRIVERS_FOLDER, 'type': '2', 'locationURI': 'virtual:/virtual'}, \
         {'name': Constants.UTILITIES_FOLDER, 'type': '2', 'locationURI': 'virtual:/virtual'}, \
         {'name': Constants.CMSIS_FOLDER, 'type': '2', 'locationURI': 'virtual:/virtual'}, \
        ]
            
        #add drivers    
        for d in (self.parentProject.parent.getBoardFilesForBoardProjects(False, True, boardName = self.parentProject.board[1], device = ksdkProj.device[1], rtosType = ksdkProj.rtos) + self.parentProject.parent.getDriversExcludedFromBuild(device = ksdkProj.device[1])):
            PROJ_STARTUP.append({NAME: (Constants.DRIVERS_FOLDER if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.DRIVERS_FOLDER) != -1) else Constants.UTILITIES_FOLDER) + '/' + d[ksdkObj.NAME_KEY], TYPE:'1', LOCATIONURI: 'PROJECT_KSDK/' + d[ksdkObj.LOCATION_URI_KEY]}) 
        
        #add CMSIS
        for d in self.parentProject.parent.getCMSISFiles(ksdkProj.device[1]):
            PROJ_STARTUP.append({NAME: Constants.CMSIS_FOLDER + os.sep + d[ksdkObj.NAME_KEY] ,TYPE:'1',LOCATIONURI:'PROJECT_KSDK/' + d[ksdkObj.LOCATION_URI_KEY]})    
        
        self.projTemplates = TEMPLATES            
        
        self.projStartup = copy.deepcopy(PROJ_STARTUP)
        
        PROJ_SOURCES = [{NAME: Constants.SOURCES_FOLDER, TYPE: '2', LOCATIONURI: 'virtual:/virtual'},{NAME: Constants.SOURCES_FOLDER + '/main.c', TYPE: '1', LOCATIONURI: 'PARENT-1-PROJECT_LOC/main.c'}]
        
        #add always main.c  and also main.h in case it is quick project generation
        if self.parentProject.isQuickGenerate:
            PROJ_SOURCES.append({NAME: Constants.SOURCES_FOLDER + '/main.h', TYPE: '1', LOCATIONURI: 'PARENT-1-PROJECT_LOC/main.h'})
            
        self.archType = CortexType.getCortexType(self.device[4])
        toolType = ToolchainType.KinetisDesignStudio
        if ksdkProj.rtos != 'bm':
            pathList = []
            folder_name = ''
            if ksdkProj.rtos == 'freertos':
                pathList = self.parentProject.parent.getMapOfFreertosPaths(self.archType, toolType, self.parentProject.board[1])
                folder_name = FREERTOS_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.FreeRTOS):
                    PROJ_SOURCES.append({NAME: Constants.SOURCES_FOLDER + '/' + name, TYPE:'1', LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + name})
            elif ksdkProj.rtos == 'ucosii':
                pathList = self.parentProject.parent.getMapOfuCOSIIPaths(self.archType, toolType, self.parentProject.board[1])
                folder_name = UCOSII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSII):
                    PROJ_SOURCES.append({NAME: Constants.SOURCES_FOLDER + '/' + name, TYPE:'1', LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + name})
            elif ksdkProj.rtos == 'ucosiii':
                pathList = self.parentProject.parent.getMapOfuCOSIIIPaths(self.archType, toolType, self.parentProject.board[1])
                folder_name = UCOSIII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSIII):
                    PROJ_SOURCES.append({NAME: Constants.SOURCES_FOLDER + '/' + name, TYPE:'1', LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + name})

            for dictionary in pathList:
                dictionary[ksdkObj.LOCATION_URI_KEY] = PROJECT_KSDK + '/' + dictionary[ksdkObj.LOCATION_URI_KEY]
                dictionary[ksdkObj.NAME_KEY] = folder_name + '/' + dictionary[ksdkObj.NAME_KEY]
                dictionary['type'] = '1'
            
            pathList.append({NAME: folder_name, TYPE: '2', LOCATIONURI: 'virtual:/virtual'})
            self.projRtos = copy.deepcopy(pathList)

        self.projSources = copy.deepcopy(PROJ_SOURCES)
        return

    def gen_cproject(self, ksdkProj):
        """ Generate the cproject file for KDS project

        :param ksdkProj: Instance of a KSDK project
        """

        kdsPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/kds'
        relPath = ''
        if self.isLinked:
            tempStr = kT.get_rel_path(kdsPath, ksdkProj.sdkPath) + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
            self.projRelPath = '${PROJECT_KSDK_PATH}/'
        else:
            relPath = '../../'
            self.projRelPath = relPath


        # Populate ksdkProj specifics to dictionaries

        ## Configure linker option
        self.linkLd['listOptionValue'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getLinkerPath(ksdkProj.device, 'gcc', False))


        ## Set a define for the device
        self.cDefines['listOptionValue'].append('CPU_' + ksdkProj.device[2])

        if ksdkProj.rtos != 'bm':
            param = self.parentProject.parent.getSmartcardParam(ksdkProj.device[1])
            if param is not None:
                self.cDefines['listOptionValue'].append(param)
            if ksdkProj.rtos == 'freertos':
                self.cDefines['listOptionValue'].append('FSL_RTOS_FREE_RTOS')
            elif ksdkProj.rtos == 'ucosii':
                self.cDefines['listOptionValue'].append('FSL_RTOS_UCOSII')
            elif ksdkProj.rtos == 'ucosiii':
                self.cDefines['listOptionValue'].append('FSL_RTOS_UCOSIII')

        ## Add C include paths necessary for project

        self.cIncludes['listOptionValue'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getCMSISIncludeDirectory(False))
         
        self.cIncludes['listOptionValue'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory())
        self.cIncludes['listOptionValue'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1])
        self.cIncludes['listOptionValue'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1] + os.sep + Constants.DRIVERS_FOLDER)
        self.cIncludes['listOptionValue'].append(self.projRelPath + self.parentProject.parent.getDirectoryStructureHelper().getDevicesDirectory() + os.sep + ksdkProj.device[1] + os.sep + Constants.UTILITIES_FOLDER)
        
        self.cIncludes['listOptionValue'].append("../../")

        # Add rtos paths
        if ksdkProj.rtos != 'bm':
            if ksdkProj.rtos == 'freertos':
                self.cIncludes['listOptionValue'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getFreertosDirectoriesPaths(self.archType, ToolchainType.KinetisDesignStudio, self.parentProject.board[1]))
            elif ksdkProj.rtos == 'ucosii':
                self.cIncludes['listOptionValue'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getuCOSIIDirectoriesPaths(self.archType, ToolchainType.KinetisDesignStudio, self.parentProject.board[1]))
            elif ksdkProj.rtos == 'ucosiii':
                self.cIncludes['listOptionValue'].extend(self.projRelPath + directoryPath for directoryPath in self.parentProject.parent.getuCOSIIIDirectoriesPaths(self.archType, ToolchainType.KinetisDesignStudio, self.parentProject.board[1]))


        # Configure linker stack and heap
        if self.projType == 'usb':
            if ksdkProj.rtos == 'bm':
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x1000'
            else:
                if 'kl' in ksdkProj.board[1]:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x400'
                else:
                    self.linkDefines['listOptionValue'][1] = '__stack_size__=0x1000'

        tree = ET.ElementTree(ET.fromstring(kF.formatted_cproject))
        root = tree.getroot()
        
        
        #exclude drivers from build
        excludedDriversText = ''
        driverPaths = [(Constants.DRIVERS_FOLDER if d[ksdkObj.LOCATION_URI_KEY].find(Constants.DRIVERS_FOLDER) != -1 else Constants.UTILITIES_FOLDER) + '/' + d[ksdkObj.NAME_KEY] for d in self.parentProject.parent.getDriversExcludedFromBuild(ksdkProj.device[1])]
        for f in driverPaths:
            if f.endswith('.c'):
                excludedDriversText += f
                if not driverPaths.index(f) == len(driverPaths):
                    excludedDriversText += '|'
                
        for excludeEntry in root.findall('.//sourceEntries'):
            elem = ET.Element('entry', {'excluding': excludedDriversText, 'flags':'VALUE_WORKSPACE_PATH', 'kind':'sourcePath', 'name':''})
            excludeEntry.insert(0, elem)


        for child in root.findall('storageModule'):
            for config in child.findall('cconfiguration'):
                for module in config.findall('storageModule'):
                    if ksdkProj.isLinked:
                        if module.get('moduleId') == "org.eclipse.cdt.core.settings":
                            macros = ET.Element('macros')
                            module.append(macros)
                            stringMacro = ET.Element('stringMacro', {'name': 'PROJECT_KSDK_PATH', 'type': 'VALUE_TEXT', 'value': kT.string_replace(ksdkProj.sdkPath, '\\', '/')})
                            for macros in module.findall('macros'):
                                macros.append(stringMacro)
                    if module.get('moduleId') == "cdtBuildSystem":
                        for configure in module.findall('configuration'):
                            buildVer = configure.get('name')
                            for folder in configure.findall('folderInfo'):
                                for toolC in folder.findall('toolChain'):
                                    for option in toolC.findall('option'):
                                        if option.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.family":
                                            option.set('value', "ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.mcpu.cortex-" + ksdkProj.device[4][1:])
                                        if option.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi":
                                            optionVal = "hard" if ksdkProj.device[3] else "default"
                                            #print optionVal
                                            option.set('value', "ilg.gnuarmeclipse.managedbuild.cross.option.arm.target.fpu.abi." + optionVal)
                                    for tool in toolC.findall('tool'):
                                        #Add assembler options
                                        if tool.get('name') == "Cross ARM GNU Assembler":
                                            if ksdkProj.rtos == 'freertos':
                                                for label in tool.findall('option'):
                                                    #Add include paths
                                                    if label.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.assembler.include.paths":
                                                        #Add New Include paths
                                                        for i in self.asmIncludes['listOptionValue']:
                                                            path = ET.Element('listOptionValue', {'builtIn': 'false', 'value': i})
                                                            label.append(path)
                                        #Add compiler options
                                        if tool.get('name') == "Cross ARM C Compiler":
                                            for label in tool.findall('option'):
                                                #Add include paths
                                                if label.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.include.paths":
                                                    #Add New Include paths
                                                    for i in self.cIncludes['listOptionValue']:
                                                        path = ET.Element('listOptionValue', {'builtIn': 'false', 'value': i})
                                                        label.append(path)
                                                #Add compiler defines
                                                if label.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.c.compiler.defs":
                                                    # Add new project defines
                                                    for d in self.cDefines['listOptionValue']:
                                                        define = ET.Element('listOptionValue', {'builtIn': 'false', 'value': d})
                                                        label.append(define)
                                        #Add linker options
                                        if tool.get('name') == "Cross ARM C Linker":
                                            for label in tool.findall('option'):
                                                #Add linker script
                                                if label.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.scriptfile":
                                                    for l in self.linkLd['listOptionValue']:
                                                        linker = ET.Element('listOptionValue', {'builtIn': 'false', 'value': l})
                                                        label.append(linker)
                                                #Add linker otions
                                                if label.get('superClass') == "ilg.gnuarmeclipse.managedbuild.cross.option.c.linker.other":
                                                    if ksdkProj.rtos != 'bm':
                                                        temp = label.get('value')
                                                        temp += ' -Xlinker --defsym=__stack_size__=0x1000  -Xlinker --defsym=__heap_size__=0x1000  -Xlinker --defsym=__ram_vector_table__=1'
                                                        if ksdkProj.rtos == 'mqx':
                                                            temp += ' -Xlinker --undefined=__isr_vector'
                                                        label.set('value', temp)



        prettyRoot = kT.pretty_xml(root, "UTF-8")

        # Write data to file
        if not os.path.isdir(kdsPath):
            os.makedirs(kdsPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(kdsPath + '/.cproject', "UTF-8")

        kT.cdt_fix_post_xml(kdsPath)

        return

    def gen_project(self, ksdkProj):
        """ Generate the eww files for KDS project

        :param ksdkProj: Instance of a KSDK project
        """

        # Get relative path
        kdsPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/kds'

        relPath = ''
        print self.isLinked
        if self.isLinked:
            print 'Linked'
            tempStr = kT.get_rel_path(kdsPath, ksdkProj.sdkPath) + '/'
            print tempStr
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
            print relPath
        else:
            relPath = '../'

        tree = ET.ElementTree(ET.fromstring(kF.formatted_project))
        root = tree.getroot()
        for child in root:
            if child.tag == 'name':
                child.text = str(self.name + '_' + ksdkProj.device[2])
            if child.tag == 'linkedResources':
                for s in self.projStartup:
                    link = ET.Element('link')
                    child.append(link)
                    linkName = ET.Element('name')
                    tempName = kT.string_replace(s['name'], DEVICE_NAME_CONSTANT, ksdkProj.device[1])
                    tempName = kT.string_replace(tempName, LINKER_NAME_CONSTANT, ksdkProj.device[0] + "_flash.ld")
                    linkName.text = tempName
                    link.append(linkName)
                    linkType = ET.Element('type')
                    linkType.text = s['type']
                    link.append(linkType)
                    linkURI = ET.Element('locationURI')
                    tempURI = kT.string_replace(s['locationURI'], DEVICE_NAME_CONSTANT, ksdkProj.device[1])
                    tempURI = kT.string_replace(tempURI, LINKER_NAME_CONSTANT, ksdkProj.device[0] + "_flash.ld")
                    if ksdkProj.isLinked == False:
                        tempURI = kT.string_replace(tempURI, 'PROJECT_KSDK', 'PARENT-1-PROJECT_LOC')
                    #print tempURI
                    linkURI.text = tempURI
                    link.append(linkURI)

                if ksdkProj.rtos != 'bm':
                    for r in self.projRtos:
                        link = ET.Element('link')
                        child.append(link)
                        linkName = ET.Element('name')
                        linkName.text = r['name']
                        link.append(linkName)
                        linkType = ET.Element('type')
                        linkType.text = r['type']
                        link.append(linkType)
                        linkURI = ET.Element('locationURI')
                        tempURI = r[ksdkObj.LOCATION_URI_KEY]
                        if ksdkProj.isLinked == False:
                            tempURI = kT.string_replace(r[ksdkObj.LOCATION_URI_KEY], 'PROJECT_KSDK', 'PARENT-1-PROJECT_LOC')
                        #print tempURI
                        linkURI.text = tempURI
                        link.append(linkURI)

                for c in self.projSources + self.projTemplates:
                    link = ET.Element('link')
                    child.append(link)
                    linkName = ET.Element('name')
                    linkName.text = c['name']
                    link.append(linkName)
                    linkType = ET.Element('type')
                    linkType.text = c['type']
                    link.append(linkType)
                    linkURI = ET.Element('locationURI')
                    linkURI.text = c['locationURI']
                    link.append(linkURI)

        # Add variable to project for KSDK path
        if ksdkProj.isLinked:
            projVarList = ET.SubElement(root, 'variableList')
            root.append(projVarList)
            projVar = ET.Element('variable')
            projVarList.append(projVar)
            varName = ET.Element('name')
            varName.text = "PROJECT_KSDK"
            projVar.append(varName)
            varVal = ET.Element('value')
            if ksdkProj.osType == 'Windows':
                varVal.text = "file:/" + kT.string_replace(ksdkProj.sdkPath, '\\', '/')
            else:
                varVal.text = "file:" + ksdkProj.sdkPath
            projVar.append(varVal)

                
        # Format data to make it more readable
        prettyRoot = kT.pretty_xml(root, "UTF-8")
 
        #print prettyRoot
 
        # Write data to file
        if not os.path.isdir(kdsPath):
            os.mkdir(kdsPath)
 
        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(kdsPath + '/.project', "UTF-8")
        return

    def gen_working_set(self, ksdkProj):
        """ Generate KDS working set for project
        """

        # Get relative path
        kdsPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/kds'

        relPath = ''
        if self.isLinked:
            tempStr = ksdkProj.sdkPath + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../'


        tree = ET.ElementTree(ET.fromstring(kF.formatted_wsd))
        root = tree.getroot()
        for child in root:
            if child.tag == 'projects':
                proj = ET.Element('project')
                child.append(proj)
                projName = ET.Element('name')
                projName.text = str(self.name + '_' + ksdkProj.device[2])
                proj.append(projName)
                projPath = ET.Element('path')
                projPath.text = '.'
                proj.append(projPath)
                projOpen = ET.Element('open')
                projOpen.text = 'true'
                proj.append(projOpen)
                projAct = ET.Element('activeconfig')
                projAct.text = 'debug'
                proj.append(projAct)
                projBulRef = ET.Element('buildreferences', {'config': "debug"})
                projBulRef.text = 'false'
                proj.append(projBulRef)
                projAct = ET.Element('activeconfig')
                projAct.text = 'release'
                proj.append(projAct)
                projBulRef = ET.Element('buildreferences', {'config': "release"})
                projBulRef.text = 'false'
                proj.append(projBulRef)

            if child.tag == 'workingsets':
                wSet = ET.Element('workingSet', {'editPageId': "org.eclipse.cdt.ui.CElementWorkingSetPage",\
                                                 'id': "1323268527287_1", 'label': self.name, 'name': self.name})
                child.append(wSet)

                wSetItem = ET.Element('item', {'factoryID': "org.eclipse.cdt.ui.PersistableCElementFactory", \
                                               'path': "/" + str(self.name + '_' + ksdkProj.device[2]), 'type': "4"})
                wSet.append(wSetItem)

            if child.tag == 'cdtconfigurations':
                wSet = ET.Element('workingSet', {'name': self.name})
                child.append(wSet)
                wSetConfig = ET.Element('config', {'name': "debug"})
                wSet.append(wSetConfig)

                wSetProjName = str(self.name + '_' + ksdkProj.device[2])
                wSetProj = ET.Element('project', {'config': "com.freescale.arm.cdt.toolchain.config.arm.release.695495605",\
                                                  'name': wSetProjName,\
                                                  'configName': "debug"})
                wSetConfig.append(wSetProj)

                wSetConfig = ET.Element('config', {'name': "release"})
                wSet.append(wSetConfig)
                wSetProj = ET.Element('project', {'config': "com.freescale.arm.cdt.toolchain.config.arm.release.695495605",\
                                                  'name': wSetProjName,\
                                                  'configName': "release"})
                wSetConfig.append(wSetProj)

        # Format data to make it more readable
        prettyRoot = kT.pretty_xml(root, "UTF-8")

        #print prettyRoot

        # Write data to file
        if not os.path.isdir(kdsPath):
            os.mkdir(kdsPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(kdsPath + '/' + self.name + '.wsd', "UTF-8")

        return

    def gen_debug(self, ksdkProj):
        """ Generate debug launch files
        """

        # Get relative path
        kdsPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/kds'

        if not 'MKL' in self.device[2]:
            tree = ET.ElementTree(ET.fromstring(kF.project_board_debug_cmsisdap_launch))
            launchPath = kdsPath + '/' + self.name + '_' + self.device[2] + ' debug cmsisdap.launch'
            tree.write(launchPath, "UTF-8")
            newStr = self.name + '_' + self.device[2]
            oldStr = 'project_board'
            kT.replace_name_in_file(launchPath, oldStr, newStr)

            tree = ET.ElementTree(ET.fromstring(kF.project_board_release_cmsisdap_launch))
            launchPath = kdsPath + '/' + self.name + '_' + self.device[2] + ' release cmsisdap.launch'
            tree.write(launchPath, "UTF-8")
            newStr = self.name + '_' + self.device[2]
            oldStr = 'project_board'
            kT.replace_name_in_file(launchPath, oldStr, newStr)

        tree = ET.ElementTree(ET.fromstring(kF.project_board_debug_jlink_launch))
        launchPath = kdsPath + '/' + self.name + '_' + self.device[2] + ' debug jlink.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'jlinkDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(kF.project_board_release_jlink_launch))
        launchPath = kdsPath + '/' + self.name + '_' + self.device[2] + ' release jlink.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'jlinkDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(kF.project_board_debug_pne_launch))
        launchPath = kdsPath + '/' + self.name + '_' + self.device[2] + ' debug pne.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'pneDEVICE', kT.string_replace(self.device[0][1:], 'xxx', 'M'))

        tree = ET.ElementTree(ET.fromstring(kF.project_board_release_pne_launch))
        launchPath = kdsPath + '/' + self.name + '_' + self.device[2] + ' release pne.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'pneDEVICE', kT.string_replace(self.device[0][1:], 'xxx', 'M'))

        return

