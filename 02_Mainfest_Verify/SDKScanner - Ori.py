import os
import re
import yaml

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
SUITS_REQUIRE = {
		"demo_apps"			: 'demo', 
		"driver_examples"	: 'example', 
		"rtos_examples"		: 'ksdk_rtos', 
		"usb_examples"		: 'usb', 
		"mmcau"				: 'mmcau'
}
#########################################################
#CmakeLists.txt   keyword
CMKAE_KEYWORD_1 = re.compile('ADD_EXECUTABLE.*\.elf',re.I)
CMKAE_KEYWORD_2 = re.compile('SET_TARGET_PROPERTIES.*\.elf',re.I)

#########################################################
#KSDK App Folde Definiton
SDK_1_3 = "/examples/"
SDK_2_0 = "/boards/"

class CaseScan:


	def __init__(self, scan_path):
		if os.path.exists(scan_path+SDK_1_3):
			self.path_top = scan_path+SDK_1_3
		elif os.path.exists(scan_path+SDK_2_0):
			self.path_top = scan_path+SDK_2_0  
		else:
			self.path_top = scan_path+SDK_2_0 
			raise ValueError("Unknown KSDK structure: %s"%self.path_top)

	def get_platforms(self, spaltform=None):
		if spaltform is not None:
			return spaltform
		else:
			return [pf for pf in os.listdir(self.path_top) if(pf !="src")and(pf[0]!=".") ]

	def scan_case(self, casefilename="case_file.yml", mode = "w",spaltform=None):
		'''
		mode      - open yaml file mode, default: "w",   type: str
		spaltform - specify platform,    default: None,  type: list
		'''
		print ("---   Scan Start   ---")

		self.all_platform_list = self.get_platforms(spaltform)
		scan_dict = {}

		#pf: platform,
		for pf in self.all_platform_list:
			print pf
			#platform top path
			pf_top = ''.join((self.path_top, pf))
			#list all suits pf current platform
			pf_suits = filter(lambda suit_name: SUITS_REQUIRE.has_key(suit_name), os.listdir(pf_top))
			#get all suits top
			pf_suits_top = (''.join([pf_top,'/', pf_suit_name]) for pf_suit_name in pf_suits)
			#get each suit apps
			pf_suits_apps = [self._scan_app(suit_top) for suit_top in pf_suits_top]
			#rename suit name
			pf_suits_new = map(lambda suit_name: SUITS_REQUIRE[suit_name], pf_suits)
			#Map suits and apps
			pf_suits_dict = dict(zip(pf_suits_new, pf_suits_apps))

			#put mmcau to example group
			if pf_suits_dict.has_key("mmcau"):
				for c in COMPILERS_PROJECT:
					if pf_suits_dict["mmcau"][c]:
						pf_suits_dict["example"][c].append("mmcau")
				del pf_suits_dict["mmcau"]
			#update scan dict
			scan_dict[pf]= pf_suits_dict

		print ("---  Scan Finished!   ---")
		#write to file
		with open(casefilename, mode) as f:
			yaml.dump(scan_dict, f, default_flow_style=False)
		print ("---  Case File Generate Done!  ---")
		

	def _scan_app(self, suit_top):
		app_project 	= {}
		First 			= True
		Last_AppParent 	= ""
		AppParent  		= ""

		suit_apps = {"iar":[], "mdk":[], "atl":[], "kds": [], "armgcc": []}

		for parent, folders, filenames in os.walk(suit_top):
			#get compiler form parent path
			compiler = os.path.basename(parent)
			if compiler not in COMPILERS_PROJECT: 
				continue
			#compiler in compiler_project
			Last_AppParent = AppParent
			AppParent = os.path.dirname(parent)

			#remove compiler info, get App Parent path
			if (cmp(Last_AppParent, AppParent)!=0 and len(app_project) != 0) and (First is False):
				appname = None
				#get appname  "eww"
				if "iar" in app_project or "mdk" in app_project:
					try:
						appname = app_project["iar"].replace(COMPILERS_PROJECT["iar"],"")
					except KeyError:
						appname = app_project["mdk"].replace(COMPILERS_PROJECT["mdk"],"")
				#project name "dac_basic_frdmk22f debug cmsisdap.launch"
				elif "atl" in app_project or "kds" in app_project:
					appname = app_project["atl"].split(" ")[0]
					appname = "_".join(appname.split("_")[:-1])
				#armgcc -- CMAKE file
				elif "armgcc" in app_project:
					#make file path:
					makefile_path = os.path.join(Last_AppParent,"armgcc", COMPILERS_PROJECT["armgcc"])
					try:
						makefile = open(makefile_path)
						content = makefile.readlines()
						makefile.close()
						#find key word
						for line in content:
							if re.search(CMKAE_KEYWORD_1, line) is not None:
								appname = line.split('(')[1].replace(' ', '').split('.elf')[0]
							elif re.search(CMKAE_KEYWORD_2, line) is not None:
								appname = line.split('OUTPUT_NAME')[1].replace(' ','').replace('\"', '').split('.elf')[0]
					except IOError:
						pass
					if appname is None: raise ValueError("Can't find app name in %s"%makefile_path)

				#update suit_apps
				try:
					for c in app_project.keys(): suit_apps[c].append(appname)
					#clear app_project
					app_project.clear()
				except KeyError:
					raise KeyError("Scan Error: Unknown Compiler Project!! %s\n\n"%app_project)


			First = False
			for project_name in filenames:
				if project_name.endswith(COMPILERS_PROJECT[compiler]):			
					#app_project: 
					#			-iar: appname.eww
					#			-mdk: appname.uvprojx
					#			-atl: appname_xxx.lunch
					#			...
					app_project[compiler]=project_name
					break
			
		##########################################################
		if len(app_project) != 0:
			#get appname
			if "iar" in app_project or "mdk" in app_project:
				try:
					appname = app_project["iar"].replace(COMPILERS_PROJECT["iar"],"")
				except KeyError:
					appname = app_project["mdk"].replace(COMPILERS_PROJECT["mdk"],"")
			#project name
			elif "atl" in app_project or "kds" in app_project:
				appname = app_project["atl"].split(" ")[0]
				appname = "_".join(appname.split("_")[:-1])
			#armgcc -- CMAKE file
			elif "armgcc" in app_project:
				#make file path:
				makefile_path = os.path.join(AppParent,"armgcc", COMPILERS_PROJECT["armgcc"])
				try:
					makefile = open(makefile_path)
					content = makefile.readlines()
					makefile.close()
					#find key word
					for line in content:
						if re.search(CMKAE_KEYWORD_1, line) is not None:
							appname = line.split('(')[1].replace(' ', '').split('.elf')[0]
						elif re.search(CMKAE_KEYWORD_2, line) is not None:
							appname = line.split('OUTPUT_NAME')[1].replace(' ','').replace('\"', '').split('.elf')[0]
				except IOError:
					pass

			try:
				for c in app_project.keys(): suit_apps[c].append(appname)
			except KeyError:
				raise KeyError("Scan Error: Unknown Compiler Project!! %s\n\n"%app_project)
		return suit_apps




	def scan_readme(self):
		'''
		scan readme!
		'''
		print ("---   Scan Start   ---")

		self.all_platform_list = self.get_platforms()
		scan_dict = {}

		#pf: platform,
		for pf in self.all_platform_list:
			print pf
			#platform top path
			pf_top = ''.join((self.path_top, pf))
			#list all suits pf current platform
			pf_suits = filter(lambda suit_name: SUITS_REQUIRE.has_key(suit_name), os.listdir(pf_top))
			#get all suits top
			pf_suits_top = (''.join([pf_top,'/', pf_suit_name]) for pf_suit_name in pf_suits)
			#get each suit apps
			pf_suits_apps = [self._scan_readme(suit_top) for suit_top in pf_suits_top]
			#rename suit name
			pf_suits_new = map(lambda suit_name: SUITS_REQUIRE[suit_name], pf_suits)
			#Map suits and apps
			pf_suits_dict = dict(zip(pf_suits_new, pf_suits_apps))

			scan_dict[pf]= pf_suits_dict

		with open("readme_info.yml", "a+") as f:
			yaml.dump(scan_dict, f, default_flow_style=False)

	def _scan_readme(self, suit_top):
		app_project 	= {}
		First 			= True
		Last_AppParent 	= ""
		AppParent  		= ""


		suit_apps = {"no_readme_case":[], "uncomplete_readme_case":[]}

		for parent, folders, filenames in os.walk(suit_top):
			#get compiler form parent path
			compiler = os.path.basename(parent)
			if compiler not in COMPILERS_PROJECT: 
				continue
			#compiler in compiler_project
			Last_AppParent = AppParent
			AppParent = os.path.dirname(parent)

			if (cmp(Last_AppParent, AppParent)!=0 and len(app_project) != 0) and (First is False):
				appname = find_appname(Last_AppParent, app_project, First)
				judge_result=judge(Last_AppParent, appname)
				if judge_result == "NOREADME":
					suit_apps["no_readme_case"].append(appname)
				elif judge_result == "EMPTY":
					suit_apps["uncomplete_readme_case"].append(appname)
				app_project.clear()

			First = False
			for project_name in filenames:
				if project_name.endswith(COMPILERS_PROJECT[compiler]):			
					app_project[compiler]=project_name
					break

		if len(app_project)!=0:
			appname = find_appname(AppParent, app_project, First)
			judge_result=judge(AppParent, appname)
			if judge_result == "NOREADME":
				suit_apps["no_readme_case"].append(appname)
			elif judge_result == "EMPTY":
				suit_apps["empty_readme_case"].append(appname)

		return suit_apps


