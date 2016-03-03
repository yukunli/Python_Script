# -*- coding: cp936 -*-

import re 
import urllib
import string
import datetime
import threading
import time
import sys
from Tkinter import *
import ttk 
import tkFileDialog
import tkMessageBox

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
        global exitflag
        compiler_dict = {"iar":3,"uv4":4,"gcc_arm":5,"kds":8,"atl":10}
        print compiler_dict[self.compiler]
        main_html = self.failcase.getHtml(self.requstPath + "?showall=1&compilerid="+str(compiler_dict[self.compiler])+"&buildresult=2" )
        self.failcase.write_html_txt(main_html)
        page_file = open('.\\page_html.txt','r')
        line = page_file.readlines()
        page_file.close()
         
        for item in line:
            if not exitflag:
                fail_build_info = self.failcase.check_fail_html(item)
                if fail_build_info:
                    fails_num += 1
                    self._match_pattern(fail_build_info)
                    del fail_build_info
                    if DEBUG :
                         print "^^^^^^^"
            else:
                print "\n Thread is killed! "
                break
        del main_html
        print "compare build error finished!"
        
    def _match_pattern(self,fail_build_info):
        global Error1fail_num
        global Error2fail_num
        global OtherErrorfail_num
        global Erroelist
        global Requst_NO
        global compiler_name
        
        other_errorlist = []
        html_file = open('.\\'+Requst_NO+compiler_name+'_compare_result.txt','a')
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

            print "! !! !!! Other Error failed"
            OtherErrorfail_num += 1
            ss = str(OtherErrorfail_num)+ ': '+str(fail_build_info[1])
            compare_info = string.ljust(ss,88,' ')+"*has the other errors*"
            html_file.write(compare_info+'\n')
           
        html_file.close()
            
