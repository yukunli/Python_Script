'''
Created on Jan 6, 2016

@author: Radka Povalova
'''

import os
from manifestMergeUtils import ManifestMergeUtils
import Constants

#minimal format version
MIN_FORMAT_VERSION = 1.2

class ManifestSelectionStrategy():
    
    KSDK_MANIFEST_NAME = 1
    VALID_FORMAT_VERSION = 2
    ANY_OTHER_FILE = 3
    

class ManifestMerge():
    """
    Class for merging of KSDK manifest
    """
    
    def __init__(self, sdkPath):
        self.sdkPath = sdkPath
    
    def getManifestDocument(self):
        """
        @return: ElementTree which contains merged manifest
        """
        manifestFiles = ManifestMergeUtils.getAllManifestFiles(self.sdkPath)
        if not manifestFiles:
            return None
        defaultManifestFile = ''
        defaultManifestFormatVersion = 0.0
        elementTree = None
        strategies = [ManifestSelectionStrategy.KSDK_MANIFEST_NAME, ManifestSelectionStrategy.VALID_FORMAT_VERSION, ManifestSelectionStrategy.ANY_OTHER_FILE]
        for strategy in strategies:
            for f in manifestFiles:
                isKsdkName = f == 'ksdk_manifest.xml'
                if strategy == ManifestSelectionStrategy.KSDK_MANIFEST_NAME:
                    matchManifestNameWithStrategy = isKsdkName
                elif strategy == ManifestSelectionStrategy.VALID_FORMAT_VERSION:
                    matchManifestNameWithStrategy = not isKsdkName
                elif strategy == ManifestSelectionStrategy.ANY_OTHER_FILE:
                    matchManifestNameWithStrategy = True
                else:
                    matchManifestNameWithStrategy = False
                    
                if matchManifestNameWithStrategy:
                    elementTree = ManifestMergeUtils.getElementTree(os.path.join(self.sdkPath, f))
                    if elementTree is not None:
                        defaultManifestFormatVersion = ManifestMergeUtils.getManifestVersion(elementTree)
                        if strategy == ManifestSelectionStrategy.KSDK_MANIFEST_NAME:
                            isOK = defaultManifestFormatVersion >= MIN_FORMAT_VERSION
                        elif strategy == ManifestSelectionStrategy.VALID_FORMAT_VERSION:
                            isOK = defaultManifestFormatVersion >= MIN_FORMAT_VERSION
                        elif strategy == ManifestSelectionStrategy.ANY_OTHER_FILE:
                            isOK = defaultManifestFormatVersion >= 0
                        else:
                            isOK = False
                    
                    if isOK:
                        defaultManifestFile = f
                        break
                    elementTree = None
            
            if elementTree is not None:
                break    
        
        if (elementTree is not None) and (len(manifestFiles) > 1) and defaultManifestFormatVersion >= MIN_FORMAT_VERSION:
            for f in manifestFiles:
                if f != defaultManifestFile:
                    self._mergeManifest(elementTree, f, defaultManifestFormatVersion)
                    
        # for debugging            
        #elementTree.write("filename.xml")
        return elementTree    
    
    def _mergeManifest(self, manifestElementTree, manifestFile, formatVersion):
        """
        @param manifestElementTree: xml.etree.ElementTree etree of base manifest
        @param manifestFile: String - name of manifest file which is going to merge to basic manifest file
        @param formatVersion: Double - format version of default manifest
        """
        newElementTree = ManifestMergeUtils.getElementTree(os.path.join(self.sdkPath, manifestFile))
        if newElementTree is None:
            return
        newElementTreeVersion = ManifestMergeUtils.getManifestVersion(newElementTree)
        if newElementTreeVersion != formatVersion:
            return
        
        curRoot = manifestElementTree.getroot()
        addRoot = newElementTree.getroot()
        
        
        # compare ksdk tag
        cur_ksdkElems = curRoot.findall(Constants.KSDK_TAG_ELEMENT)
        new_ksdkElems = addRoot.findall(Constants.KSDK_TAG_ELEMENT)
        if len(cur_ksdkElems) != 1 or len(new_ksdkElems) != 1:
            return
        if not ManifestMergeUtils.makeDiffOfTagsContent(cur_ksdkElems[0], new_ksdkElems[0]):
            return
        
        forMerge = {}
        
        #merge compilers
        result = ManifestMergeUtils.findSubTagsForMerge(curRoot, addRoot, Constants.COMPILERS_TAG_NAME, False, Constants.COMPILER_TAG_NAME, "name", None, None, forMerge)
        if not result:
            return
        
        #merge toolchains
        result = ManifestMergeUtils.findSubTagsForMerge(curRoot, addRoot, Constants.TOOLCHAINS_TAG_NAME, False, Constants.TOOLCHAIN_TAG_NAME, "name", None, None, forMerge)
        if not result:
            return
        
        #merge tools
        result = ManifestMergeUtils.findSubTagsForMerge(curRoot, addRoot, Constants.TOOLS_TAG_NAME, False, Constants.TOOL_TAG_NAME, 'id', None, None, forMerge)
        if not result:
            return
        
        #merge boards
        result = ManifestMergeUtils.findSubTagsForMerge(curRoot, addRoot, Constants.BOARDS_TAG_NAME, False, Constants.BOARD_TAG_NAME, "id", None, None, forMerge)
        if not result:
            return
        
        #merge devices
        result = ManifestMergeUtils.findSubTagsForMerge(curRoot, addRoot, Constants.DEVICES_TAG_NAME, False, Constants.DEVICE_TAG_NAME, Constants.DEVICE_FULL_NAME_ATR, None, None, forMerge)
        if not result:
            return
        
        #merge components
        result = ManifestMergeUtils.findSubTagsForMerge(curRoot, addRoot, Constants.COMPONENTS_TAG_NAME, True, Constants.COMPONET_TAG_NAME, "name", "type", "device", forMerge)
        if not result:
            return
        
        for key, value in forMerge.iteritems():
            numberOfChildren = len(list(value))
            value.insert(numberOfChildren, key)
        
            
            
        
        
