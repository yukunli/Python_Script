# -*- coding: cp936 -*-

from xml.etree import ElementTree as ET
import  xml.dom.minidom
import re
import os
import sys
from collections import Counter


import time

global fail_num
global SDK_Source
global verification_case
global SDK_Path
global componttype_List
global result
global fail_num

def Read_Path_and_Run():
    global SDK_Path
    global SDK_Source
    global Manifest_Info
    global verification_case
    global result
    global fail_num
    if  os.path.exists(SDK_Path):
        if os.path.isdir(SDK_Path):
            file_Path = SDK_Path
            print file_Path
            
            SDK_Source = SDKSource(file_Path)
        
            Manifest_Info = ManifestInfo(file_Path)
            verification_case = Verification(SDK_Source,Manifest_Info)
            verification_case.Get_SDKXML_info()
            ##
            verification_case.verify_board_name()
            verification_case.verify_example_name()
            verification_case.verify_example_category()
            verification_case.verify_example_codeFile()

            verification_case.verify_driver_TYPE()
            verification_case.verify_XMLdriver_dupcheck()
            ##
    else:
        print "This path does not exist"
def put_result():
    global result
    global fail_num
    global Manifest_Info

    head = '---'+Manifest_Info.boardList[0][1]+':\n'
    result_file = open('.\\virify_mainfest_result.yml','a')
    result_file.write( head )
    for i in result:
        result_file.write(i + ': ' + str(result[i]) + '\n')

    print  fail_num
    if fail_num == 0:
         result_file.write(Manifest_Info.boardLst[0][1]+': '+'Verify Finish! Result = PASS \n' )
    else:
        result_file.write(Manifest_Info.boardList[0][1]+': '+'Verify Finish! Result = FAIL '+ str(fail_num) +' times\n' )
        
    result_file.close()
    
##________________________________________________________________________________-

