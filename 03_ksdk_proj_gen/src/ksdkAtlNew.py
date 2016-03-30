'''
Created on Dec 9, 2015

@author: B49736
'''


## USER MODULES
from ksdkTools import KsdkTools as kT
from ksdkProj import ksdkProjClass
import atlFiles as aF
import ksdkKdsNew
import ksdkObj
from ksdkObj import ToolchainType, CortexType
import Constants

## PYTHON MODULES
import copy
import os
import xml.etree.ElementTree as ET
from directoryStructureHelper import RTOSType


## Important ewp tags
LINKLIBS_USB = {'valueType': 'userObjs', \
               'listOptionValue': ['lib/ksdk_xxx_lib/atl/ddd/debug/libksdk_xxx.a', \
                         'usb/usb_core/device/build/atl/usbd_sdk_yyy_zzz/debug/libusbd_zzz.a', \
                         'usb/usb_core/device/build/atl/usbh_sdk_yyy_zzz/debug/libusbh_zzz.a']}

WS_PROJECTS = ksdkKdsNew.WS_PROJECTS


class KsdkAtlNew(object):
    """ Class for generating ATL projects
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
            self.cDefines = copy.deepcopy(ksdkKdsNew.CDEFINES)
            self.linkDefines = copy.deepcopy(ksdkKdsNew.LINKDEFINES)
        else:
            self.cDefines = copy.deepcopy(ksdkKdsNew.CDEFINES_USB)
            self.linkDefines = copy.deepcopy(ksdkKdsNew.LINKDEFINES_USB)
            self.linkLibs = copy.deepcopy(LINKLIBS_USB)

        self.cIncludes = copy.deepcopy(ksdkKdsNew.CINCLUDES)
        self.linkOut = copy.deepcopy(ksdkKdsNew.LINKOUT)
        self.linkLd = copy.deepcopy(ksdkKdsNew.LINKLD)

        self.asmDefines = copy.deepcopy(ksdkKdsNew.ASMDEFINES)
        self.asmIncludes = copy.deepcopy(ksdkKdsNew.ASMINCLUDES)
        
        TEMPLATES = copy.deepcopy(ksdkKdsNew.TEMPLATES)
        
        #add board templates
        templateNames = self.parentProject.parent.getBoardFilesList()
        for t in templateNames:
            TEMPLATES.append({ksdkKdsNew.NAME: ksdkKdsNew.BOARD_FOLDER_NAME + '/' + t, ksdkKdsNew.TYPE:'1', ksdkKdsNew.LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + t})
        
        #FIXME Radka load it from manifest    
        PROJ_STARTUP =\
        [\
         {'name': 'startup', 'type': '2', 'locationURI': 'virtual:/virtual'}, \
         {'name': 'startup/startup_xxx.S', 'type': '1', 'locationURI': 'PROJECT_KSDK/' + ksdkKdsNew.KSDK_DIRECTORY_PREFIX + 'gcc/startup_xxx.S'}, \
         {'name': 'startup/system_xxx.c', 'type': '1', 'locationURI': 'PROJECT_KSDK/' + ksdkKdsNew.KSDK_DIRECTORY_PREFIX + 'system_xxx.c'}, \
         {'name': 'startup/system_xxx.h', 'type': '1', 'locationURI': 'PROJECT_KSDK/' + ksdkKdsNew.KSDK_DIRECTORY_PREFIX + 'system_xxx.h'}, \
         {'name': ksdkKdsNew.LINKER_NAME_CONSTANT, 'type': '1', 'locationURI': 'PROJECT_KSDK/' + ksdkKdsNew.KSDK_DIRECTORY_PREFIX + '/gcc/' + ksdkKdsNew.LINKER_NAME_CONSTANT}, \
         {'name': Constants.DRIVERS_FOLDER, 'type': '2', 'locationURI': 'virtual:/virtual'}, \
         {'name': Constants.UTILITIES_FOLDER, 'type': '2', 'locationURI': 'virtual:/virtual'}, \
         {'name': Constants.CMSIS_FOLDER, 'type': '2', 'locationURI': 'virtual:/virtual'}, \
        ]
            
        #add drivers
        #PROJ_STARTUP = copy.deepcopy(ksdkKdsNew.PROJ_STARTUP)    
        for d in (self.parentProject.parent.getBoardFilesForBoardProjects(False, True, boardName = self.parentProject.board[1], device = ksdkProj.device[1], rtosType = ksdkProj.rtos) + self.parentProject.parent.getDriversExcludedFromBuild(device = ksdkProj.device[1])):
            PROJ_STARTUP.append({'name': (Constants.DRIVERS_FOLDER if (d[ksdkObj.LOCATION_URI_KEY].find(Constants.DRIVERS_FOLDER) != -1) else Constants.UTILITIES_FOLDER) + '/' + d[ksdkObj.NAME_KEY], 'type':'1', 'locationURI': 'PROJECT_KSDK/' + d[ksdkObj.LOCATION_URI_KEY]}) 
        
        #add CMSIS
        for d in self.parentProject.parent.getCMSISFiles(ksdkProj.device[1]):
            PROJ_STARTUP.append({'name': 'CMSIS' + os.sep + d[ksdkObj.NAME_KEY] ,'type':'1','locationURI':'PROJECT_KSDK/' + d[ksdkObj.LOCATION_URI_KEY]})     
        
        self.projTemplates = TEMPLATES 
        
        PROJ_SOURCES = [{ksdkKdsNew.NAME: Constants.SOURCES_FOLDER, ksdkKdsNew.TYPE: '2', ksdkKdsNew.LOCATIONURI: 'virtual:/virtual'},{ksdkKdsNew.NAME: Constants.SOURCES_FOLDER + '/main.c', ksdkKdsNew.TYPE: '1', ksdkKdsNew.LOCATIONURI: 'PARENT-1-PROJECT_LOC/main.c'}]
        if self.parentProject.isQuickGenerate:
            PROJ_SOURCES.append({ksdkKdsNew.NAME: Constants.SOURCES_FOLDER + '/main.h', ksdkKdsNew.TYPE: '1', ksdkKdsNew.LOCATIONURI: 'PARENT-1-PROJECT_LOC/main.h'})

        self.archType = CortexType.getCortexType(self.device[4])
        toolType = ToolchainType.AtollicStudio
        if ksdkProj.rtos != 'bm':
            pathList = []
            folder_name = ''
            if ksdkProj.rtos == 'freertos':
                pathList = self.parentProject.parent.getMapOfFreertosPaths(self.archType, toolType, self.parentProject.board[1])
                folder_name = ksdkKdsNew.FREERTOS_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.FreeRTOS):
                    PROJ_SOURCES.append({ksdkKdsNew.NAME: Constants.SOURCES_FOLDER + '/' + name, ksdkKdsNew.TYPE:'1', ksdkKdsNew.LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + name})
            elif ksdkProj.rtos == 'ucosii':
                pathList = self.parentProject.parent.getMapOfuCOSIIPaths(self.archType, toolType, self.parentProject.board[1])
                folder_name = ksdkKdsNew.UCOSII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSII):
                    PROJ_SOURCES.append({ksdkKdsNew.NAME: Constants.SOURCES_FOLDER + '/' + name, ksdkKdsNew.TYPE:'1', ksdkKdsNew.LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + name})
            elif ksdkProj.rtos == 'ucosiii':
                pathList = self.parentProject.parent.getMapOfuCOSIIIPaths(self.archType, toolType, self.parentProject.board[1])
                folder_name = ksdkKdsNew.UCOSIII_DIRECTORY_NAME
                for name in self.parentProject.parent.getRTOSTemplateFilesNames(RTOSType.uCOSIII):
                    PROJ_SOURCES.append({ksdkKdsNew.NAME: Constants.SOURCES_FOLDER + '/' + name, ksdkKdsNew.TYPE:'1', ksdkKdsNew.LOCATIONURI: 'PARENT-1-PROJECT_LOC/' + name})

            for dictionary in pathList:
                dictionary[ksdkObj.LOCATION_URI_KEY] = ksdkKdsNew.PROJECT_KSDK + '/' + dictionary[ksdkObj.LOCATION_URI_KEY]
                dictionary[ksdkObj.NAME_KEY] = folder_name + '/' + dictionary[ksdkObj.NAME_KEY]
                dictionary['type'] = '1'
            
            pathList.append({'name': folder_name, 'type': '2', 'locationURI': 'virtual:/virtual'})
            self.projRtos = copy.deepcopy(pathList)
        
        self.projStartup = copy.deepcopy(PROJ_STARTUP)
        self.projSources = copy.deepcopy(PROJ_SOURCES)
        return

    def gen_cproject(self, ksdkProj):
        """ Generate the cproject file for KDS project

        :param ksdkProj: Instance of a KSDK project
        """

        kdsPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl'
        relPath = ''
        if self.isLinked:
            tempStr = kT.get_rel_path(kdsPath, ksdkProj.sdkPath) + '/../'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../../'
        
        self.projRelPath = relPath


        # Populate ksdkProj specifics to dictionaries

        ## Configure linker option
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




        #    l = kT.string_replace(l, 'zzz', ksdkProj.rtos)
        #    kT.debug_log(l)
        #    if self.projType == 'usb':
        #        l = kT.string_replace(l, 'yyy', ksdkProj.board[1])
        #    b = l

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

        tree = ET.ElementTree(ET.fromstring(aF.formatted_cproject))
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
                    if module.get('moduleId') == "cdtBuildSystem":
                        for configure in module.findall('configuration'):
                            buildVer = configure.get('name')
                            for folder in configure.findall('folderInfo'):
                                for toolC in folder.findall('toolChain'):
                                    for tool in toolC.findall('tool'):
                                        #Add assembler options
                                        if tool.get('name') == "Assembler":
                                            for label in tool.findall('option'):
                                                if label.get('superClass') == "com.atollic.truestudio.common_options.target.fpu":
                                                    optionVal = "hard" if ksdkProj.device[3] else "soft"
                                                    #print optionVal
                                                    label.set('value', "com.atollic.truestudio.common_options.target.fpu." + optionVal)
                                                if label.get('superClass') == "com.atollic.truestudio.as.general.otherflags":
                                                    label.set('value', " -mcpu=cortex-" + ksdkProj.device[4][1:])
                                                if label.get('superClass') == "com.atollic.truestudio.as.general.incpath":
                                                    if ksdkProj.rtos == 'freertos':
                                                        for a in self.asmIncludes['listOptionValue']:
                                                            path = ET.Element('listOptionValue', {'builtIn': 'false', 'value': a})
                                                            label.append(path)
                                        #Add compiler options
                                        if tool.get('name') == "C Compiler":
                                            for label in tool.findall('option'):
                                                #Add include paths
                                                if label.get('superClass') == "com.atollic.truestudio.gcc.directories.select":
                                                    #Add New Include paths
                                                    for i in self.cIncludes['listOptionValue']:
                                                        path = ET.Element('listOptionValue', {'builtIn': 'false', 'value': i})
                                                        label.append(path)
                                                #Add compiler defines
                                                if label.get('superClass') == "com.atollic.truestudio.gcc.symbols.defined":
                                                    # Add new project defines
                                                    for d in self.cDefines['listOptionValue']:
                                                        define = ET.Element('listOptionValue', {'builtIn': 'false', 'value': d})
                                                        label.append(define)
                                                if label.get('superClass') == "com.atollic.truestudio.common_options.target.fpu":
                                                    optionVal = "hard" if ksdkProj.device[3] else "soft"
                                                    #print optionVal
                                                    label.set('value', "com.atollic.truestudio.common_options.target.fpu." + optionVal)
                                                if label.get('superClass') == "com.atollic.truestudio.gcc.misc.otherflags":
                                                    label.set('value', " -mcpu=cortex-" + ksdkProj.device[4][1:])
                                        #Add linker options
                                        if tool.get('name') == "C Linker":
                                            for label in tool.findall('option'):
                                                #Add linker script
                                                if label.get('superClass') == "com.atollic.truestudio.ld.general.scriptfile":
                                                    for l in self.linkLd['listOptionValue']:
                                                        label.set('value', l)
                                                if label.get('superClass') == "com.atollic.truestudio.ld.misc.linkerflags":
                                                    temp = label.get('value')
                                                    if ksdkProj.device[4][1:] != 'm4':
                                                        temp = kT.string_replace(temp, 'm4', ksdkProj.device[4][1:])
                                                    if ksdkProj.rtos != 'bm':
                                                        temp += ' -Xlinker --defsym=__ram_vector_table__=1'
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
        atlPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl'

        relPath = ''
        if self.isLinked:
            tempStr = kT.get_rel_path(atlPath, ksdkProj.sdkPath) + '/'
            if ksdkProj.osType == 'Windows':
                relPath = kT.string_replace(tempStr, '\\', '/')
            else:
                relPath = tempStr[:]
        else:
            relPath = '../'

        tree = ET.ElementTree(ET.fromstring(aF.formatted_project))
        root = tree.getroot()
        for child in root:
            if child.tag == 'name':
                child.text = str(self.name + '_' + ksdkProj.device[2])
            if child.tag == 'linkedResources':
                #Add linked resources
                if ksdkProj.useBSP == True:
                    #Add board file links
                    for b in self.projBoard:
                        link = ET.Element('link')
                        child.append(link)
                        linkName = ET.Element('name')
                        linkName.text = b['name']
                        link.append(linkName)
                        linkType = ET.Element('type')
                        linkType.text = b['type']
                        link.append(linkType)
                        linkURI = ET.Element('locationURI')
                        linkURI.text = b['locationURI']
                        link.append(linkURI)

                for s in self.projStartup:
                    link = ET.Element('link')
                    child.append(link)
                    linkName = ET.Element('name')
                    tempName = kT.string_replace(s['name'], ksdkKdsNew.DEVICE_NAME_CONSTANT, ksdkProj.device[1])
                    tempName = kT.string_replace(tempName, ksdkKdsNew.LINKER_NAME_CONSTANT, ksdkProj.device[0] + "_flash.ld")
                    linkName.text = tempName
                    link.append(linkName)
                    linkType = ET.Element('type')
                    linkType.text = s['type']
                    link.append(linkType)
                    linkURI = ET.Element('locationURI')
                    tempURI = kT.string_replace(s['locationURI'], ksdkKdsNew.DEVICE_NAME_CONSTANT, ksdkProj.device[1])
                    tempURI = kT.string_replace(tempURI, ksdkKdsNew.LINKER_NAME_CONSTANT, ksdkProj.device[0] + "_flash.ld")
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
        if not os.path.isdir(atlPath):
            os.mkdir(atlPath)

        tree = ET.ElementTree(ET.fromstring(prettyRoot))
        tree.write(atlPath + '/.project', "UTF-8")

        return

    def gen_debug(self, ksdkProj):
        """ Generate debug launch files
        """

        # Get relative path
        atlPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl'

        tree = ET.ElementTree(ET.fromstring(aF.project_board_debug_jlink_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' debug jlink.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'jlinkDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(aF.project_board_release_jlink_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' release jlink.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'jlinkDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(aF.project_board_debug_pne_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' debug pne.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'pneDEVICE', self.device[0])

        tree = ET.ElementTree(ET.fromstring(aF.project_board_release_pne_launch))
        launchPath = atlPath + '/' + self.name + '_' + self.device[2] + ' release pne.launch'
        tree.write(launchPath, "UTF-8")
        newStr = self.name + '_' + self.device[2]
        oldStr = 'project_board'
        kT.replace_name_in_file(launchPath, oldStr, newStr)
        kT.replace_name_in_file(launchPath, 'pneDEVICE', self.device[0])

        return

    def gen_settings(self, ksdkProj):
        """ Generate settings files for ATL project
        """

        atlPath = self.parent + ('' if self.parent[-1:] == '/' else '/') + self.name + '/atl/.settings'

        # Write data to file
        if not os.path.isdir(atlPath):
            os.mkdir(atlPath)

        tree = ET.ElementTree(ET.fromstring(aF.language_settings_xml))
        launchPath = atlPath + '/language.settings.xml'
        tree.write(launchPath, "UTF-8")

        setPath = atlPath + '/com.atollic.truestudio.debug.hardware_device.prefs'
        setContent = aF.com_atollic_truestudio_debug_hardware_device_prefs
        setContent = kT.string_replace(setContent, 'settingDevice', self.device[0])
        with open(setPath, 'wb+') as f:
            f.write(setContent)
            f.close()

        return

