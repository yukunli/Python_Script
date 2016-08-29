# -*- coding: UTF-8 -*-
 
import socket
import sys
import os
import platform
import string
import time
import re
import datetime
import threading
from Tkinter import *
import ttk 
import tkFileDialog

if platform.system() == 'Windows':
    import _winreg
    
"""
状态表示位： 
             LS ：服务器监听成功
             SS : 服务器停止监听
             CF ：连接失败或断开连接
             CS ：连接成功
"""
        
class TCPServer:
    
    """ 实现：TCP/IP class，实现Socket通信的服务端的创建，启动监听，建立连接，接收数据，停止监听等功能
        备注：给类中的所有方法均由 ServerGui 调用
    """
    def __init__(self,PORT):

        self.Connect_State = 'SS'
        self.Port = PORT
        self.data = ''
        self.tcpClientSock = None
        self.Clientaddr = ''
        self.DataSize = 0
        self.dataList = []
        self.dataByteLenth = 0
        self.servsocket = None
        ##self.BUFSIZE 变量表示一次接收能够收到的最大字节数
        self.BUFSIZE = 19+512*2
        
    def CreatTCP(self):
        
        ##create an AF_INET, STREAM socket (TCP)
        if self.servsocket != None:
            self.servsocket.close()
            self.servsocket = None
        
        try:
            self.servsocket  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.servsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except  socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit()
        print "-- : Creat the TCP Client Successfully"
        time.sleep(1)
        
    def Listen(self):
        
        if self.Connect_State == 'LS': #如果已经有Port口打开，则先close()该套接字
            self.servsocket.close()
            self.Connect_State = 'SS'
            time.sleep(0.5)
        try:
            self.servsocket.bind(('',self.Port))
            self.servsocket.listen(10)
            print self.Port
            self.Connect_State = 'LS'
            time.sleep(0.5)
            return True
        except socket.error,msg:
            print 'Listen failed !'+ str(msg[0]) + ' , Error message : ' + msg[1]
            self.servsocket.close()
            return False

    def Dislisten(self):
        
        if self.tcpClientSock != None:
            self.tcpClientSock.close()
            self.Connect_State = 'CF'
        if self.servsocket != None:
            self.servsocket.close()
            print "-- : Close the TCP Client!"
            self.Connect_State = 'SS'
            return True
        else:
            self.Connect_State = 'SS'
            print"There's no connection to be disconnected "
            return False
            
    def AcceptConnect(self):
        
        tcpClientSock = None
        while self.Connect_State == 'LS':
            try:
                self.servsocket.settimeout(6)
                self.tcpClientSock,self.Clientaddr = self.servsocket.accept()
            except socket.timeout:
                print 'reaccepting...'
                
            if self.tcpClientSock :
                self.Connect_State = 'CS'
                print "Connect successfull "
                break        
            
    def RecvData(self):
        
        if self.Connect_State == 'CS':
            try:
                self.tcpClientSock.settimeout(10)  #设置10s超市，如果10S内没有收到数据则认为timeout
                self.data = self.tcpClientSock.recv(self.BUFSIZE)
                if self.data == '' and self.Connect_State != 'SS' :
                    self.Connect_State = 'CF'
                    print "client disconnect"
                    return None
                else:       
                    self.dataList.append(self.data)
                    self.dataByteLenth += len(self.data)
                    return None
                return
        
            except socket.timeout:
                print "-- : Time out!"
                if self.Connect_State != 'SS':
                    self.Connect_State = 'CF' 
        return None
    