class SDKSource:
    """
    """
    def __init__(self,SDK_path):
        self.SDK_PATH = SDK_path
        self.examples_category = ''
        self.example_codeList =[]
        self.boardList = []
        
        self.examplesPath = ''
        self.CodeFiles = []
        self.driversList=[]
        self.driversPath = ''
        self.driversFiles = []
        self.utilitPath = ''
        self.utilitFiles = []
        self.oTherPath = ''
        self.oTherFiles = []
        self.startupPath = ''
        self.startupFiles = []

        self.board_num = 0  #default one board
        self.examples_num = 0

    def get_SDKS_examples(self):
        """
        """

        board_path = os.listdir(self.SDK_PATH+'/boards')
        examples_Path = self.SDK_PATH+'/boards'+'/'+board_path[0]
        examples_type = os.listdir( examples_Path)

        self.board_num = len( board_path)
        self.boardList = board_path
        print 'The SDK board num is ' + str(self.board_num)
        for exam_type in examples_type:
            example_fold = os.listdir( examples_Path+'/'+exam_type)
            for exam_fold in example_fold:
                example_fold_Path =  examples_Path+'/'+exam_type+'/'+exam_fold     
    ##            print example_fold_Path
                
                for exam_cate in os.listdir(example_fold_Path):
                
                    pattern = re.compile(r'.*\.[chbt]')   #其他的.bin .txt文件会影响
                    if pattern.match(exam_cate):
                        
                        example_name = exam_fold
                        self.examplesPath = 'boards/'+board_path[0]+'/'\
                                            +exam_type+'/'+exam_fold   #"boards/twrk21f120m/demo_apps/hello_world"
                        self.examples_category = exam_type
        
                        #
                        pat = re.compile(r'.*\.c$|.*\.h$',re.I)
                        for exam_src in os.listdir(example_fold_Path) :    
                            if pat.match(exam_src):
                                self.CodeFiles.append(exam_src)
                            
                        new_putle=(board_path[0],self.examples_category,exam_fold,self.CodeFiles[:],self.examplesPath)
                        self.example_codeList.append(new_putle)
                        del self.CodeFiles[:]
                        del self.examplesPath
                        del new_putle
                        del pat
                        #
                        break
                    elif os.path.isdir(example_fold_Path+'/'+exam_cate):
                        exam_cate_Path = example_fold_Path+'/'+exam_cate
                        for exam_inner in os.listdir(exam_cate_Path):
                            
                            pattern = re.compile(r'.*\.[chbt]') 
                            if pattern.match(exam_inner):
                                example_name = exam_cate
                                self.examples_category = exam_type+'/'+exam_fold
                                self.examplesPath = 'boards/'+board_path[0]+'/'\
                                            +exam_type+'/'+exam_fold+'/'+exam_cate   #"boards/twrk21f120m/demo_apps/hello_world"

                                #
                                pat = re.compile(r'.*\.c$|.*\.h$',re.I)
                                for exam_src in os.listdir(exam_cate_Path) :    
                                    if pat.match(exam_src):
                                        self.CodeFiles.append(exam_src)
                                if self.CodeFiles:    
                                    new_putle=(board_path[0],self.examples_category,exam_cate,self.CodeFiles[:],self.examplesPath)
                                    self.example_codeList.append(new_putle)
                                    del self.CodeFiles[:]
                                    del self.examplesPath
                                    del new_putle
                                    del pat
                                #
                                
                                break
                            elif  re.match('.*\.inf',exam_inner):
                                self.examplesPath = 'boards/'+board_path[0]+'/'\
                                            +exam_type+'/'+exam_fold+'/'+exam_cate
                                new_putle=(board_path[0],self.examples_category,exam_cate,self.CodeFiles[:],self.examplesPath)
                                self.example_codeList.append(new_putle)
                                del self.CodeFiles[:]
                                del self.examplesPath
                                del new_putle
                                break
                            elif os.path.isdir(exam_cate_Path+'/'+exam_inner):
                                exam_inner_Path = exam_cate_Path+'/'+exam_inner
    ##                            print exam_inner_Path
                                for exam_code in os.listdir(exam_inner_Path):
                            
                                    pattern = re.compile(r'^.*\.c$|^.*\.h$') 
                                    if pattern.match(exam_code):
                                        example_name = exam_inner
                                        self.examples_category = exam_type+'/'+exam_fold+'/'+ exam_cate
                                        self.examplesPath = 'boards/'+board_path[0]+'/'\
                                                            +exam_type+'/'+exam_fold+'/'+ exam_cate +'/'\
                                                            +exam_inner  #"boards/twrk21f120m/demo_apps/hello_world"
                                        #
                                        pat = re.compile(r'.*\.c|.*\.h',re.I)
                                        for exam_src3th in os.listdir(exam_inner_Path) :    
                                            if pat.match(exam_src3th):
                                                self.CodeFiles.append(exam_src3th)

                                        new_putle=(board_path[0],self.examples_category,exam_inner,self.CodeFiles[:],self.examplesPath)
                                        self.example_codeList.append(new_putle)
                                        del self.CodeFiles[:]
                                        del self.examplesPath
                                        del new_putle
                                        del pat
                                        #
                                        break
                                    elif os.path.isdir(exam_inner_Path+ '/'+ exam_code):
                                        exam_forth_path = exam_inner_Path+ '/'+ exam_code
                                        for exam_forth in os.listdir(exam_forth_path):
                                            pattern4 = re.compile(r'^.*\.c$|^.*\.h$')
                                            if  pattern4.match(exam_forth):
                                                example_name = exam_code
                                                self.examples_category = exam_type+'/'+exam_fold+'/'+ exam_cate+'/'+ exam_inner
                                                self.examplesPath = 'boards/'+board_path[0]+'/'\
                                                                    +exam_type+'/'+exam_fold+'/'+ exam_cate +'/'\
                                                                    +exam_inner+'/'+exam_code  #"boards/twrk21f120m/demo_apps/hello_world"
                                                #
                                                pat = re.compile(r'.*\.c|.*\.h',re.I)
                                                for exam_src4th in os.listdir(exam_forth_path) :    
                                                    if pat.match(exam_src4th):
                                                        self.CodeFiles.append(exam_src4th)

                                                new_putle=(board_path[0],self.examples_category,exam_code,self.CodeFiles[:],self.examplesPath)
                                                self.example_codeList.append(new_putle)
                                                del self.CodeFiles[:]
                                                del self.examplesPath
                                                del new_putle
                                                del pat
                                                #
                                                break
                                    
        self.examples_num = len(self.example_codeList)
        print "get source folder info   success!"
        print 'The SDK examples_num is '+ str(self.examples_num)

    def get_SDK_drivers(self):
        """
        """
        devices_path = os.listdir(self.SDK_PATH+'/devices')
        drivers_Path = self.SDK_PATH+'/devices'+'/'+devices_path[0]

        drivers_type = os.listdir(drivers_Path)  # boards/devices/mk21af
        
        for dri_type in drivers_type:
            dri_type_Path = drivers_Path+'/'+dri_type  # boards/devices/mk21af/xx/
            if os.path.isdir(dri_type_Path): # 是目录？

                if dri_type == 'drivers':
