'''
Created on Dec 7, 2015

Helper class for getting information about directory structure

@author: B49736 - Radka Povalova
'''

import os

# Name for platform folder
PLATFORM_FOLDER_NAME = 'platform'
# Name for devices folder 
DEVICES_FOLDER_NAME = 'devices'
# Prefix of SWT Content file
SW_CONTENT_FILE_PREFIX = 'SW-Content-Register-KSDK'
# List of license file names in new ksdk version (2.0 and higher)
LICENCE_NAME_LIST = ["LA_OPT_Base_License.htm", "LA_OPT_HOST_TOOL.htm"]

class RTOSType():
    # FreeRTOS flag
    FreeRTOS = 1
    # uCOSII flag
    uCOSII = 2
    # uCOSIII flag
    uCOSIII = 3

class DirectoryStructureHelper():
    
    def __init__(self, isNewKsdkVersion = False):
        self.isNewKsdkVersion = isNewKsdkVersion
    
    def getCMSISIncludeDirectory(self, shouldStartWithPathSeparator = True):
        """
        Get path to CMSIS/Include directory, it is different for KSDK 1.3 and 2.0. It is relative to ksdk directory
        : param shouldStartWithPathSeparator flag path should start with file separator
        """
        cmsisPath = "CMSIS" + os.sep + "Include"
        if not self.isNewKsdkVersion:
            cmsisPath = PLATFORM_FOLDER_NAME + os.sep + cmsisPath
        if shouldStartWithPathSeparator:
            cmsisPath = os.sep + cmsisPath
        return cmsisPath 
    
    def getDevicesDirectory(self, shouldStartWithPathSeparator = True, shouldEndWithPathSeparator = True):
        """
        Get path to devices directory. Path is relative to ksdk directory.
        : param shouldStartWithPathSeparator flag path should start with file separator
        """
        devicesPath = DEVICES_FOLDER_NAME
        if shouldEndWithPathSeparator:
            devicesPath = devicesPath + os.sep
        if not self.isNewKsdkVersion:
            devicesPath = PLATFORM_FOLDER_NAME + os.sep + devicesPath
        if shouldStartWithPathSeparator:
            devicesPath = os.sep + devicesPath
        return devicesPath
    
    def getFeature_hFileLocation(self, partName = '', shouldStartWithPathSeparator = True):
        """
        Get path to _feature.h file. Path is relative to ksdk directory.
        : param partName: Family name of part
        : param shouldStartWithPathSeparator flag path should start with file separator
        """
        if not self.isNewKsdkVersion:
            featureFile = os.path.join(PLATFORM_FOLDER_NAME, DEVICES_FOLDER_NAME, partName, "include", partName + '_features.h')
        else:
            featureFile = os.path.join(DEVICES_FOLDER_NAME, partName, partName + '_features.h')
        if shouldStartWithPathSeparator:
            featureFile = os.path.join(os.sep, featureFile)
        return featureFile
    
    def getUtilitiesDirectory(self, deviceName, shouldStartWithPathSeparator = True, shouldEndWithPathSeparator = True):
        """
        Get path to utilities directory. It is relative to ksdk directory
        :param deviceName 
        :param shouldStartWithPathSeparator flag whether path should start with path separator
        :param shouldEndWithPathSeparator flag whether path should end with path separator
        """
        utilitiesPath = "utilities"
        if shouldEndWithPathSeparator:
            utilitiesPath = utilitiesPath + os.sep
        if not self.isNewKsdkVersion:
            utilitiesPath = os.path.join(PLATFORM_FOLDER_NAME, deviceName, utilitiesPath)
        else:
            utilitiesPath = os.path.join(DEVICES_FOLDER_NAME, deviceName, utilitiesPath)
        if shouldStartWithPathSeparator:
            utilitiesPath = os.sep + utilitiesPath
        return utilitiesPath
    
    def getDriversDirectory(self, deviceName, shouldStartWithPathSeparator = True, shouldEndWithPathSeparator = True):
        """
        Get path to drivers directory. It is relative to ksdk directory
        :param shouldStartWithPathSeparator flag whether path should start with path separator
        :param shouldEndWithPathSeparator flag whether path should end with path separator
        """
        driversPath = "drivers"
        if shouldEndWithPathSeparator:
            driversPath = driversPath + os.sep
        if not self.isNewKsdkVersion:
            driversPath = os.path.join(PLATFORM_FOLDER_NAME, driversPath)
        else:
            driversPath = os.path.join(DEVICES_FOLDER_NAME, deviceName, driversPath)
        if shouldStartWithPathSeparator:
            driversPath = os.sep + driversPath
        return driversPath
    
    
    def getLinkerPath(self, device, linkerName, shouldStartWithPathSeparator = True):
        # FIXME Radka rework to load from manifest
        ending = ''
        if linkerName == 'arm':
            ending = 'scf'
        elif linkerName == 'iar':
            ending = 'icf'
        elif linkerName == 'gcc':
            ending = 'ld'
        path = os.path.join(DEVICES_FOLDER_NAME, device[1], linkerName, device[0] + '_flash.' + ending)
        if not self.isNewKsdkVersion:
            path = os.path.join(PLATFORM_FOLDER_NAME, path)
        if shouldStartWithPathSeparator:
            path = os.sep + path 
        return path
    
    def getListOfStartupFiles(self, deviceName, linkerName, shouldStartWithPathSeparator = True):
        # FIXME Radka rework to load from manifest
        listOfStartupFiles = []
        listOfStartupFiles.append(os.path.join(DEVICES_FOLDER_NAME, deviceName, "system_" + deviceName + ".c"))
        listOfStartupFiles.append(os.path.join(DEVICES_FOLDER_NAME, deviceName, "system_" + deviceName + ".h"))
        listOfStartupFiles.append(os.path.join(DEVICES_FOLDER_NAME, deviceName, linkerName, "startup_" + deviceName + ".S"))
        if shouldStartWithPathSeparator:
            listOfStartupFiles = [os.sep + l for l in listOfStartupFiles]
        return listOfStartupFiles
    
    def getUserLinkedExamplesPath(self, boardName):
        """
        @param boardName: string name of board
        @return string value which is path to folder where user application for quick generation should be saved. 
        """
        if self.isNewKsdkVersion:
            return 'boards/' + boardName + '/user_apps'
        else:
            return 'examples' + boardName + '/user_apps'
            
            
                
                
                
                