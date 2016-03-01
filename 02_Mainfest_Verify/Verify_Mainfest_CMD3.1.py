# -*- coding: cp936 -*-

from xml.etree import ElementTree as ET
from collections import Counter
import  xml.dom.minidom
from collections import Counter
import os
import re
import sys

#########################################################
#Compilers Project Definition
COMPILERS_PROJECT = {
        "armgcc"            :   'CMakeLists.txt',
        "atl"               :   '.launch',
        "iar"               :   '.eww',
        "mdk"               :   '.uvprojx',
        "kds"               :   '.launch'
}
#Suits Require
SUITS_REQUIRE = ["demo_apps","driver_examples","rtos_examples","usb_examples","mmcau"]

#KSDK App Folde Definiton
EXAMPLE_SDK_2_0 = "boards"
DEVICE_SDK_2_0 = "devices"
DEBUG = False

#========================================================
class SDKSource:
    """
    analysis the source SDK folder
    The example tuple format is : ( example_name, example_category, driver files,driver_path)
    """
    def __init__(self,sdk_path):
        
        self.SDK_PATH = sdk_path    
        self.board_path = self.SDK_PATH + '/'+ EXAMPLE_SDK_2_0
        self.device_path = self.SDK_PATH +'/'+ DEVICE_SDK_2_0 
        self.board_list = self.get_board_list()
        self.device_list = self.get_device_list()

    def get_board_list(self) :
        return self._get_folder_list(self.board_path)
      
    def get_device_list(self) :
        return self._get_folder_list(self.device_path)
    
    def get_SDKS_examples(self):
        examples_dict = {}
        for board in self.board_list:
            examples_dict[board] = self._scan_app(self.board_path, board)
        return examples_dict

    def get_SDKS_drivers(self):
        drivers_dict = {}
        for device in self.device_list:
            drivers_dict[device]= self._scan_driver(self.device_path,device)
        return drivers_dict
        
    def _get_folder_list(self,folder) :
        if os.path.exists(folder) == False:
            PATH = folder
            raise ValueError("Unknown KSDK structure: %s"%PATH)
        list = []
        for item in os.listdir(folder):
            if os.path.isdir(os.path.join(folder,item)) and (item in list) == False and item != "." and item != ".." :
                list.append(item) 
        if DEBUG:
            print "\nget folder list in: " + folder
            print list
        return list
    def _scan_driver(self,suit_path,device_name):
        """
        current just scan the 'drivers','utilities' type
        """
        source_list = []
        srcfil_list = []

        driver_type = ['drivers','utilities']
        suit_top = suit_path + '/'+ device_name
        suit_top.replace('\\','/')
        for dtype in driver_type:
            for dsrc in os.listdir(suit_top):
                if dsrc == dtype and os.path.isdir(suit_top +'/'+ dsrc):
                    #get driver source file path
                    srcfil_path = 'drivers'+'/'+ device_name +'/'+ dsrc
                    #get source files
                    for src in os.listdir(suit_top +'/'+ dsrc):
                        if re.match(r'^.*\.c$|^.*\.h$',src) and src != '.' and src != '..' :
                            srcfil_list.append(src)
                    new_putle = (dsrc,srcfil_list[:],srcfil_path)
                    source_list.append(new_putle)
        if DEBUG:
            print "get driver source files in: " + 'drivers'+'/'+ device_name
        return source_list

    def _scan_app(self, suit_path,board_name):
        
        REPEAT_flag  = False
        Last_AppParent  = ""
        AppParent       = ""
        scan_app_list = []
        source_list = []
        num = 0
        suit_apps = {"iar":[], "mdk":[], "atl":[], "kds": [], "armgcc": []}
        suit_top = suit_path + '/'+ board_name
        for parent, folders, filenames in os.walk(suit_top):
            #get compiler form parent path
            compiler = os.path.basename(parent)
            if compiler not in COMPILERS_PROJECT: 
                continue
            #compiler in compiler_project
            Last_AppParent = AppParent.replace('\\','/')
            AppParent = os.path.dirname(parent).replace('\\','/')
            #get the category and example name and the source files  in the appname/ folder
            if cmp(Last_AppParent, AppParent)!=0 and re.match(r'.*\.eww|.*\.cproject|.*\.uvprojx|.*\.bat.*',''.join(os.listdir(parent))):
                ##hello_world_qspi_alias, hello_world_qspi
                #get appname