##                    print 3.1
                    pattern1 = re.compile(r'.*\.c|.*\.h')
                    for dri_code in os.listdir(dri_type_Path):
                        match1 = pattern1.match(dri_code)
                        if match1:
                            self.driversFiles.append(dri_code)
                            
                        else:
                             print dri_type_Path+'/ exists no.c/.h file'
                             break
                    self.driversPath = 'devices/'+devices_path[0]+'/'\
                                                    +dri_type
                    newdriverputle = (devices_path[0],self.driversPath,self.driversFiles[:])
                    self.driversList.append(newdriverputle)
                    
                    del self.driversPath
                    del self.driversFiles[:]
                    del newdriverputle
                elif dri_type == 'utilities':

                    pattern2 = re.compile(r'.*\.c|.*\.h')
                    for utilit_code in os.listdir(dri_type_Path):
                        match2 = pattern2.match(utilit_code)
                        if match2:

                           self.utilitFiles.append(utilit_code) 
                        else:
                            print dri_type_Path+'/ exists no.c/.h file' 
                            break
                    self.utilitPath = 'devices/'+devices_path[0]+'/'\
                                                    +dri_type
                    newdriverputle = (devices_path[0],self.utilitPath,self.utilitFiles[:])
                    self.driversList.append(newdriverputle)
                    del self.utilitPath
                    del self.utilitFiles[:]
                    del newdriverputle
                else: # tool folder
##                    print 3.3
                    pass

            elif os.path.isfile(dri_type_Path): #是文件？
                 
                if re.match('system_.*\.',dri_type):
                    self.startupPath = 'devices/'+ devices_path[0]
                    self.startupFiles.append(dri_type)
                    newdriverputle = (devices_path[0],self.startupPath[:],self.startupFiles[:])
                    self.driversList.append(newdriverputle)
                    del self.startupPath
                    del self.startupFiles[:]
                    del newdriverputle
                elif re.match('.*\.h|.*\.c|.*\.svd',dri_type):
                    self.oTherPath = 'devices/'+devices_path[0]
                    self.oTherFiles.append(dri_type)
                    newdriverputle = (devices_path[0],self.oTherPath[:],self.oTherFiles[:])
                    self.driversList.append(newdriverputle)
                    del self.oTherPath
                    del self.oTherFiles[:]
                    del newdriverputle

        print "get source devices info  success! "
##____________________________________________________________________________

