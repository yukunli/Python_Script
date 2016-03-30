"""
File:  ksdkTools.py
===================
Copyright (c) 2015 Freescale Semiconductor

Brief
+++++
**Methods for KSDK data manipulation**

.. codeauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. sectionauthor:: M. Hunt <Martyn.Hunt@freescale.com>

.. versionadded:: 0.0.5

UML
+++
.. uml:: {{/../../../src/ksdkTools.py

API
+++

"""

import re
import os
import shutil
import time
import xml.dom.minidom
import xml.etree.ElementTree
import json

#: Controls debug_log behavior: 'debug', 'log', or None
PG_SESSION = None

class KsdkTools(object):

    def __init__(self):
        pass

    @staticmethod
    def debug_log(outStr, errMsg=None):
        """ Used to print messages to the console for debugging
        or to console a log file if not a debug session

        :param outStr: Message to display in terminal
        :param errMsg: Exception traceback string
        """

        if errMsg != None:
            fileNname = os.path.split(errMsg.tb_frame.f_code.co_filename)[1]
            errString = ' in ' + fileNname + ' on line ' + str(errMsg.tb_lineno)
        else:
            fileNname = ''
            errString = ''

        if PG_SESSION == 'debug':
            # Print to the console
            print 'DEBUG: ' + str(outStr) + errString
        elif PG_SESSION == 'log':
            # Append log file
            curDate = time.strftime("[%m/%d/%Y:%I:%M:%S %p]")
            logStr = 'LOG' + curDate + ': ' + str(outStr) + errString
            logStamp = time.strftime("[%m_%d_%Y]")
            print logStr
            with open('session_log_' + logStamp + '.txt', "a") as f:
                f.write(logStr + '\n')
                f.close()
        return

    @staticmethod
    def string_replace(userString, oldString, newString):
        """This function replaces a substring and returns the new string

        :param userString: The string to be modified
        :param oldString: The current substring
        :param newString: The substring that will be inserted
        :returns: A newly modified string
        """
        contents = userString[:]
        isOldName = True
        oldLength = len(oldString)
        while isOldName == True:
            stringLocals = [match.start() for match in re.finditer(re.escape(oldString), contents)]
            if len(stringLocals) > 0:
                isOldName = True
                contents = contents[:stringLocals[0]] + newString + contents[(stringLocals[0] \
                                                                              + oldLength):]
            else:
                isOldName = False
        return contents

    @staticmethod
    def replace_name_in_file(filePath, oldString, newString):
        """ Change references from oldString to newString

        :param filePath: File to be modified
        :param oldString: The current substring
        :param newString: The substring that will be inserted
        """
        with open(filePath, "r+b") as f:
            contents = f.read()
            f.close()
        isOldName = True
        oldLength = len(oldString)
        while isOldName == True:
            stringLocals = [match.start() for match in re.finditer(re.escape(oldString), contents)]
            if len(stringLocals) > 0:
                isOldName = True
                contents = contents[:stringLocals[0]] + newString + contents[(stringLocals[0] \
                                                                              + oldLength):]
            else:
                isOldName = False
        with open(filePath, "w+b") as f:
            f.write(contents)
            f.close()
        return
    

    def mask_features(self, ksdkPath, ksdkVersion, featureList, partName, packName):
        """ Mask off features based on what is available for this part

        :param ksdkPath: Absolute path of KSDK installation being used
        :param ksdkVersion: version of the KSDK being used
        :param featureList: List of features to be modified
        :param partName: Name of target part
        """
        
        #FIXME Radka refactor code to avoid circular depedencies another way
        import ksdkObj 
        directoryHelper = ksdkObj.kinetisSDK(ksdkPath).getDirectoryStructureHelper()
        featureFile = ksdkPath + directoryHelper.getFeature_hFileLocation(partName, True)   

        preProc = ['#if', '#elif', '#endif']

        portCount = 0
        dmaCount = 0
        tsiVersion = 0

        partFeatures = []
        featIndex = 0
        lineIndex = 0
        preProcType = 4
        index = 0
        featLine = '/* SOC module features */'
        defLine = 'defined(CPU_' + packName + ')'

        # Get line where SOC module features begin
        with open(featureFile, "rb") as f:
            for index, newLine in enumerate(f):
                if featLine in newLine:
                    featIndex = index
                    lineIndex = featIndex
                    break
            f.close()

        #self.debug_log('Feature start: ' + str(featIndex))

        # Get line where the package is defined, if defined
        with open(featureFile, "rb") as f:
            for i in xrange(featIndex):
                f.next()
            for index, newLine in enumerate(f):
                if '#if' in newLine:
                    preProcType = preProc.index('#if')
                elif '#elif' in newLine:
                    preProcType = preProc.index('#elif')
                if defLine in newLine:
                    if preProcType == preProc.index('#if'):
                        if index > featIndex + 100:
                            lineIndex = featIndex
                            break
                    if preProcType == preProc.index('#elif'):
                        if index > featIndex + 300:
                            lineIndex = featIndex
                            break
                    else:
                        lineIndex = index
                        break
            f.close()

        #self.debug_log('Index start: ' + str(lineIndex))

        # Begin feature checking from package check to end of section
        with open(featureFile, "rb") as f:
            for i in xrange(lineIndex):
                f.next()
            for newLine in f:
                if preProcType < 2:
                    if preProc[preProcType + 1] in newLine:
                        break
                if '#define FSL_FEATURE_SOC' in newLine:
                    partFeatures.append(newLine)
                    #print newLine
            f.close()

        smartCardCnt = 0
        smartCardUart = 0
        index = 0
        while index < len(featureList):
            isValid = False
            if featureList[index] == 'sai':
                temp = '_I2S_'
            elif featureList[index] == 'rnga':
                temp = '_RNG_'
            elif featureList[index] == 'flexbus':
                temp = '_FB_'
            elif featureList[index] == 'quadtmr':
                temp = '_TMR_'
            elif featureList[index] == 'qspi':
                temp = '_QuadSPIO_'
            elif featureList[index] == 'sdramc':
                temp = '_SDRAM_'
            elif featureList[index] == 'smartcard':
                temp = '_ENVSIM_'
            elif featureList[index] == 'lmem_cache':
                temp = '_LMEM_'
            else:
                temp = '_' + featureList[index].upper() + '_'
            #print 'List: ' + temp
            self.debug_log('List: ' + temp)
            for p in partFeatures:
                #self.debug_log('File: ' + p)
                if temp in p:
                    #self.debug_log(p)
                    countEndIndex = p.rfind(')')
                    #self.debug_log(p[countEndIndex - 1:countEndIndex])
                    insCount = int(p[countEndIndex - 1:countEndIndex])
                    if insCount < 1:
                        #self.debug_log('Zero instance')
                        isValid = False
                    else:
                        isValid = True
            if isValid == False:
                #self.debug_log('Zero instance')
                featureList[index] = 'N/A'
            index += 1
        isValid = True
        while isValid:
            try:
                featureList.remove('N/A')
            except ValueError:
                isValid = False

        # Check for special features
        copCount = 0
        isIrtc = 0
        with open(featureFile, "rb") as f:
            for newLine in f:
                if 'FSL_FEATURE_SIM_HAS_COP_WATCHDOG' in newLine:
                    countEndIndex = newLine.rfind(')')
                    #self.debug_log(newLine[countEndIndex - 1:countEndIndex])
                    copCount = int(newLine[countEndIndex - 1:countEndIndex])
                if 'FSL_FEATURE_SOC_PORT_COUNT' in newLine:
                    countEndIndex = newLine.rfind(')')
                    #self.debug_log(p[countEndIndex - 1:countEndIndex])
                    portCount = int(newLine[countEndIndex - 1:countEndIndex])
                if 'FSL_FEATURE_SOC_DMA_COUNT' in newLine:
                    countEndIndex = newLine.rfind(')')
                    #self.debug_log(p[countEndIndex - 1:countEndIndex])
                    dmaCount = int(newLine[countEndIndex - 1:countEndIndex])
                if 'FSL_FEATURE_TSI_VERSION' in newLine:
                    countEndIndex = newLine.rfind(')')
                    tsiVersion = int(newLine[countEndIndex - 1:countEndIndex])
                if 'FSL_FEATURE_RTC_IS_IRTC' in newLine:
                    countEndIndex = newLine.rfind(')')
                    isIrtc = int(newLine[countEndIndex - 1:countEndIndex])
                if 'FSL_FEATURE_SOC_EMVSIM_COUNT' in newLine:
                    countEndIndex = newLine.rfind(')')
                    smartCardCnt = int(newLine[countEndIndex - 1:countEndIndex])
                if 'FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT' in newLine:
                    countEndIndex = newLine.rfind(')')
                    smartCardUart = int(newLine[countEndIndex - 1:countEndIndex])
            f.close()

        if copCount > 0:
            featureList.append('cop')

        if isIrtc > 0:
            tempI = featureList.index('rtc')
            featureList[tempI] = 'irtc'

        if smartCardCnt > 0:
            featureList.append('smartcard')

        if smartCardUart > 0:
            featureList.append('smartcard')

        return [portCount, dmaCount, tsiVersion]

    @staticmethod
    def get_smartcard_type(ksdkPath, partName):
        """ Returns smartcard type from feature file

        : param ksdkPath: Path to KSDK parent directory
        : param partName: Family name of part
        """
        #FIXME Radka refactor code to avoid circular depedencies another way
        import ksdkObj
        directoryStructureHelper = ksdkObj.kinetisSDK(ksdkPath).getDirectoryStructureHelper()
        featureFile = ksdkPath + directoryStructureHelper.getFeature_hFileLocation(partName, True)

        smartCardDirect = 0
        smartCardUart = 0
        with open(featureFile, "rb") as f:
            for newLine in f:
                if 'FSL_FEATURE_SOC_EMVSIM_COUNT' in newLine:
                    countEndIndex = newLine.rfind(')')
                    smartCardDirect = (int(newLine[countEndIndex - 1:countEndIndex])) << 8
                if 'FSL_FEATURE_UART_HAS_SMART_CARD_SUPPORT' in newLine:
                    countEndIndex = newLine.rfind(')')
                    smartCardUart = int(newLine[countEndIndex - 1:countEndIndex])
            f.close()

        smartType = smartCardDirect | smartCardUart

        #print 'Smart Type' + str(smartType)

        return smartType

    @staticmethod
    def list_files(filePath):
        """ Returns list of all files in path

        :param filePath: absolute path to seach for files

        :returns: A list of file names in the path
        """

        try:
            return [f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))]
        except:
            return []

    @staticmethod
    def list_dirs(dirPath):
        """ Returns list of all directories in path

        :param dirPath: absolute path to seach for directories

        :returns: A list of directory names in the path
        """

        return [f for f in os.listdir(dirPath) if os.path.isdir(os.path.join(dirPath, f))]

    @classmethod
    def update_file(cls, oldFile, oldName, newName):
        """ Updates file to change name and references to new name

        :param oldFile: path to file
        :param oldName: refrence name to be changed in file and in file name
        :param newName: new name to be used
        """

        newFile = cls.string_replace(oldFile, oldName, newName)
        #print oldFile
        #print newFile
        os.rename(oldFile, newFile)
        cls.replace_name_in_file(newFile, oldName, newName)
        return

    @classmethod
    def usb_make_list_update(cls, isDevice, filePath, cloneName, newName):
        """ Special file update for usb CMakeLists.txt

        :param isDevice: is USB device?
        :param filePath: path to CMakeLists.txt
        :param cloneName: name from clonable list in GUI
        :param newName: name of the new project being created
        """

        if isDevice:
            oldMk = 'dev_' + cloneName[cloneName.rfind('device-') + len('device-'):]
            oldMk = cls.string_replace(oldMk, '-', '_')
            newMk = 'dev_' + cloneName[cloneName.rfind('device-') + len('device-'):cloneName.rfind('-')]
            newMk = cls.string_replace(newMk, '-', '_') + '_' + newName
            cls.replace_name_in_file(filePath, oldMk, newMk)
        else:
            oldMk = cloneName[cloneName.find('-') + 1:]
            oldMk = cls.string_replace(oldMk, '-', '_')
            newMk = cloneName[cloneName.find('-') + 1:cloneName.rfind('-')]
            newMk = cls.string_replace(newMk, '-', '_') + '_' + newName
            cls.replace_name_in_file(filePath, oldMk, newMk)
        return

    @staticmethod
    def cdt_fix_post_xml(dirPath):
        """ Fixed .cproject files after using xml write in python.

        :param dirPath: path to directory containing .cproject file
        """

        #Remove / if present in path
        if dirPath[-1:] == '/':
            dirPath = dirPath[:-1]

        #Edit file to make it CDT project (add <?fileVersion 4.0.0?>)
        with open(dirPath + '/.cproject', "r+b") as f:
            contents = f.read()
            f.close()
        with open(dirPath + '/.txt', "wb") as f:
            f.write(contents)
            f.close()
        with open(dirPath + '/.txt', "rb") as f:
            header = f.readline()
            content = f.read()
            f.close()
        with open(dirPath + '/.txt', "wb") as f:
            fileVer = "<?fileVersion 4.0.0?>"
            f.write(header + fileVer + content)
            f.close()
        shutil.copy(dirPath + '/.txt', dirPath + '/.cproject')

        #Clean up temporary file
        os.remove(dirPath + '/.txt')
        return

    @staticmethod
    def check_proj_name(nameString):
        """ Checks project name for validity

        :param nameString: string containing the project name

        :returns: True if string is valid, False if invalid
        """

        isMatch = re.findall(r'[^0-9a-zA-Z_-]', nameString)

        if isMatch or not nameString:
            return False
        else:
            return True

    @staticmethod
    def check_wksp_name(nameString):
        """ Checks workspace path for validity

        :param nameString: string containing the workspace path

        :returns: True if string is valid, False if invalid
        """

        isMatch = re.findall(r'[^.0-9a-zA-Z_:/\\-]', nameString)

        if isMatch:
            return False
        else:
            return True

    @staticmethod
    def pretty_xml(xmlElement, xmlEncoding):
        """ Edit xml element to make it more readable

        :param xmlElement: xml element to formatted
        :param xmlEncoding: xml encoding

        :returns: Tab formatted xml string to be parsed
        """

        origString = xml.etree.ElementTree.tostring(xmlElement, xmlEncoding)

        newString = xml.dom.minidom.parseString(origString)

        #FIXME Radka find out why it is not possible to import kds project which it is formatted
        #return newString.toprettyxml(indent='\t')
        return origString

    @staticmethod
    def get_rel_path(pathOrigin, pathDest):
        """ Takes two paths, and returns a string to navigate to the second from the first

        :param pathOrigin: String containing the path to navigate from
        :param pathDest: String containing the path to navigate to

        :returns: String of relative path
        """

        return os.path.relpath(pathDest, pathOrigin)

    @staticmethod
    def get_all_indices(strName, charName):
        """ Returns a list of all indices of a char in string

        :param strName: String to search
        :param charName: Character to search for
        """

        indices = []

        for i, getChar in enumerate(strName):
            if getChar == charName:
                indices.append(i)

        return indices

    @staticmethod
    def update_json_file(fileName, valueKey, newVal):
        """ Updated JSON file with new value for specified key

        :param fileName: Name of file to update (needs path)
        :param valueKey: Key of JSON entry to update
        :param newVal: New value to write
        """

        newData = []

        with open(fileName, "r+") as f:
            origData = json.load(f)
            newData.append(origData[0])
            f.close()

        newData[0][valueKey] = newVal

        with open(fileName, "w+") as f:
            json.dump(newData, f, sort_keys=True, indent=2)
            f.close()

        return