##                print AppParent
                appname = os.path.basename(AppParent)
                #get category and get source path
                for exam_type in SUITS_REQUIRE:
                    pattern = re.compile(r'.*'+'/'+'('+exam_type+'.*'+')'+'/'+appname)
                    match = pattern.match(AppParent)
                    if match:
                        category = ''.join(match.groups())
                        sourch_path = EXAMPLE_SDK_2_0 + '/' + board_name + '/'+ category +  '/'+ appname
                    else:
                        continue
                # avoid the repeat same folder
                for i in range(len(scan_app_list)):
                    if scan_app_list[i][1] == appname and scan_app_list[i][2] == category:
                        REPEAT_flag = True
                        continue 
                if REPEAT_flag:
                    REPEAT_flag = False
                    continue
                #get source files
                for exam_src in os.listdir(AppParent):
                    if re.match(r'^.*\.c$|^.*\.h$',exam_src):
                        source_list.append(exam_src)
                new_putle = (appname,category,source_list,sourch_path)

                num += 1
                scan_app_list.append(new_putle)
                del new_putle
                source_list = []
        if DEBUG :
            print "==",num
        return scan_app_list
############################################################################
#===========================================================================
class ManifestInfo: 
    """
        The example tuple format is : ( example_name, example_category, driver files,link file)
        The driver format is : dict = {device name: (drivename, drivetype,sourcePaths[:], includePaths[:], \
                                                            sourceFiles[:], includeFiles[:])}
    """
    def __init__(self,SDK_path):
        for item in os.listdir(SDK_path):
            if re.findall(r'.*_manifest.xml',item):
                xml_file = SDK_path +'/'+ item
                break
        if os.path.exists(xml_file):
            tree = ET.parse(xml_file)
            self.root = tree.getroot()
        else:
            raise  ValueError("Can't find the manifest file in : %s"%xml_file)

        self.board_list = self.get_board_list()
        self.device_list = self.get_device_list()
        tool_list = self.get_tool_list()
        compiler = self.get_compiler_list()

    def get_board_list(self):
        boaList = []
        for boardsPresent in self.root.findall('boards'):
            for child in boardsPresent.findall('board'):
                brdName = child.get('name')
                boaList.append(brdName)
        if DEBUG:
            print boaList
        return boaList

    def get_device_list(self):
        devList = []
        for devicesPresent in self.root.findall('devices'):
            for child in devicesPresent.findall('device'):
                devName = child.get('name')
                if not (devName in devList):
                    devList.append(devName)
        if DEBUG:
            print devList
        return devList
    def get_tool_list(self):
        tooList = []
        for toolsPresent in self.root.findall('tools'):
            for child in toolsPresent.findall('tool'):
                toolId = child.get('id')
                tooList.append(toolId)
        if DEBUG:
            print tooList
        return tooList
    
    def get_compiler_list(self):
        cpiList = []
        for compilersPresent in self.root.findall('compilers'):
            for child in compilersPresent.findall('compiler'):
                compilerName = child.get('name')     
                cpiList.append(compilerName)
        if DEBUG:
            print cpiList
        return cpiList

    def get_driver_components(self):
        com_drvdict = {}    
        for device in self.device_list:
            com_drvdict[device] = self._scan_components('driver',device)
        return com_drvdict

    def get_utilities_components(self):
        com_utidict = {}   
        for device in self.device_list:
            com_utidict[device] = self._scan_components('utilities',device) 
        return com_utidict
    def get_others_components(self):
        com_othersdict = {}   
        for device in self.device_list:
            com_othersdict[device] = self._scan_components('others',device) 
        return com_othersdict
    def get_all_components(self):
        com_alldict = {}   
        for device in self.device_list:
            com_alldict[device] = self._scan_components('all',device) 
        return com_alldict
    def get_board_examples(self):  
        boa_examdict = {}
        for board in self.board_list:
            if not re.match(r'usb.*',board):
                boa_examdict[board] = self._scan_examples(board)
        return boa_examdict

    def _scan_components(self,driver_type,device_name):
    
        drvList = []
        drvName = ''
        includePaths = []
        sourcePaths = []
        includeFiles = []
        sourceFiles = []
        if driver_type == 'all' :
            driver_types = ['driver','utilities','other','middleware',\
                              'os','CMSIS','startup','project_template','debugger','linker']
        elif driver_type == 'other' :
            driver_types = ['other','middleware',\
                              'os','CMSIS','startup','project_template','debugger','linker']
        else:
            driver_types = [driver_type]
            
        for i in range(len(driver_types)):  
            for driversPresent in self.root.findall('components'):
                  for componentType in driversPresent.findall('component'):
                        if componentType.get('type') == driver_types[i] and componentType.get('device') == device_name:
                                
                            drvName = componentType.get('name')

                            for sources in componentType.findall('source'):
                                for files in sources.findall('files'):
                                    if sources.get('type') == 'src':
                                        sourcePaths.append(str(sources.get('path')))
                                        sourceFiles.append(str(files.get('mask')))
                                    elif sources.get('type') == 'c_include':
                                        includePaths.append(str(sources.get('path')))
                                        includeFiles.append(str(files.get('mask')))

                            #New tuple for each driver containing name and paths
                            newDrvTuple = (drvName,driver_types[i],sourcePaths[:], includePaths[:], \
                                                        sourceFiles[:], includeFiles[:])
                            #Append drvList with new tuple for
                            drvList.append(newDrvTuple)
                            sourcePaths = []
                            includePaths = []
                            sourceFiles = []
                            includeFiles = []
                            del newDrvTuple

        if DEBUG:
            print "Get the drivers of : " + driver_type +'\n'
        return drvList

    def _scan_examples(self,board_name):                     
        """
        """
        examList = []
        boardname = ''
        examples_category = ''
        sourcePaths = []
        includePaths = []
        linkerPaths = []
        includeFiles = []
        sourceFiles = []
        linkerFiles = []
    
        for boardsPresent in self.root.findall('boards'):
            for boardType in boardsPresent.findall('board'):
                if boardType.get('name') == board_name:
                    for examplesPresent in boardType.findall('examples'):
                        for exampleType in examplesPresent.findall('example'):
                            pattern = re.compile(r'')
                            match = pattern.match(exampleType.get('category'))
                            if match:
                                #get examples category
                                examples_category = exampleType.get('category')
                                #print examples_category
                                #get examples name and source files
                                exampleName = exampleType.get('name')
                                for sources in exampleType.findall('source'):
                                    for files in sources.findall('files'):
                                        if sources.get('type') == 'src':