def find_appname(app_path, app_project, First):
	#remove compiler info, get App Parent path
	appname = None
	#get appname  "eww"
	if "iar" in app_project or "mdk" in app_project:
		try:
			appname = app_project["iar"].replace(COMPILERS_PROJECT["iar"],"")
		except KeyError:
			appname = app_project["mdk"].replace(COMPILERS_PROJECT["mdk"],"")
	#project name "dac_basic_frdmk22f debug cmsisdap.launch"
	elif "atl" in app_project or "kds" in app_project:
		appname = app_project["atl"].split(" ")[0]
		appname = "_".join(appname.split("_")[:-1])
	#armgcc -- CMAKE file
	elif "armgcc" in app_project:
		#make file path:
		makefile_path = os.path.join(app_path,"armgcc", COMPILERS_PROJECT["armgcc"])
		try:
			makefile = open(makefile_path)
			content = makefile.readlines()
			makefile.close()
			#find key word
			for line in content:
				if re.search(CMKAE_KEYWORD_1, line) is not None:
					appname = line.split('(')[1].replace(' ', '').split('.elf')[0]
				elif re.search(CMKAE_KEYWORD_2, line) is not None:
					appname = line.split('OUTPUT_NAME')[1].replace(' ','').replace('\"', '').split('.elf')[0]
		except IOError:
			pass
		if appname is None: raise ValueError("Can't find app name in %s"%makefile_path)

	return appname

		##############################################################

def judge(p, appname):
	if "usb_examples" in p:
	 	if not os.path.exists(os.path.join(p,"readme.pdf")):
			print "No readme: %s"%appname
			return "NOREADME"
	else:
		readme_path = os.path.join(p,"readme.txt")
		if not os.path.exists(readme_path):
			suit_apps["no_readme_case"].append(appname)
			print "No Readme: %s"%appname
			return "NOREADME"
		with open(readme_path, "r") as f:
			if len(f.readlines())<=40:
				print "Uncomplete Readme: %s"%appname
				return "EMPTY"
	return None


import zipfile
import time
import sys, os

__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

if __name__ == '__main__':
	path=sys.argv[1]

	#creat and clear readme_yml
	with open("readme_info.yml","w+")as f:
		pass

	if os.path.exists(path + "/boards/"):
		sdk = path
		cs=CaseScan(sdk)
		cs.scan_readme()
	else:
		for p in os.listdir(path):
			if p.endswith(".zip"): continue
			sdk=os.path.join(path, p)
			cs=CaseScan(sdk)
			cs.scan_readme()