class ManifestInfo:
    """
    """
    def __init__(self,SDK_path):
        
        self.SDK_PATH = SDK_path
        tree = ET.parse(self.SDK_PATH + '/ksdk_manifest.xml')
        self.root = tree.getroot()  
        self.boardList = []
        self.example_appsList = []
        self.toolList = []
        self.compilerList = []
        self.driverList = []


        self.board_num = 0
        self.tools_num = 0
        self.examples_num = 0

    def get_Mainfest_board(self):

        brdId = ''
        brdName = ''
        brdUser = ''
          
        for boardsPresent in self.root.findall('boards'):
            for child in boardsPresent.findall('board'):
                brdId = child.get('id')
                brdName = child.get('name')
                brdUser = child.get('user_name')
                newboardputle = (brdId, brdName, brdUser)
                self.boardList.append(newboardputle)
                del newboardputle
        self.board_num = len(self.boardList)
        
        print 'The XML board num is '+str(self.board_num)
        
    def get_Mainfest_tools(self):
        """
        """
        for toolsPresent in self.root.findall('tools'):
            for child in toolsPresent.findall('tool'):
                toolId = child.get('id')
                toolName = child.get('name')
                toolversion = child.get('version')
                toolvendor = child.get('vendor')
                newtoolputle = (toolId, toolName, toolversion, toolvendor)
                self.toolList.append(newtoolputle)
                del newtoolputle
        self.tools_num = len(self.toolList)
        print 'get The platform Mainfest tools   success!'
        print 'The tools_num is '+str(self.tools_num)
    def get_Mainfest_compiler(self):
        """
        """
        for compilersPresent in self.root.findall('compilers'):
            for child in compilersPresent.findall('compiler'):
                compilerName = child.get('name')     
                self.compilerList.append(compilerName)

        print 'get The platform Mainfest complier   success!'

    def get_Mainfest_drv(self):   ##得到所有的driver 的.c 和.h 文件
        """
        :param self.driverList: list of drivers
        """
        global componttype_List
        drvName = ''
        drvtype = ''
        includePaths = []
        sourcePaths = []
        includeFiles = []
        sourceFiles = []
        componttype_List=['driver','utilities','other','middleware',\
                            'os','CMSIS','startup','project_template','debugger','linker']
        for k in range(len(componttype_List)):
            index = 0
            for driversPresent in self.root.findall('components'):
                for componentType in driversPresent.findall('component'):
                    if componentType.get('type') == componttype_List[k]:  ## componttype_List[]
                            drvName = componentType.get('name')
                            drvtype = componentType.get('type')
                            # HACK: for K80 lmem_cache to lmem
                            if drvName == 'lmem_cache':
                                drvName = 'lmem'
                            for sources in componentType.findall('source'):
                                for files in sources.findall('files'):
    ##                                print drvName+':'  + files.get('mask')