##                                            sourcePaths.append(str(sources.get('path')))
                                            sourceFiles.append(str(files.get('mask')))
                                        elif sources.get('type') == 'c_include':
##                                            includePaths.append(str(sources.get('path')))
                                            includeFiles.append(str(files.get('mask')))
                                        elif sources.get('type') == 'linker':
##                                            linkerPaths.append(str(sources.get('path')))
                                            linkerFiles.append(str(files.get('mask')))
                                #New tuple for each driver containing name and paths
                                newdemoTuple = (exampleName,examples_category,\
                                                sourceFiles[:]+includeFiles[:],linkerFiles[:])

                                #Append drvList with new tuple for
                                examList.append(newdemoTuple)
                                del sourceFiles[:]
                                del sourcePaths[:]
                                del includeFiles[:]
                                del includePaths[:]
                                del linkerFiles[:]
                                del linkerPaths[:]
                                del newdemoTuple
                                
        if DEBUG:
            examples_num = len(examList)
            print 'The examples_num is '+str(examples_num)
            print "get the exampels of : " + board_name +'\n'
            print 'get the platform Mainfest examples   success!'
        return examList


###########################################################################
#=========================================================================
class Verification:
    """
      1.verify whether the board and device name is same between SDK and mainfest
      2.verify whether the SDK source and mainfest source are same about drivers file
      3.verify whether the SDK examples and mainfest examples are same about examples name and examoles source files
      3.verify whether the comontens and examples of manifest whether is repeat 
    """
    def __init__(self,scan_path):
        if os.path.exists(scan_path):
            self.SDK_PATH = scan_path
        else:
            self.SDK_PATH = scan_path
            raise ValueError("Unknown KSDK structure: %s"%self.SDK_PATH)
        self.SDK_Source =  SDKSource(self.SDK_PATH)
        self.Manifest_Info = ManifestInfo(self.SDK_PATH)
        self.result = {}
        self.fail_num = 0
        
        verify1 = self.Verify_boardname()
        verify2 = self.Verify_devicename()
        
        self.boarepeat_flag = self.Verify_repeatboard()
        self.devrepeat_flag = self.Verify_repeatdevice()
        
        verify5 = self.Verify_driver_components()
        verify6 = self.Verify_repeatcomponts()
        verify7 = self.Verify_examples()
        
    def Verify_boardname(self):
        return self._simple_compare(self.SDK_Source.board_list, self.Manifest_Info.board_list,'Board name')

    def Verify_devicename(self):
        return self._simple_compare(self.SDK_Source.device_list, self.Manifest_Info.device_list,'Device name')
    
    def Verify_repeatboard(self):
        """
            verify the mainfest whether repeat the board and modify the boatd_list
            eg: if board_list = ['frdmk82f','frdmk82f']. script will print log and set the board_list = ['frdmk82f']
        """
        reboard = {}
        for item in self.Manifest_Info.board_list:
            if self.Manifest_Info.board_list.count(item) > 1 and not(item in reboard) :
                self.fail_num += 1
                self.result[str(self.fail_num)+' Board duplication '+ " --- manifest repeat the "] = item
                reboard[item] = self.Manifest_Info.board_list.count(item)
        if len(reboard)>0:
            for key in reboard:
                for i in range(1,reboard[key]):
                    self.Manifest_Info.board_list.remove(item)   
            return 0
        else:
            self.result['Board duplication '+ " --- manifest verification  "] = 'OK'
            return 1
        
    def Verify_repeatdevice(self):
        """
            the functions same as the Verify_repeatboard(self)
        """
        redevice = {}
        for item in self.Manifest_Info.device_list:
            if self.Manifest_Info.device_list.count(item) > 1 and not(item in redevice) :
                print 'Result: Verify repeat device, the device '+ item +' has been repeated ~~ '
                self.fail_num += 1
                self.result[str(self.fail_num)+' Device duplication '+ " --- manifest repeat the "] = item
                self.fail_num += 1
                redevice[item] = self.Manifest_Info.device_list.count(item)
        if len(redevice)>0:
            for key in redevice:
                for i in range(1,redevice[key]):
                    self.Manifest_Info.device_list.remove(item) 
            return 0
        else:
            self.result['Device duplication '+ " --- manifest verification  "] = ['OK']
            return 1
    def Verify_driver_components(self):
        drilistXML = []
        drilistSDK = []
        self.Verify_repeatdevice()  # verify the device whether repeat firstly
        
        dridictSDK = self.SDK_Source.get_SDKS_drivers()
        dridictXML = self.Manifest_Info.get_driver_components()
        for device in self.SDK_Source.device_list:
            drilistSDK = dridictSDK[device][0][1]
            for i in range(len(dridictXML[device])):
                drilistXML += dridictXML[device][i][4]+ dridictXML[device][i][5]
            self._simple_compare(drilistSDK,drilistXML,device+' driver components')
            del drilistSDK[:]
            del drilistXML[:]
        
    def Verify_repeatcomponts(self):

        componttype_List = ['driver','utilities','other','middleware',\
                              'os','CMSIS','startup','project_template','debugger','linker']
        drvnameList = []
        drvflieList = []
        drvfliedict = dict()
        repeatname_num = 0
        compontdict = self.Manifest_Info.get_all_components()
        for device in self.Manifest_Info.device_list:
            compontuple = compontdict[device]
            for k in range(len(componttype_List)):
                for i in range(len(compontuple)):
                    if compontuple[i][1]== componttype_List[k] :
                        drvnameList.append(compontuple[i][0])
                        
                        drvflieList = compontuple[i][4]+compontuple[i][5]
                        drvfliedict[compontuple[i][0]] = drvflieList

                name_dupcheck = Counter(drvnameList)
                for drvname in name_dupcheck:
                    if name_dupcheck[drvname] > 1:
                        print 'The driver name '+ drvname + ' is repeated'
                        repeatname_num += 1
                        self.fail_num += 1
                        self.result[str(self.fail_num)+' '+ device+' Componens duplication' + " --- manifest repeat"] = drvname +' of '+ componttype_List[k]
                        
                for filname in drvfliedict:
                    if filname == 'CMSIS':
                        continue
                    file_dupcheck = Counter(drvfliedict[filname])
                    for j in file_dupcheck:       
                        if file_dupcheck[j] > 1 :
                            print  'The drivers file '+ j + ' is repeated'
                            self.fail_num += 1
                            repeatname_num += 1
                            self.result[str(self.fail_num)+' '+ device+' Componens duplication' + " --- manifest repeat"] = j +' in '+ filname         
                drvnameList = []
                drvflieList = []
                drvfliedict = {}
        if repeatname_num == 0:
            result['drivers duplication' + " --- manifest verification"] = ["OK"]
            print 'Result: Drivers duplication verify done. Success! '
        else:
            print 'Result: Drivers duplication verify done. Repeated driver has '+str(repeatname_num)  
            
    def Verify_examples(self):
        """
            1.compare the .c and .h file under the example folder
            2.verify whether the example of the xml is repeat
            The compare format is : ( example_name, example_category, driver files)
        """
        re_num = 0
        SDK_examdict = self.SDK_Source.get_SDKS_examples()
        XML_examdict = self.Manifest_Info.get_board_examples()
        fail_count = self.fail_num
        for boaname in self.SDK_Source.board_list:
            example_SDK = SDK_examdict[boaname]
            example_XML = XML_examdict[boaname]
            for SDKitem in example_SDK:
                for XMLitem in example_XML:
                    if SDKitem[0] == XMLitem[0] and SDKitem[1] == XMLitem[1]:
                        self._mul_compare(SDKitem[2],XMLitem[2],SDKitem[1],SDKitem[0])
                        re_num += 1
                #verify whether the example of the xml is repeat       
                if self.boarepeat_flag and re_num >1 :
                    if DEBUG:
                        print SDKitem[1]+ ' ' +SDKitem[0]+' repeat in manifest:'+str(re_num)+' times\n'
                    self.fail_num +=1
                    self.result[str(self.fail_num)+ ' examples duplication  --- manifest repeat the'] = SDKitem[1]+ ' ' +SDKitem[0] +' '+ str(re_num)+' times'
                re_num = 0
            del example_SDK
            del example_XML
        if fail_count == self.fail_num :
            self.result[ 'examples duplication' + " --- manifest verification"] = ["OK"]
            self.result[ 'examples code' + " --- manifest verification"] = ["OK"]
            print "Result: Examples code and duplication verify done. Success!"
          
    def _simple_compare(self,listSDK,listXML,compare_type):

        diff1 = list(set(listSDK).difference(listXML))
        diff2 = list(set(listXML).difference(listSDK))

        if not diff1 and not diff2:
            print 'Result: '+compare_type+' verify done. Success!'
            self.result[compare_type + " --- manifest verification"] = ["OK"]
            return 1
        else:
            if  diff1 :
                    print diff1,' mainftes has less these files\n'
                    self.fail_num += 1
                    self.result[str(self.fail_num)+' '+compare_type + " --- manifest missing"] = diff1
                    
            if  diff2 and not re.match(r'usb.*',''.join(diff2)) :
                    print diff2,' mainftes has more these files\n'
                    self.fail_num += 1
                    self.result[str(self.fail_num)+' '+compare_type + " --- manifest redundant "] = diff2
            return 0
    def _mul_compare(self,listSDK,listXML,categoryname,examplename):

        diff1 = list(set(listSDK).difference(listXML))
        diff2 = list(set(listXML).difference(listSDK))
        
        if not diff1 and not diff2:
            return 1
        else:
            if  diff1:
                print categoryname+ ' ' +examplename+'  verify fail!\n', diff1 , ' manifest has less these files'
                self.fail_num += 1
                self.result[str(self.fail_num)+ " examples code --- manifest missing"] = str(diff1) +' in '+categoryname +'/'+ examplename
            if  diff2:
                print categoryname+ ' ' +examplename+'  verify fail!\n',  diff2,' mainfest has more these files'
                self.fail_num += 1
                self.result[str(self.fail_num)+ " examples code --- manifest redundant"] = str(diff2) +' in ' +categoryname +'/'+ examplename

            return 0