class Setting_Gui:
    """
    """
    def __init__(self,master = None):

        global Timeshow
        self.master = master
        self.frame = Frame(self.master)
        self.master.geometry('700x500')
        self.master.minsize(700,400)
        self.master.maxsize(700,500)
        self.master.title("Build LOG spider1.0") 
        Button(self.master, text='Refresh The Settings Info', bg='blue',fg='white',\
               font=('Arial', 10),command=self._Refresh_info).pack(fill=X,side=BOTTOM)
        ##Requst number
        self.CaseNo_Input = StringVar()
        self.CaseNo_Input.set("3367")   
        CaseNo_entry = Entry(self.master,text = self.CaseNo_Input,width=8,background='white',
                                font=('Arial', 15),foreground='black').place(x=120,y=30)
        Label(self.master,text='Requst Number:',font=('Arial', 10)).place(x=10,y=30)

        ##Compiler select
        self.compiler_Input = StringVar()
        self.compiler_Input.set("iar")
        Compiler_combobox = ttk.Combobox(self.master,text=self.compiler_Input,values=["iar","uv4","kds","atl","gcc_arm"],\
                                           width=5,font=('Arial', 15)).place(x=335,y=30)
        Label(self.master,text='Compiler select:',font=('Arial', 10)).place(x=230,y=30)
        ## save button
        Save_Button = Button(self.master,text = ' Save ',command=self._Save_info,font=('Arial', 10,'bold')).place(x=440,y=30)
        ## run button
        Run_Button = Button(self.master,text=' Run ',command=self.Run_spider,font=('Arial', 10,'bold')).place(x=530,y=30)
        ## stop button
        Stop_Button = Button(self.master,text=' Stop ',command=self.Stop_spider,font=('Arial', 10,'bold')).place(x=610,y=30)
        ## Error info text
        self.ERROR_Info = Text(self.master,font=('Arial',10),height=15,width=90)
        self.ERROR_Info.insert(INSERT," Please entry the ERROR type as such format:\n\n")
        self.ERROR_Info.insert(END,"1:Error.* cannot open source file .*portmacro.h\n\n")
        self.ERROR_Info.insert(END," You can also press bule button to get the last error info Firstly \n\n")
        self.ERROR_Info.insert(END," Add the '#' at the end of line if you want to comment it...\n\n")
        self.ERROR_Info.place(x=30,y=100)

        ## time show
        Timeshow = StringVar()
        Timeshow.set('Time: 00')
        Timlabel = Label(self.master,textvariable=Timeshow,font=('Arial', 10)).place(x=30,y=350)
        self.master.update()
        root.protocol("WM_DELETE_WINDOW", root.destroy)
    def _Refresh_info(self):
        print " \nRefresh_info ..."
        CompilerName = self.compiler_Input.get()
        self.ERROR_Info.delete('1.0',END)
        fileERROR = open('./'+CompilerName+'_ERROR_Type.txt','r')
        Errors = fileERROR.readlines()
        for line in Errors:
           self.ERROR_Info.insert(END,line)
        fileERROR.close()
    def _Save_info(self):

        CompilerName = self.compiler_Input.get()
        ErrorInfo = self.ERROR_Info.get('1.0',END)
        fileERROR = open('./'+CompilerName+'_ERROR_Type.txt','w')
        fileERROR.write(ErrorInfo)
        fileERROR.close()
        
    def Run_spider(self):
        
        global Requst_NO
        global compiler_name
        global compare_dict
        global Timeshow
        compare_dict = {}
        ERROR_List = []
        Requst_NO = self.CaseNo_Input.get()
        compiler_name = self.compiler_Input.get()
        fileERROR = open('./'+compiler_name+'_ERROR_Type.txt','r')
        Errors = fileERROR.readlines()
        fileERROR.close()
        for line in Errors:
            Error_type = re.match(r'^\d{1,2}:(.*)[^#]\n$',line)
            if Error_type:
                ERROR_List.append(''.join(Error_type.groups(0)))
        compare_dict[compiler_name] = ERROR_List
        
        print (Requst_NO,compiler_name,compare_dict[compiler_name])
        ## creat one thread 
        Main_thread = threading.Thread(group=None, target = self.Main_function)
        Time_show_thread = threading.Thread(group=None, target = self.Time_function)
        try:
            Main_thread.start()
            Time_show_thread.start()
        except:
           print "\nError: unable to start thread"

    def Stop_spider(self):
        global exitflag
        global timeflag
        timeflag = 1
        exitflag = 1
        time.sleep(1)
    def Time_function(self):
        global Timeshow
        global timeflag
        global starttime
        timeflag =0
        starttime = datetime.datetime.now()
        while not timeflag:
            endtime = datetime.datetime.now()
            Timeshow.set(endtime - starttime)
    def Main_function(self):
            
            global Requst_NO
            global compiler_name
            global compare_dict
            global fails_num
            global Error1fail_num
            global OtherErrorfail_num
            global Error2fail_num
            global Erroelist
            global exitflag
            global starttime
            exitflag = 0
            Erroelist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            Error1fail_num = 0
            Error2fail_num = 0
            fails_num = 0
            OtherErrorfail_num = 0
            compiler_list = ["iar","uv4","kds","atl"]

            dapeng_requst_fail_path = "http://10.192.225.198/dapeng/EditMcuautoRequest/"+Requst_NO+"/" 
            resule_file = open('.\\'+Requst_NO+ compiler_name +'_compare_result.txt','w')
            resule_file.truncate()    #clear the file content
            
            html_file = open('.\\'+Requst_NO+compiler_name+'_compare_result.txt','a')
            html_file.write(dapeng_requst_fail_path+' -- '+compiler_name+' --\n')
            html_file.write('Check The Build Errors : --\n')
            html_file.close()
            
            build_failcase = compare(dapeng_requst_fail_path,compiler_name,compare_dict[compiler_name])
            build_failcase.compare_fail_log()
            endtime = datetime.datetime.now()
            print endtime - starttime
            
            html_file = open('.\\'+Requst_NO+compiler_name+'_compare_result.txt','a')
            html_file.write('Final Result: '+'Total compile fails num is '+str(fails_num)+'\n')
            for i in range(0,len(compare_dict[compiler_name])):
                html_file.write('Final Result: '+' This Error '+str(i)+' num is '+str(Erroelist[i])+'\n')
            while not exitflag:
                html_file.write('Final Result: '+'Other Errors fails num is '+str(OtherErrorfail_num)+'  END at: '+str(endtime)+'\n')
            html_file.close()
####################################################

if __name__ == '__main__':


    root = Tk()
    app = Setting_Gui(root)
    root.mainloop()