##                                    if '_dma_' in files.get('mask'):
##                                        #print 'DMA'
##                                        if self.dmaCount > 0:
##                                            if sources.get('type') == 'src':
##                                                sourcePaths.append(str(sources.get('path')))
##                                                sourceFiles.append(str(files.get('mask')))
##                                            elif sources.get('type') == 'c_include':
##                                                includePaths.append(str(sources.get('path')))
##                                                includeFiles.append(str(files.get('mask')))
##                                    else:
                                    if sources.get('type') == 'src':
                                        sourcePaths.append(str(sources.get('path')))
                                        sourceFiles.append(str(files.get('mask')))
                                    elif sources.get('type') == 'c_include':
                                        includePaths.append(str(sources.get('path')))
                                        includeFiles.append(str(files.get('mask')))

                            #New tuple for each driver containing name and paths
                            newDrvTuple = (drvName,drvtype, sourcePaths[:], includePaths[:], \
                                    sourceFiles[:], includeFiles[:])

                            #Append drvList with new tuple for
                            self.driverList.append(newDrvTuple)
                            del sourcePaths[:]
                            del includePaths[:]
                            del sourceFiles[:]
                            del includeFiles[:]
                            del newDrvTuple
                            index += 1

        print 'get The platform Mainfest drivers   success'

        return
    
    def get_Mainfest_example_apps(self):  
        """
        :param exampleList: list of examples
        """

        boardname = ''
        examples_category = ''
        sourcePaths = []
        includePaths = []
        linkerPaths = []
        includeFiles = []
        sourceFiles = []
        linkerFiles = []
        index = 0
        for boardsPresent in self.root .findall('boards'):
            for boardType in boardsPresent.findall('board'):
                boardname = boardType.get('name')
                for examplesPresent in boardType.findall('examples'):
                    for exampleType in examplesPresent.findall('example'):

                        pattern = re.compile(r'')
                        match = pattern.match(exampleType.get('category'))
                        if match:
                            examples_category = exampleType.get('category')
                            #print examples_category
            
                            exampleName = exampleType.get('name')
                            #print demoName
                            # HACK: for K80 lmem_cache to lmem
        ##                    if drvName == 'lmem_cache':
        ##                        drvName = 'lmem'
                            for sources in exampleType.findall('source'):
                                for files in sources.findall('files'):
                                    if sources.get('type') == 'src':
                                         sourcePaths.append(str(sources.get('path')))
                                         sourceFiles.append(str(files.get('mask')))
                                    elif sources.get('type') == 'c_include':
                                         includePaths.append(str(sources.get('path')))
                                         includeFiles.append(str(files.get('mask')))
                                    elif sources.get('type') == 'linker':
                                         linkerPaths.append(str(sources.get('path')))
                                         linkerFiles.append(str(files.get('mask')))
                            #New tuple for each driver containing name and paths
                            newdemoTuple = (boardname,examples_category,exampleName,\
                                            sourceFiles[:],sourcePaths[:],\
                                            includeFiles[:],includePaths[:],\
                                            linkerFiles[:],linkerPaths[:])

                            #Append drvList with new tuple for
                            self.example_appsList.append(newdemoTuple)
                            del sourceFiles[:]
                            del sourcePaths[:]
                            del includeFiles[:]
                            del includePaths[:]
                            del linkerFiles[:]
                            del linkerPaths[:]
                            del newdemoTuple
                            index += 1
        self.examples_num = len(self.example_appsList)
        print 'get the platform Mainfest examples   success!'
        print 'The examples_num is '+str(self.examples_num)
        del index
                    
##______________________________________________________________________________