class ServerGui(Frame):
    """ 实现： GUI界面控制class ，实现GUI的界面布局和主要的功能调用
    """
    def __init__(self,master = None):

        
        Frame.__init__(self,master)
        
        self.widgetList = []
        self.currState = ''

        self.Port = '555'
        self.SavePath = 'C:/Users/Administrator/Desktop'  ##'Please choose a path'
        self.ServerP = None
        
        self.string = ''
        self.ConnectState = ''
        self.timestartflag = True
        self.starttime = ''
        self.endtime = ''
        self.DataListBuf = []
        self.DataLenth = 0
        self.WriteFlag = False
        self.grid()
        self.dataframe = ''
        self.showstringflag = False
        #set defaules
        osName = platform.system()
        curDate = time.strftime("%m/%d/%Y")

        # defining options for opening a directory
        self.dir_opt = {}
        if osName == 'Windows':
            self.dir_opt['initialdir'] = 'C:\\'
        self.dir_opt['mustexist'] = False
        self.dir_opt['parent'] = master

        #creat indicator for recive data
        
        self.main_gui(master)
    
        
    def main_gui(self,master):
        """ 实现：GUI各个控件的创建，包括Label，Button，Entry，Progressbar和Text
            备注：控件中的 command 参数用于链接到本类中的一些方法（函数调用）
        """

        #Remove active widgets from the screen and then clear widget list out
        if self.widgetList:
            for w in self.widgetList:
                w.grid_remove()
            del self.widgetList[:]

        # Begin repopulating window with new widget list
        osName = platform.system()
        if osName != 'Darwin':
            labelFont =  'Arial 9 bold'
        else:
            labelFont = 'bold'
            
        ## Widget 0 is a label for save path entry
        self.widgetList.append(Label(self, text='Save Path:', font=labelFont))
        self.widgetList[0].grid(row=0, column=1, sticky=W, pady=(5, 0),padx=(10, 0))
        
        ## Widget 1 is a text field entry for save path
        self.widgetList.append(Entry(self, width=45))
        self.widgetList[1].insert(0, self.SavePath)
        self.widgetList[1].grid(row=1, column=1, sticky=W, pady=(0, 0),padx=(10, 0))

        self.SavePath = self.widgetList[1].get()

        ## Widget 2 is a button to browse for KSDK path
        self.dir_opt['title'] = 'Select the directory that could ' + \
                                'save the received data.'
        self.widgetList.append(Button(self, text='Browse', \
                                      command=lambda: self.ask_set_directory(False, 1)))
        self.widgetList[2].grid(row=1, column=2, columnspan=2, sticky=E+W, pady=(0, 0),padx=(10, 0))

        ##Widget 3 is label for porNo name text filed
        self.widgetList.append(Label(self, text='Port Name:', font=labelFont))
        self.widgetList[3].grid(row=2, column=1, sticky=W, pady=(2, 0),padx=(10, 0))

        ## Widget 4 is the text field for project name entry
        
        self.widgetList.append(Entry(self, width=45))
        self.widgetList[4].insert(0, self.Port)
        self.widgetList[4].grid(row=3, column=1, sticky=W,pady=(0, 0),padx=(10, 0))
        
        ## Widget 5 is a button for start listen
        self.widgetList.append(Button(self, text='Start listening', \
                                      command= self.CreatTCPandListen))
        self.widgetList[5].grid(row=3, column=2, sticky=W,pady=(0, 0),padx=(10, 0))

        ## Widget 6 is a button for stop listen
        self.widgetList.append(Button(self, text='Stop listening', \
                                      command= self.DisListenTCP))
        self.widgetList[6].grid(row=3, column=3, sticky=E,pady=(0, 0),padx=(10, 0))

        ##Widget 7 is the text field for the connect state
        ##Widget 8 is the label field for the connect state
        self.widgetList.append(Label(self, text='Connect Status: ', font=labelFont))
        self.widgetList[7].grid(row=4, column=1, sticky=W, pady=(2, 0),padx=(10, 0))

        self.ConnectState = StringVar()
        self.ConnectState.set('Wait Connect...')
        self.widgetList.append(Label(self, textvariable=self.ConnectState, font=('Arial', 10)))
        self.widgetList[8].grid(row=5, column=1, sticky=W, pady=(0, 0),padx=(10, 0))
        
        ##widget 9 is text field for the byte num
        ##widget 10 is label field for the byte num
        self.widgetList.append(Label(self, text=' Byte num:', font=labelFont))
        self.widgetList[9].grid(row=4, column=2, sticky=W, pady=(2, 0),padx=(10, 0))

        self.RecvByteNum = StringVar()
        self.RecvByteNum.set('0')
        self.widgetList.append(Label(self, textvariable=self.RecvByteNum, font=('Arial', 10)))
        self.widgetList[10].grid(row=5, column=2, sticky=W, pady=(2, 0),padx=(10, 0))
        
        ## widget 11 is text field for a timeshow
        ## widget 12 is label field for a timeshow
        self.widgetList.append(Label(self, text='time: ', font=labelFont))
        self.widgetList[11].grid(row=4, column=3, sticky=W, pady=(2, 0),padx=(10, 0))

        self.Timehint = StringVar()
        self.Timehint.set('00:00')
        self.widgetList.append(Label(self, textvariable=self.Timehint, font=('Arial', 10)))
        self.widgetList[12].grid(row=5, column=3, sticky=W, pady=(2, 0),padx=(10, 0))

        ##widget 13 is label field for a timeshow
        self.valbar = IntVar() 
        self.widgetList.append(ttk.Progressbar(self, orient = "horizontal", length=316, mode="determinate", variable=self.valbar))
        self.widgetList[13].grid(row=6, column=1, sticky=W, pady=(10, 0),padx=(10, 0)) 

        ##widget 14 is text field for the received data show 一个窗口能够显示14行信息
        self.widgetList.append(Text(self, width=75,height=14,font=('Arial', 10)))
        scrollb = Scrollbar(self, command=self.widgetList[14].yview)
        self.widgetList[14].grid(row=7, column=1,columnspan=3, sticky=W, pady=(10, 0),padx=(10, 0))
        scrollb.grid(row=7, column=3, sticky='nsew',pady=(10, 0),padx=(10, 0))
        self.widgetList[14]['yscrollcommand'] = scrollb.set
        
        ##widget 15 is text field for the copyright
        self.widgetList.append(Label(self, text='@copyright 东北空管局 技术保障中心 2016', font=labelFont))
        self.widgetList[15].grid(row=8, column=1,columnspan=3, sticky=E, pady=(5, 0),padx=(10, 0))
        
    def CreatTCPandListen(self):
        """ 实现： 创建Socket并启动监听，监听成功后创建并启动4个线程
            备注： 由GUI上的 Start listening 按钮触发执行
        """
        self.ServerP = TCPServer(int(self.widgetList[4].get()))
        self.ServerP.CreatTCP()
        Backstatus = self.ServerP.Listen()
        time.sleep(0.1)
        if Backstatus:
            self.ConnectState.set('Listening successfully!')
            #创建4个线程，依次为：TimeShow，tringShow，WriteFile，OpretData
            OpretData_thread = threading.Thread(group=None, target = self.OpretData)
            TimeShow_thread = threading.Thread(group=None, target = self.TimeShow)
            WriteFile_thread = threading.Thread(group=None, target=self.WriteFile)
            StringShow_thread = threading.Thread(group=None, target=self.StringShow)
            
            try:
                TimeShow_thread.start()
                print "-- : Start Timeshow thread"
            except:
                print "\nError: unable to Start Timeshow thread"
             
            try:
                StringShow_thread.start()
                print "-- : Start StringShow thread" 
            except:
                print "\nError: unable to StringShow thread"
            try:
                WriteFile_thread.start()
                print "-- : Start WriteFile thread" 
            except:
                print "\nError: unable to WriteFile thread"
            try:
                OpretData_thread.start()
                print "-- : Start OpretData thread" 
            except:
                print "\nError: unable to OpretData thread"
               
        else:
            self.ConnectState.set('Listening failed!')
        
            
    def DisListenTCP(self):
        """ 实现： 停止Socket监听，将self.ServerP.Connect_State置为'SS'，4个线程都将结束
            备注： 由GUI上的 Stop listening 按钮触发执行
        """
        if  self.ServerP:                    
            Backstatus = self.ServerP.Dislisten()
            if Backstatus:
                self.ConnectState.set('Stop listening successfully')
                
            else:
                self.ConnectState.set('Stop listening failed!')
        
    def ask_set_directory(self, isTyped, widgetIndex):
        """ 实现： Callback method for browe selection of KSDK directory
            备注： 由GUI上的 Browse 按钮触发执行
        """
        self.SavePath = tkFileDialog.askdirectory(**self.dir_opt)
        if self.SavePath != '':
            self.widgetList[widgetIndex].delete(0, END)
            self.widgetList[widgetIndex].insert(0, self.SavePath)
            self.SavePath.replace("/",'\\')
            if os.path.isdir(self.SavePath):
                print self.SavePath
                return
            else:
                self.widgetList[widgetIndex].delete(0, END)
                self.widgetList[widgetIndex].insert(0, 'please choose right address')
        else:
            return
    def WriteFile(self):
        """ 实现： 将接收的数据写入txt文本文件
            规则1：自线程建立起开始执行该函数，直到停止监听
            规则2：每接收10次数据写一次文件
            规则3：每到一个时间整点（24小时制）就创建一个新的文件，文件以下面格式命名“
                   4GData_filetileT.txt ：其中，filetileT格式为2016-8-22_15
        """
        global per_filetileT
        global filetileT
        per_filetileT = None
        
        filetileT1 = str(datetime.datetime.now()).split('.')[0]
        filetileT2 = filetileT1.split(' ')[0] +"_"+filetileT1.split(' ')[1]
        filetileT = filetileT2.split(':')[0] #每小时存一个文件
        per_filetileT = filetileT
        Savefile = open(self.SavePath+'/4GData_'+filetileT+'.txt','a')
        while self.ServerP.Connect_State != 'SS':
            
            filetileT1 = str(datetime.datetime.now()).split('.')[0]
            filetileT2 = filetileT1.split(' ')[0] +"_"+filetileT1.split(' ')[1]
            filetileT = filetileT2.split(':')[0] #每小时存一个文件
            
            if per_filetileT != filetileT:
                Savefile.close()
                Savefile = open(self.SavePath+'/4GData_'+filetileT+'.txt','a')
                per_filetileT = filetileT
            
            while self.WriteFlag == True:
               ##self.DataListBuf 为包含10次接收到的数据的列表，将该变量内容写入文本文件
                try:
                    for i in range(len(self.DataListBuf)):
                        Savefile.write(self.DataListBuf[i])
                except:
                    print "Write file wrong."
                finally:
                    del self.DataListBuf
                    self.DataListBuf = []
                    self.WriteFlag = False  
            if self.ServerP.Connect_State == 'CF':
                Savefile.close()
                time.sleep(0.1)
                Savefile = open(self.SavePath+'/4GData_'+filetileT+'.txt','a')
                
        Savefile.close()
        print "-- :The WriteFile thread is end."
        
    def OpretData(self):
        """ 实现： 与客户端连接传输连接并接收4G数据
            规则： 自线程建立起开始执行该函数，直到停止监听
        """
        while self.ServerP.Connect_State != 'SS':  
            self.DataLenth = 0
            ##AcceptConnect 为服务端与客户端建立Socket连接
            self.ServerP.AcceptConnect()
            print self.ServerP.Connect_State
            while self.ServerP.Connect_State == 'CS':
            ##RecvData 为接收数据子函数，在连接状态下循环执行   
                self.ServerP.RecvData()
                ## 将一次接收到的数据存入缓存self.dataframe，以便于显示
                if self.showstringflag == False:
                    self.dataframe = self.ServerP.data
                    self.showstringflag = True
            ## 如果接收到15次数据，则将接收到的数据传给缓存变量self.DataListBuf，并置写文件标志位    
                if len(self.ServerP.dataList) > 15:
                    self.DataListBuf = self.ServerP.dataList
                    self.WriteFlag = True
                    del self.ServerP.dataList
                    self.ServerP.dataList = []
                    
        print '-- :The OpretData thread is end.'
            
    def TimeShow(self):
        """ 实现： GUI界面的时间显示和接收字节显示，以及进度条显示
            规则： 自线程建立起开始执行该函数，直到停止监听
        """
        BarValue = 0
        self.starttime = datetime.datetime.now()
        while self.ServerP.Connect_State != 'SS':
            ##获得系统的当前时间
            self.endtime = datetime.datetime.now()
            TimePeriod =  self.endtime - self.starttime
            ##显示已经运行了的时间
            self.Timehint.set(str(TimePeriod).split('.')[0])
            ##显示已经接收到的字节数
            self.RecvByteNum.set(str(self.ServerP.dataByteLenth))
            ##显示进度条和连接状态
            if self.ServerP.Connect_State == 'CS':
                self.ConnectState.set('Connected with the IP: '+ str(self.ServerP.Clientaddr[0])+'.'+ str(self.ServerP.Clientaddr[1]))
                self.valbar.set(BarValue)
                BarValue += 0.03
                if BarValue > 100:
                    BarValue = 0
            elif self.ServerP.Connect_State == 'CF':
                self.ConnectState.set('The client disconnect or time out')
                BarValue = 0
                self.valbar.set(BarValue)
                self.ServerP.Connect_State = 'LS'  
                    
        BarValue = 0
        self.valbar.set(BarValue)
        print '-- :The TimeShow thread is end.'
        
    def StringShow(self):
        """ 实现： 接收到的字节显示在文本框中
            规则： 自线程建立起开始执行该函数，直到停止监听
            备注： 该线程测试时总是引起软件卡死，原因不明，已经屏蔽
        """
        while self.ServerP.Connect_State != 'SS':
            
            if self.showstringflag == True:
                pattarn = re.match(r'.*(Frame.*\r\n.*\r\n.*)',self.dataframe)
                if pattarn:
                    showframe = "".join(pattarn.groups(0))
                    SS = self.widgetList[14].index(END)
                    ##print '++ '+ str(SS)
                    if float(SS) >= 70.0:
                        self.widgetList[14].delete(1.5,42.0)
                    try:          
                        self.widgetList[14].insert(END,showframe)
                        time.sleep(1.0)
                        self.widgetList[14].see(END)

                    finally:
                        time.sleep(1.0)
                self.showstringflag = False
            
        print '-- :The StringShow thread is end.'
        
