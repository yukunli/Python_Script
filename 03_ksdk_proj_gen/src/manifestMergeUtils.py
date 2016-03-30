'''
Created on Jan 6, 2016

@author: B49736
'''
import os
import xml.etree.ElementTree as ET
import decimal

import Constants

# API_ELEMENT = 'api'
# API_VERSION_ATR = 'version'
# KSDK_TAG_ELEMENT = 'ksdk'
# COMPILER_TAG_NAME = 'compiler'
# COMPILERS_TAG_NAME = 'compilers'
# FOR_ATR = 'for'
# ID_ATR = 'id'
# DEFAULT_VERSION = "1.0"
# BOARD_TAG = 'board'
# BOARDS_TAG = 'boards'

class ManifestMergeUtils():

    
    
    @staticmethod
    def getAllManifestFiles(sdkPath):
        """
        @param sdkPath: string path to sdk directory
        @return list of files in input directory which end with .manifest
        """
        manifestFiles = []
        if os.path.isdir(sdkPath):
            manifestFiles = [f for f in os.listdir(sdkPath) if os.path.isfile(os.path.join(sdkPath,f)) and f.endswith('manifest.xml')]
        return manifestFiles
    
    @staticmethod
    def getElementTree(filePath):
        """
        @param filePath string containing path to xml file
        @return elementTree: xml.entree.ElementTree representing of manifest tree or None
        """
        tree = None
        if os.path.isfile(filePath):
            tree = ET.parse(filePath)
            #FIXME Radka catch exceptions ?
        return tree
    
    @staticmethod
    def getManifestVersion(elementTree):
        """
        @param elementTree: xml.entree.ElementTree representing of manifest tree
        @return number - double  
        """
        root = elementTree.getroot()
        versionList = root.findall(Constants.API_TAG_ELEMENT)
        if len(versionList) != 1:
            return -1
        version = versionList[0].get(Constants.API_VERSION_ATR)
        if len(version) < 3:
            return -1;
        return decimal.Decimal(version[:3])
        
    @staticmethod
    def makeDiffOfTagsContent(currentElem, newElem):
        """
        @param currentElem: xml.entree.ElementTree.Element
        @param newElem: xml.entree.ElementTree.Element
        @return boolean flag whether they have same content or not 
        """
        if currentElem == newElem:
            return True
        if currentElem is None or newElem is None:
            return False
        #compare tag name
        if currentElem.tag != newElem.tag:
            return False
        
        #compare tags
        curAttrs = currentElem.attrib
        newAttrs = newElem.attrib
        if len(curAttrs) != len(newAttrs):
            return False
        for key, value in curAttrs.iteritems():
            if key not in newAttrs:
                return False
            elif value != curAttrs[key]:
                return False
        
        #compare children
        curChildren = list(currentElem)
        newChildren = list(list(newElem))
        if len(curChildren) != len(newChildren):
            return False
        
        
        for curChild in curChildren:
            tagNotFound = False
            for newChild in newChildren:
                if ManifestMergeUtils.makeDiffOfTagsContent(curChild, newChild):
                    tagNotFound = True
                    newChildren.remove(newChild)
                    break
            if not tagNotFound:
                return False
        
        #compare text
        if currentElem.text != newElem.text:
            return False
        
        return True
    
    @staticmethod
    def getFirstChildElementByName(parentElement, name):
        """
        @param parentElement: xml.etree.ElementTree.Element xml element to find its first child
        @param name: String name of the child which is going to get
        @return xml.etree.ElementTree.Element or None which has input name and its parent is input element 
        """
        if parentElement is not None:
            listOfElem = parentElement.findall(name)
            if len(listOfElem) >= 1:
                return listOfElem[0]
        return None    
    
            
    @staticmethod
    def _checkComponentsAttributes(tag):
        """
        Checks attributes of the 'components' tag, the following attributes are accepted:
        - tag does not contain any attribute
        - tag contains two attributes named 'for' and 'id'
        @param tag instance of the 'components' tag
        @return boolean flag whether element is OK or not
        """        
        if len(tag.attrib) == 0:
            return True
        if (Constants.FOR_ATR not in tag.attrib) or (Constants.ID_ATR not in tag.attrib) or len(tag.attrib) != 2:
            return False
        
    @staticmethod
    def _getComponentTagAttribute(tag, attributeName):
        """
        @return attribute of input tag which has input name 
        """
        if attributeName in tag.attrib:
            return tag.attrib[attributeName]
        else:
            return None
        
            
    @staticmethod
    def findSubTagsForMerge(currentRoot, addRoot, tagName, allowAttrs, subTagName, keyAttrName, key2AttrName, key3AttrName, forMerge):
        """
        @param currentRoot: xml.etree.ElementTree.Element root element of base manifest file
        @param addRoot:  xml.etree.ElementTree.Element root element of manifest file which is going to merge to base manifest
        @param  tagName: String name of tag which is going to be merge
        @param allowAttr: boolean flag whether attributes are allowed or not (it is used only for components tag)
        @param subTagName: String name of subtags of tag which is going to be merge
        @param keyAttrName: String name of attribute of subtags which is going to be controlled while merging
        @param key2AttrName: String name of attribute of subtags which is going to be controlled while merging
        @param key3AttrName: String name of attribute of subtags which is going to be controlled while merging
        @param forMerge: map where tags which are going to be added to basic manifest file are stored   
        """
        cur_list_elem = ManifestMergeUtils.getFirstChildElementByName(currentRoot, tagName)
        add_list_elem = ManifestMergeUtils.getFirstChildElementByName(addRoot, tagName)
        if cur_list_elem is None:
            if add_list_elem is None:
                return True
            cur_list_elem = ET.SubElement(currentRoot, add_list_elem.tag, add_list_elem.attrib)
        
        if add_list_elem is None:
            return True
        
        if len(cur_list_elem.attrib) > 0 or len(add_list_elem.attrib) > 0:
            if not allowAttrs:
                return False
            if (not ManifestMergeUtils._checkComponentsAttributes(cur_list_elem)) or ( not ManifestMergeUtils._checkComponentsAttributes(add_list_elem)):
                return False
            curForAtr = ManifestMergeUtils._getComponentTagAttribute(cur_list_elem, Constants.FOR_ATR)
            addForAtr = ManifestMergeUtils._getComponentTagAttribute(add_list_elem, Constants.FOR_ATR)
            if curForAtr != addForAtr:
                return False
            curIdAtr = ManifestMergeUtils._getComponentTagAttribute(cur_list_elem, Constants.ID_ATR)
            addIdAtr = ManifestMergeUtils._getComponentTagAttribute(add_list_elem, Constants.ID_ATR)
            if curIdAtr != addIdAtr:
                return False
        
        subTagIds = set([])
        addChildrenList = add_list_elem.findall(subTagName)
        if len(addChildrenList) > 0:
            curChildrenList = cur_list_elem.findall(subTagName)
            if len(curChildrenList) == 0:
                return False
            for addElem in addChildrenList:
                if keyAttrName not in addElem.attrib:
                    return False
                addKeyAttrVal = addElem.attrib[keyAttrName]
                
                if key2AttrName is not None:
                    if key2AttrName not in addElem.attrib:
                        return False
                    addKey2AttrVal = addElem.attrib[key2AttrName]
                else:
                    addKey2AttrVal = None
                
                if key3AttrName is not None:
                    if key3AttrName not in addElem.attrib:
                        addKey3AttrVal = ''
                    else:
                        addKey3AttrVal = addElem.attrib[key3AttrName]
                else:
                    addKey3AttrVal = ''
                    
                if 'version' not in addElem.attrib:
                    addVersion = Constants.DEFAULT_VERSION
                else:
                    addVersion = addElem.attrib['version']
                
                subTagValueId = addKeyAttrVal + ('' if addKey2AttrVal is None else addKey2AttrVal) + ('' if addKey3AttrVal is None else addKey3AttrVal)
                if subTagValueId in subTagIds:
                    return False
                else:
                    subTagIds.add(subTagValueId)
                
                foundSameElem = False
                for curElem in curChildrenList:
                    if keyAttrName not in curElem.attrib:
                        return False
                    curKeyAttr = curElem.attrib[keyAttrName]
                    
                    #check second key
                    if key2AttrName is not None:
                        if key2AttrName not in curElem.attrib:
                            return False
                        curKey2Attr = curElem.attrib[key2AttrName]
                        matchKey2 = addKey2AttrVal == curKey2Attr
                    else:
                        matchKey2 = True
                        
                    #check third key
                    if key3AttrName is not None:
                        curKey3AttrVal = ''
                        if key3AttrName in curElem.attrib:
                            curKey3AttrVal = curElem.attrib[key3AttrName]
                        matchKey3 = addKey3AttrVal == curKey3AttrVal
                    else:
                        matchKey3 = True
                        
                    # check version
                    if 'version' not in curElem.attrib:
                        curVersion = Constants.DEFAULT_VERSION
                    else:
                        curVersion = curElem.attrib['version']
                    
                    if curKeyAttr == addKeyAttrVal and matchKey2 and matchKey3 and curVersion == addVersion:
                        if not ManifestMergeUtils.makeDiffOfTagsContent(curElem, addElem):
                            return False
                        foundSameElem = True
                        curChildrenList.remove(curElem)
                        break
                
                if not foundSameElem:
                    forMerge[addElem] = cur_list_elem

        return True                

            
            
        
        
         
