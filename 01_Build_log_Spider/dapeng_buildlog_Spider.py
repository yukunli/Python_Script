# -*- coding: cp936 -*-

import re 
import urllib
import string
import datetime
import time
import sys

DEBUG = False
##############################################
#=============================================
class get_fail_caseinfo():

    def __init__(self,requst_path,compiler):
        self.requstPath = requst_path
        self.compiler_name = compiler
    
    def check_build_html(self,line):
        pattern = re.compile(r"<tr><td><img src='/dapeng/static/pics/file.gif'> <a href='(.*)' onmouseout")
        fail_line = pattern.match(line)
        if fail_line:
            build_file_path =  "http://10.192.225.198" + str(fail_line.groups(0)[0])
            build_log = self.getHtml(build_file_path)
            if build_log:
                return build_log
            else:
                raise ValueError("can't find the build log in: %s"%line)
        else:
            return None
            
               
    def check_fail_html(self,line):
        faild_case_tuple = ()
        pattern = re.compile(r"(<tr.*<td>"+self.compiler_name+"</td>.*<td><img src='/dapeng/static/pics/not_ok_small.png'></td>.*Finished</td>)")
        fail_line = pattern.match(line)
        if fail_line :
            fail_info = str(fail_line.groups(0))
            case_name = self.get_fail_case_name(fail_info)
            fail_html = re.match(r".*<td><a href=.?'(.*).?' target.*",fail_info)
            build_log = None
            if fail_html:
                #print "++++++\n"
                build_path = "http://10.192.225.198" + str(fail_html.groups(0)[0])
                build_html = self.getHtml(build_path)
                self.write_build_html_txt(build_html)
                page_file = open('.\\build_html.txt','r')
                buthml_line = page_file.readlines()
                for line in buthml_line:
                    loginfo = self.check_build_html(line)
                    if loginfo:
                        build_log = loginfo
                        break                   
                        
            else:
                print'patern fail in check_fail_html of ' + fail_info
            faild_case_tuple =(self.compiler_name,case_name,build_log)
            del build_log
            return faild_case_tuple
        else:
            return None
    def get_fail_case_name(self,fail_info):
        pattern = re.compile(r"</a></td><td>(.*)</td><td>.*\d")
        patinfo = pattern.findall(fail_info)
        if patinfo:
            caseinfo = patinfo[0]
            newcaseinfo = caseinfo.replace('</td><td>','-')
            return newcaseinfo
        else:
            print "Can't find the fialed case info in " + fail_info
            return "No Failed Case Info"

        
    def getHtml(self,url):
        try:
            page = urllib.urlopen(url)
            html = page.read()
        except:
            html = None
            print "read url fail in:  " + url
        finally:
            page.close()
            return html
    def write_html_txt(self,html_page):
        html_file = open('.\\page_html.txt','w')
        html_file.write(html_page)
        html_file.close()
    
    def write_build_html_txt(self,html_page):

        html_file = open('.\\build_html.txt','w')
        html_file.write(html_page)
        html_file.close()
#####################################################
        
class compare():
    def __init__(self,dapeng_requst_path,compiler,compare_list = []):
        self.requstPath = dapeng_requst_path
        self.logList = []
        for pattern in compare_list:
            self.logList.append(re.compile(r".*"+ pattern +".*"))
        
        self.failcase = get_fail_caseinfo(dapeng_requst_path,compiler)
        self.compiler = compiler
    def compare_fail_log(self):
        global fails_num
        compiler_dict = {"iar":3,"uv4":4,"gcc_arm":5,"kds":8,"atl":10}
        print compiler_dict[self.compiler]
        main_html = self.failcase.getHtml(self.requstPath + "?showall=1&compilerid="+str(compiler_dict[self.compiler])+"&buildresult=2" )
        self.failcase.write_html_txt(main_html)
        page_file = open('.\\page_html.txt','r')
        line = page_file.readlines()
        page_file.close()
        for item in line:
            fail_build_info = self.failcase.check_fail_html(item)
            if fail_build_info:
                fails_num += 1
                self._match_pattern(fail_build_info)
                del fail_build_info
                if DEBUG :
                     print "^^^^^^^"
        del main_html
        print "compare build error finished!"
        
    def _match_pattern(self,fail_build_info):
        global Error1fail_num
        global Error2fail_num
        global OtherErrorfail_num
        global Erroelist
        global NO
        global compiler_name
        other_errorlist = []
        html_file = open('.\\'+NO+compiler_name+'_compare_result.txt','a')
        match = str(fail_build_info[2])
        pattern_flag = 0
        if match == None:
            OtherErrorfail_num += 1
            compare_info = str(OtherErrorfail_num)+ ': '+fail_build_info[1]+' has no compile result!'
            html_file.write(compare_info+'\n')
            html_file.close()
            return 1
        for i in range (0,len(self.logList)):
            ERROR = self.logList[i].findall(match)
            if ERROR:
                Erroelist[i] += 1
                print " . .. ... ",fails_num
                ss = str(Erroelist[i])+ ': '+ str(fail_build_info[1])
                compare_info = string.ljust(ss,88,' ')+ "has the same errors "+str(i)
                html_file.write(compare_info+'\n')
                pattern_flag = 1
                break
        if pattern_flag == 0:
##            print "Other Errors fails has happend! such as: " +  str(fail_build_info[1])
##            sys.exit()
            print "! !! !!! OtherErrorfail_num"
            OtherErrorfail_num += 1
            ss = str(OtherErrorfail_num)+ ': '+str(fail_build_info[1])
            compare_info = string.ljust(ss,88,' ')+"*has the other errors*"
            html_file.write(compare_info+'\n')
           
        html_file.close()
            
        
            
        
