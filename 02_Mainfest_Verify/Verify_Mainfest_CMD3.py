
from xml.etree import ElementTree as ET
import  xml.dom.minidom
from collections import Counter
import os
import re
import sys

#########################################################
#Compilers Project Definition
#Contain app name
COMPILERS_PROJECT = {
		"armgcc"			:	'CMakeLists.txt',
		"atl"				: 	'.launch',
		"iar"				: 	'.eww',
		"mdk"				: 	'.uvprojx',
		"kds"				: 	'.launch'
}
#########################################################
#Suits Require
SUITS_REQUIRE = ["demo_apps","driver_examples","rtos_examples","usb_examples","mmcau"]
#########################################################
#KSDK App Folde Definiton
EXAMPLE_SDK_2_0 = "boards"
DEVICE_SDK_2_0 = "devices"
DEBUG = True

#========================================================
class SDKSource:
	"""
	analysis the source SDK folder
	"""
	def __init__(self,scan_path):
		if os.path.exists(scan_path):
			self.SDK_PATH = scan_path
		else:
			self.SDK_PATH = scan_path
			raise ValueError("Unknown KSDK structure: %s"%self.SDK_PATH)
			
		self.board_path = self.SDK_PATH + '/'+ EXAMPLE_SDK_2_0
		self.device_path = self.SDK_PATH +'/'+ DEVICE_SDK_2_0 
		self.board_list = self.get_board_list()
		self.device_list = self.get_device_list()
		#dd = self.get_SDKS_examples()
		#ff = self.get_SDKS_drivers()
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
		print folder
		for item in os.listdir(folder):
			if os.path.isdir(os.path.join(folder,item)) and (item in list) == False and item != "." and item != ".." :
				list.append(item) 
		if DEBUG:
			print "\nget folder list in: " + folder
			print list
		return list
   	def _scan_driver(self,suit_path,device_name):
   		"""
   		curent just scan the 'drivers','utilities' type
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
   			print "\nget driver source files in: " + 'drivers'+'/'+ device_name
   			print source_list
   		return source_list

	def _scan_app(self, suit_path,board_name):
		
		REPEAT_flag  = False
		Last_AppParent 	= ""
		AppParent  		= ""
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
			if cmp(Last_AppParent, AppParent)!=0 :

				#get appname
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
		print "======================\n",num
		print scan_app_list	
		return scan_app_list
############################################################################
#===========================================================================
class ManifestInfo: 
	"""
	"""
	def __init__(self,SDK_path):
		xml_file = SDK_path + '/ksdk_manifest.xml'
		if os.path.exists(xml_file):
			tree = ET.parse(xml_file)
			self.root = tree.getroot()
		else:
			raise  ValueError("Can't find the ksdk_manifest.xml in : %s"%xml_file)

		self.board_list = self.get_board_list()
		self.device_list = self.get_device_list()
    
		tool_list = self.get_tool_list()
		compiler = self.get_compiler_list()
		dd = self.get_board_examples()
		ff = self.get_driver_components()
		uu = self.get_utilities_components()

	def get_board_list(self):
		boaList = []
		for boardsPresent in self.root.findall('boards'):
			for child in boardsPresent.findall('board'):
				brdName = child.get('name')
				if not (brdName in boaList):
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
	def get_other_components(self):
		pass

	def get_board_examples(self):
		pass
	def _scan_components(self,driver_type,device_name):
    
		driver_type_List=['driver','utilities','other','middleware',\
							  'os','CMSIS','startup','project_template','debugger','linker']
		drvList = []
		drvName = ''
		includePaths = []
		sourcePaths = []
		includeFiles = []
		sourceFiles = []
		for driversPresent in self.root.findall('components'):
			  for componentType in driversPresent.findall('component'):
					if componentType.get('type') == driver_type:
							if componentType.get('device') == device_name:
								drvName = componentType.get('name')
								# HACK: for K80 lmem_cache to lmem
								# if drvName == 'lmem_cache':
								#     drvName = 'lmem'
								for sources in componentType.findall('source'):
									for files in sources.findall('files'):
										#print 'File: ' + files.get('mask')
										if '_dma_' in files.get('mask'):
										  #print 'DMA'
											if self.dmaCount > 0:
												if sources.get('type') == 'src':
													sourcePaths.append(str(sources.get('path')))
													sourceFiles.append(str(files.get('mask')))
												elif sources.get('type') == 'c_include':
													includePaths.append(str(sources.get('path')))
													includeFiles.append(str(files.get('mask')))
										else:
											if sources.get('type') == 'src':
												sourcePaths.append(str(sources.get('path')))
												sourceFiles.append(str(files.get('mask')))
											elif sources.get('type') == 'c_include':
												includePaths.append(str(sources.get('path')))
												includeFiles.append(str(files.get('mask')))

								#New tuple for each driver containing name and paths
								newDrvTuple = (drvName, sourcePaths[:], includePaths[:], \
															sourceFiles[:], includeFiles[:])
								#Append drvList with new tuple for
								drvList.append(newDrvTuple)
								sourcePaths = []
								includePaths = []
								sourceFiles = []
								includeFiles = []
								del newDrvTuple

		if DEBUG:
			print "\nget the drivers of : " + driver_type +'\n'
			print drvList
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
		index = 0
		for boardsPresent in self.root .findall('boards'):
			for boardType in boardsPresent.findall('board'):
				if board_name in boardType.get('device'):  # pattern board name such as device = 'MK82F25615 frdmk82f'
					boardname = boardType.get('name')
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
											sourcePaths.append(str(sources.get('path')))
											sourceFiles.append(str(files.get('mask')))
										elif sources.get('type') == 'c_include':
											includePaths.append(str(sources.get('path')))
											includeFiles.append(str(files.get('mask')))
										elif sources.get('type') == 'linker':
											linkerPaths.append(str(sources.get('path')))
											linkerFiles.append(str(files.get('mask')))
								#New tuple for each driver containing name and paths
								newdemoTuple = (exampleName,examples_category,\
												sourceFiles[:],sourcePaths[:],\
												includeFiles[:],includePaths[:],\
												linkerFiles[:],linkerPaths[:])

								#Append drvList with new tuple for
								examList.append(newdemoTuple)
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
		if DEBUG:
			print "\nget the exampels of : " + board_name +'\n'
			print examList
		return examList


###########################################################################
#=========================================================================
class Verification;
	"""
		1.verify whether the board and device name is same between SDK and mainfest
		1.verify whether the SDK source and mainfest source are same on drivers file
		2.verify whether the SDK examples and mainfest examples are same on examples name and examoles source files
		3.verify 
	"""


##########################################################################
if __name__ == '__main__':
    # add SDK path configuration for SDK 2.0 KEx packages batch invoke
    global SDK_Path
    global SDK_Source
    global verification_case
    global result
    global fail_num
    fail_num = 0
    result = dict()
    
    SDK_Path = "C:/01_MY_job/A_TO_DO/Verify_Mainfest/TWR-K80F150M_PKG_sdk_2_0_windows_iar"
    arg_list = sys.argv[1:]
    if len(arg_list) > 0: SDK_Path = str(arg_list[0])
    
    SDK_Source =  SDKSource(SDK_Path)
    Manifest_Info = ManifestInfo(SDK_Path)
	#SDK_Source.get_SDKS_examples()
    
    del SDK_Source
    sys.exit()