def CreatRoot():
    """ 实现： 创建GUI Root, 设置软件title和显示窗大小
        备注： 在此函数中修改 软件的title
    """
    global root
    osName = platform.system()
    root = Tk()
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    root.resizable(width=FALSE, height=FALSE)
    root.title("4G数据传输系统1.2")
    if osName == 'Windows':
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop\\WindowMetrics")
        value = _winreg.QueryValueEx(key, "AppliedDPI")[0]
        ##print "DPI value: " + str(value)

        if value == 96:
            WIN_SCALE = 1.0
        elif value == 120:
            WIN_SCALE = 1.25
        elif value == 144:
            WIN_SCALE = 1.5
        elif value == 192:
            WIN_SCALE = 2.0
        else:
            WIN_SCALE = value / 96.0

        windowWidth = (570 * WIN_SCALE)
        windowHeight = (450 * WIN_SCALE)

        # Get x & y location for centering the window
        xLocation = screenWidth / 2 - windowWidth / 2
        yLocation = screenHeight / 2 - windowHeight / 2

        root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, xLocation, yLocation))


def main():
    global root
    global app
    CreatRoot()
    app = ServerGui(root)
    root.mainloop()
    
    try:
        root.destroy()                  # Destroy the Tkinter object 'root'
        sys.exit()
    except TclError:
        sys.exit()
        
if __name__ == '__main__':
    """ 实现： 函数入口
    """
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()    
             