####################################################

if __name__ == '__main__':

    global fails_num
    global Error1fail_num
    global OtherErrorfail_num
    global Error2fail_num
    global Erroelist
    global NO
    global compiler_name
    Erroelist = [0,0,0,0,0,0,0,0,0]
    Error1fail_num = 0
    Error2fail_num = 0
    fails_num = 0
    OtherErrorfail_num = 0
    compiler_list = ["iar","uv4","kds","atl"]
    # ============config the compare info===================
    NO = '3367'
    compiler_name = "iar"
    compare_dict = {
        'iar': [
##                    "duplicate definitions for .*s_dummyData",\
##                    "the size of an array must be greater than zero",\
##                    "Fatal Error.* cannot open source file .*fsl_clock.h",\
##                    "Error.*: Cannot call intrinsic function .*__nounwind __DSB.* from Thumb mode in this architecture",\
                    "Warning.* function .__get_PRIMASK. declared implicitly",\
                    "Error.*: Cannot call intrinsic function .*__nounwind __WFI.* from Thumb mode in this architecture",\
                    "Fatal Error.* cannot open source file .*portmacro.h",\
                    "Error.*: struct .* has no field .*CRC",\
                    "Fatal Error.* cannot open source file .*fsl_uart.h",\
                    "Error.* identifier .*DAC_SR_DACBFRPTF_MASK.* is undefined",\
                    "Error.* identifier .*LPUART_BAUD_RXEDGIE_MASK.* is undefined",\
                    "Error.* identifier .*TSI_GENCS_EOSF_MASK.* is undefined",\
                    "Error.* identifier .*CAN_CTRL1_BOFFMSK_MASK.* is undefined",\
                    "Error.* identifier .*ENET_EIR_BABR_MASK.* is undefined",\
               ],
        'uv4': [
##                    "fsl_enet.h.* error:.*identifier .* is undefined",\
##                    "Symbol s_dummyData multiply defined",\
##                    "fsl_slcd.h.* error:.* identifier .* is undefined",\
##                    "cannot open source input file .*fsl_clock.h.*: No such file or directory",\
##                    "the size of an array must be greater than zero",\
                    "cannot open source input file .*portmacro.h.*: No such file or directory",
                    "error:.*struct .*has no field .*CRC",\
                    "No space in execution regions with .ANY selector matching",\
                    "error:.* identifier .*ENET_EIR_BABR_MASK.* is undefined",\
                    "warning:.* enumeration value is out of .*int.* range",\
                    "error:.* identifier .*DAC_SR_DACBFRPTF_MASK.* is undefined",\
                    "error:.* identifier .*LPUART_BAUD_RXEDGIE_MASK.* is undefined",\
                    "error:.* identifier .*TSI_GENCS_EOSF_MASK.* is undefined",\
                    "error:.* cannot open source input file .*fsl_uart.h.*: No such file or directory",\
                    "error:.* identifier .*CAN_CTRL1_BOFFMSK_MASK.* is undefined"
               ],
        
        'atl': [
##                    "collect2.exe: error: ld returned 1 exit status",\
##                    "fsl_slcd.h:.* error: unknown type name",\
##                    "fsl_enet.c.* error: unknown type name",\
##                    "fatal error: fsl_clock.h: No such file or directory",\
                    " region .*m_data.* overflowed by .* bytes",\
                    "fatal error: portmacro.h: No such file or directory",\
                    "fatal error: fsl_uart.h: No such file or directory",\
                    "error: unknown type name .*CAN_Type",\
                    "error: unknown type name .*DAC_Type",\
                    "error: unknown type name .*LPUART_Type",\
                    "error: unknown type name .*TSI_Type",\
                    "error: unknown type name .*ENET_Type"
               ],
        'kds': [
                    "duplicate definitions for .*s_dummyData",\
                    "the size of an array must be greater than zero",\
                    "fsl_clock.h: No such file or directory",\
                    "region m_data overflowed with stack and heap",\
                    "error: 'TSI_Type' has no member named .*CRC",\
                    "fatal error: portmacro.h: No such file or directory"
               ]
            
                }
    # ========== end ===================================
 
    dapeng_requst_fail_path = "http://10.192.225.198/dapeng/EditMcuautoRequest/"+NO+"/" 
    resule_file = open('.\\'+NO+compiler_name+'_compare_result.txt','w')
    resule_file.truncate()    #clear the file content
    
    html_file = open('.\\'+NO+compiler_name+'_compare_result.txt','a')
    html_file.write(dapeng_requst_fail_path+' -- '+compiler_name+' --\n')
    html_file.write('Check The Build Errors : --\n')
    html_file.close()
    
    starttime = datetime.datetime.now()
    iar_failcase = compare(dapeng_requst_fail_path,compiler_name,compare_dict[compiler_name])
    iar_failcase.compare_fail_log()
    endtime = datetime.datetime.now()
    print endtime - starttime
    
    html_file = open('.\\'+NO+compiler_name+'_compare_result.txt','a')
    html_file.write('Final Result: '+'Total compile fails num is '+str(fails_num)+'\n')
    for i in range(0,len(compare_dict[compiler_name])):
        html_file.write('Final Result: '+' This Error '+str(i)+' num is '+str(Erroelist[i])+'\n')
    html_file.write('Final Result: '+'Other Errors fails num is '+str(OtherErrorfail_num)+'  END at: '+str(endtime)+'\n')
    html_file.close()
 
   

    
    