class Verification:
    """
    """

    def __init__(self,compare_SDK,compare_XML):
        global fail_num
        self.classSDK = compare_SDK
        self.classXML = compare_XML
        
        self.exampletupleSDK = 0
        self.exampletupleXML = 0
  
        self.longSDK = 0
        self.longXML = 0
        self.aa = 0

    def verify_board_name(self):
        global result
        global fail_num 
        print 'Process: ---compare board_name---'
        if self.classSDK.board_num == self.classXML.board_num and self.classXML.board_num ==1:
            
            board_nameSDK = self.classSDK.boardList[0]
            board_nameXML = self.classXML.boardList[0][1]
            if board_nameSDK == board_nameXML:
                print 'Result: this compare done, success!'
                result['board name' + " --- manifest verification"] = ["OK"]
            else: print 'Result: fail!   board name is inconsistent'
        elif self.classXML.board_num > 1 and self.classSDK.boardList[0]== self.classXML.boardList[1][1]:
            result['board name' + " --- manifest board name"] = ["Repeated Definition"]
            print 'the XML board name Repeated definition'
            fail_num += 1
    
    def verify_example_name(self):
        global result
        example_nameSDK = []
        example_nameXML = []
        
        for i in range(self.aa):
            example_nameSDK.append(self.exampletupleSDK[i][2])
            example_nameXML.append(self.exampletupleXML[i][2])

        print 'Process: ---compare example_name---'
        self.compare(example_nameSDK,example_nameXML,'example_name')
        del example_nameSDK[:]
        del example_nameXML[:]
        
    def verify_example_category(self):
        global result
        example_categorySDK = []
        example_categoryXML = []
        for i in range(self.aa):
            example_categorySDK.append(self.exampletupleSDK[i][1])
            example_categoryXML.append(self.exampletupleXML[i][1])
            
        print 'Process: ---compare example_category---'
        self.compare(example_categorySDK,example_categorySDK,'example_category')
        del example_categorySDK[:]
        del example_categorySDK[:]
        
    def verify_example_codeFile(self):
        """
            compare the .c and .h file under the example folder
        """
        global result
        global fail_num  
        success_num = 0
        unsuccess_num = 0
        example_nameSDK = []
        example_nameXML = []
        example_categorySDK = []
        example_categoryXML = []
        
        name_SDKdict = dict()
        category_SDKdict = dict()
        codefile_SDKdict = dict()
        name_XMLdict = dict()
        category_XMLdict = dict()
        codefile_XMLdict = dict()

        print 'Process: ---compare example_codeFile---'
        for i in range(self.longSDK):
            example_nameSDK.append(self.exampletupleSDK[i][2])
            example_categorySDK.append(self.exampletupleSDK[i][1])

            category_SDKdict[i] = self.exampletupleSDK[i][1]
            name_SDKdict[i] = self.exampletupleSDK[i][2]
            codefile_SDKdict[i] = self.exampletupleSDK[i][3]

            
        for i in range(self.longXML):
            example_nameXML.append(self.exampletupleXML[i][2])
            example_categoryXML.append(self.exampletupleXML[i][1])
       
            category_XMLdict[i] = self.exampletupleXML[i][1]
            name_XMLdict[i] = self.exampletupleXML[i][2]
            codefile_XMLdict[i] = self.exampletupleXML[i][3]+self.exampletupleXML[i][5]

        for i in  range(self.longSDK):
            for j in range(self.longXML):
                if category_SDKdict[i] ==  category_XMLdict[j]:
                    if name_SDKdict[i] ==  name_XMLdict[j]:
                        
                        count = self.mul_compare(codefile_SDKdict[i],codefile_XMLdict[j],category_SDKdict[i],name_SDKdict[i])
                        if count == 1:
                            success_num += 1
                        else: unsuccess_num += 1
                        
                    else: pass
                else: pass
        fail_num += unsuccess_num
        if unsuccess_num == 0:
            result['example code' + " --- manifest verification"] = ["OK"]
        print 'Result: this compare done, success '+str(success_num)+ ' times, unsuccess '+str(unsuccess_num)+' times'

    def  verify_driver_TYPE(self):
        
        driver_typeSDK = []
        driver_typeXML = []
        
        driver_typeSDK = self.classSDK.driversList[0][2]
    
        for i in range(len(self.classXML.driverList)):
            if self.classXML.driverList[i][1]== 'driver' :
                driver_typeXML = driver_typeXML + self.classXML.driverList[i][4]
                driver_typeXML = driver_typeXML + self.classXML.driverList[i][5]
        print 'Process: ---compare driver_TYPE---'
        self.compare(driver_typeSDK,driver_typeXML,'drivers')
        del driver_typeSDK[:]
        del driver_typeXML[:]

    def verify_XMLdriver_dupcheck(self):
        global fail_num
        global componttype_List
        global result
        drvnameList = []
        drvflieList = []
        drvfliedict = dict()
        repeatname_num = 0
        print 'Process: ---mainfest drivers duplicate check---'

        
        for k in range(len(componttype_List)):
            for i in range(len(self.classXML.driverList)):
                if self.classXML.driverList[i][1]== componttype_List[k] :
                    drvnameList.append(self.classXML.driverList[i][0])
                    
                    drvflieList = self.classXML.driverList[i][4]+self.classXML.driverList[i][5]
                    drvfliedict[self.classXML.driverList[i][0]] = drvflieList

            name_dupcheck = Counter(drvnameList)
            for drvname in name_dupcheck:
                if name_dupcheck[drvname] > 1:
                    print 'The driver name '+ drvname + ' is repeated'
                    result['driver name duplication' + " --- manifest repeat"] = drvname
                    repeatname_num += 1
                    fail_num += 1
            for filname in drvfliedict:
                if filname == 'CMSIS':
                    continue
                file_dupcheck = Counter(drvfliedict[filname])
                for j in file_dupcheck:       
                    if file_dupcheck[j] > 1 :
                        result['drivers duplication' + " --- manifest repeat"] = j +' in '+ filname
                        print  'The drivers file '+ j + ' is repeated'
                        fail_num += 1
                        repeatname_num += 1
            drvnameList = []
            drvflieList = []
            drvfliedict = {}
        if repeatname_num == 0:
             result['drivers duplication' + " --- manifest verification"] = ["OK"]
        print 'Result: this compare done. Repeated driver name hava '+str(repeatname_num)      
        
    def compare(self,listSDK,listXML,compare_type):
        global fail_num

        diff1 = list(set(listSDK).difference(listXML))
        diff2 = list(set(listXML).difference(listSDK))

        if not diff1 and not diff2:
            print 'Result: this compare done, success!'
            result[compare_type + " --- manifest verification"] = ["OK"]
            return 1
        else:
            if  diff1:
                    print diff1,' mainftes has less these files\n'
                    result[compare_type + " --- manifest missing"] = diff1
                    fail_num += 1
            if  diff2:
                    print diff2,' mainftes has more these files\n'
                    result[compare_type + " --- manifest redundant "] = diff2
                    fail_num += 1
            return 0
    def mul_compare(self,listSDK,listXML,categoryname,examplename):
   
        diff1 = list(set(listSDK).difference(listXML))
        diff2 = list(set(listXML).difference(listSDK))
        
        if not diff1 and not diff2:
            return 1
        else:
            if  diff1:
                print categoryname+examplename+'  vierify fail!\n', diff1 , ' mainftes has less these files'
                result['examples code' + " --- manifest missing"] = (diff1,'in '+categoryname +'-'+ examplename)
            if  diff2:
                print categoryname+examplename+'  vierify fail!\n',  diff2,' mainftes has more these files'
                result['examples code' + " --- manifest redundant"] = (diff2,'in '+categoryname +'-'+ examplename)
                return 1  ##notice!!! 
            return 0
        
    def Get_SDKXML_info(self):
        global fail_num

        self.classSDK.get_SDKS_examples()
        self.classXML.get_Mainfest_example_apps()

        self.classSDK.get_SDK_drivers()
        
        self.classXML.get_Mainfest_board()
        self.classXML.get_Mainfest_tools()
        self.classXML.get_Mainfest_compiler()
        self.classXML.get_Mainfest_drv()

        self.exampletupleSDK = self.classSDK.example_codeList[:]
        self.exampletupleXML = self.classXML.example_appsList[:]

        
        self.longSDK = len(self.exampletupleSDK)
        self.longXML = len(self.exampletupleXML)
        if self.longSDK == self.longXML:
            self.aa = self.longSDK
            print 'Process: ---load the SDK and XML info---'
        else:
            if self.longSDK < self.longXML:
                self.aa = self.longSDK   # self.aa is the short list
            else:
                self.aa = self.longXML

                
##__________________________________________________________________________
if __name__ == '__main__':
    # add SDK path configuration for SDK 2.0 KEx packages batch invoke
    global SDK_Path
    global SDK_Source
    global verification_case
    global result
    global fail_num
    fail_num = 0
    result = dict()
    
    SDK_Path = "C:\01_MY_job\A_TO_DO\Verify_Mainfest\TWR-K21F120M_PKG_sdk_2_0_windows_iar"
    arg_list = sys.argv[1:]
    if len(arg_list) > 0: SDK_Path = str(arg_list[0])
    
    Read_Path_and_Run()
    put_result()
    
    del SDK_Source
    del verification_case
    sys.exit()
#~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~       