#########################################################################
#========================================================================
def put_result(result_path,result,fialnum):

    head = '--- '+result_path+' Verify:\n'
    if fialnum == 0:
        print 'Verify Finish! Result = PASS \n'
        result_file = open(result_path+'/Verify_Manifest_PASS.yml','a')
        result_file.close()
    else:
        print 'Verify Finish! Result = FAIL \n'
        result_file = open(result_path+'/Verify_Manifest_Fialed.yml','a')
        result_file.write( head )
        for i in result:
            result_file.write(i + ': ' + str(result[i]) + '\n')
        result_file.write('--- Verify Finish! Result = FAIL '+ str(fialnum) +' times\n' )
        result_file.close()
#========================================================================
if __name__ == '__main__':
    # add SDK path configuration for SDK 2.0 KEx packages batch invoke
    result = dict()
    
    SDK_Path = "C:\\01_MY_job\\A_TO_DO\\TWR-K60D100M_PKG_sdk_2_0_windows_all"
    arg_list = sys.argv[1:]
    if len(arg_list) > 0: SDK_Path = str(arg_list[0])

    print "=== VERIFY THE MANIFEST: "+ SDK_Path + " ==="
    Verification = Verification(SDK_Path)
    put_result(SDK_Path,Verification.result,Verification.fail_num)
    
    del Verification
    sys.exit()
