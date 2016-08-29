# -*- coding: UTF-8 -*-
 
import socket
import sys
import os
import platform
import string
import time
import datetime
import threading
from Tkinter import *
import ttk 
import tkFileDialog

if platform.system() == 'Windows':
    import _winreg
    
        
class TCPServer:
    """
    """
    def __init__(self,PORT):

        self.Connect_State = 'WC'
        self.Port = PORT
        self.data = ''
        self.tcpClientSock = None
        self.Clientaddr = ''
        self.BUFSIZE = 19+512*2
        self.DataSize = 0
        self.dataList = []
        self.dataByteLenth = 0
        self.servsocket = None
    def CreatTCP(self):
        
        #create an AF_INET, STREAM socket (TCP)
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
            print"There's no connection to be disconnected "
            return False
            
    def AcceptConnect(self):
        
        while self.Connect_State == 'LS':
            print '!!!'
            self.tcpClientSock,self.Clientaddr = self.servsocket.accept()
            if self.tcpClientSock :
                self.Connect_State = 'CS'
                print "Connect successfull "
                print self.Clientaddr
                break
            else:
                self.Connect_State = 'CF'
                print "Connect failed! "
            
    def RecvDate(self):
        recvfailnum = 0
        try:
            self.tcpClientSock.settimeout(20)
            self.data = self.tcpClientSock.recv(self.BUFSIZE)
            if self.data == '':
                self.Connect_State = 'CF'
                print "client disconnect"
            else:       
                self.dataList.append(self.data)
                self.dataByteLenth += len(self.data)
            return
    
        except socket.timeout:
            print "-- : Time out!"
            self.Connect_State = 'CF'
            
        if self.Connect_State == 'CF':
            self.tcpClientSock.close()
            self.tcpClientSock = None
            
        return
    
class ServerGui(Frame):
    """
    """
    def __init__(self,master = None):

        
        Frame.__init__(self,master)
        
        self.widgetList = []
        self.currState = ''

        self.Port = '555'
        self.SavePath = 'Please choose a path'
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

        ##widget 14 is text field for the copyright
        self.widgetList.append(Label(self, text='@copyright 丁盛伟 2016.7.8', font=labelFont))
        self.widgetList[14].grid(row=7, column=1,columnspan=3, sticky=E, pady=(20, 0),padx=(10, 0))
        
    def CreatTCPandListen(self):

        self.ServerP = TCPServer(int(self.widgetList[4].get()))
        self.ServerP.CreatTCP()
        Backstatus = self.ServerP.Listen()
        time.sleep(0.1)
        if Backstatus:
            hintcontent = 'Listening successfully!'
            self.ConnectState.set('Listening successfully!')
            #creat two thread
            OpretData_thread = threading.Thread(group=None, target = self.OpretData)
            TimeShow_thread = threading.Thread(group=None, target = self.TimeShow)
            WriteFile_thread = threading.Thread(group=None, target=self.WriteFile)
            try:
                OpretData_thread.start()
                print "-- : Start OpretData thread" 
            except:
                print "\nError: unable to OpretData thread"
               
            try:
                TimeShow_thread.start()
                print "-- : Start Timeshow thread"
            except:
                print "\nError: unable to Start Timeshow thread"
            
            try:
                WriteFile_thread.start()
                print "-- : Start WriteFile thread" 
            except:
                print "\nError: unable to WriteFile thread"
            
        else:
            self.ConnectState.set('Listening failed!')
        
            
    def DisListenTCP(self):

        if  self.ServerP:                    
            Backstatus = self.ServerP.Dislisten()
            if Backstatus:
                self.ConnectState.set('Stop listening successfully')
                
            else:
                self.ConnectState.set('Stop listening failed!')
        
    def ask_set_directory(self, isTyped, widgetIndex):
        """Callback method for browe selection of KSDK directory

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

        per_filetileT = None
        filetileT = str(datetime.datetime.now())
        filetileT = filetileT.split('.')[0]
        filetileT = filetileT.split(' ')[0] +"_"+filetileT.split(' ')[1]
        filetileT = filetileT.split(':')[0] #每小时存一个文件
        per_filetileT = filetileT
        Savefile = open(self.SavePath+'/4GDate_'+filetileT+'.txt','a')
        while self.ServerP.Connect_State != 'SS':
            filetileT = str(datetime.datetime.now())
            filetileT = filetileT.split('.')[0]
            filetileT = filetileT.split(' ')[0] +"_"+filetileT.split(' ')[1]
            filetileT = filetileT.split(':')[0] #每小时存一个文件
            if per_filetileT != filetileT: 
                Savefile = open(self.SavePath+'/4GDate_'+filetileT+'.txt','a')
                per_filetileT = filetileT
            
            while self.WriteFlag == True:
               # print str(datetime.datetime.now())
                try:
                    lenth = len(self.DataListBuf)
                    for i in range(lenth):
                        Savefile.write(self.DataListBuf[i])
                    del self.DataListBuf
                    self.DataListBuf = []
                    self.WriteFlag = False
                except:
                    print "Write file wrong."
                if self.ServerP.Connect_State == 'CF':
                   Savefile.close() 
        Savefile.close()
        print "-- :The WriteFile thread is end. \n"
        
    def OpretData(self):

        while self.ServerP.Connect_State != 'SS': #服务器处于监听状态 
            self.DataLenth = 0
            self.ServerP.AcceptConnect()
            while self.ServerP.Connect_State == 'CS':
                self.ConnectState.set('Connected with the IP: '+ str(self.ServerP.Clientaddr[0])+'.'+ str(self.ServerP.Clientaddr[1]))
                if self.ServerP.Connect_State == 'CF':  #如果客户端断开连接
                    self.ConnectState.set('Connection is broken ')
                    
                ## start recv data   
                self.ServerP.RecvDate()
                if len(self.ServerP.dataList) >= 10:
                    self.DataListBuf = self.ServerP.dataList
                    self.WriteFlag = True
                    del self.ServerP.dataList
                    self.ServerP.dataList = []
                    
        print '-- :The OpretData thread is end. \n'
            
    def TimeShow(self):
        BarValue = 0
        self.starttime = datetime.datetime.now()
        while self.ServerP.Connect_State != 'SS':
            self.endtime = datetime.datetime.now()
            TimePeriod =  self.endtime - self.starttime
            self.Timehint.set(str(TimePeriod).split('.')[0])
            self.RecvByteNum.set(str(self.ServerP.dataByteLenth))
            if self.ServerP.Connect_State == 'CS':
                self.valbar.set(BarValue)
                BarValue += 10
                time.sleep(0.3)
                if BarValue > 100:
                    BarValue = 0
            elif self.ServerP.Connect_State == 'CF':
                BarValue = 0
                self.valbar.set(BarValue)
                self.ConnectState.set('The client disconnect or time out')
        BarValue = 0
        self.valbar.set(BarValue)
        print '-- :The TimeShow thread is end. \n'

def CreatRoot():
    """
    """
    global root
    osName = platform.system()
    root = Tk()
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    root.resizable(width=FALSE, height=FALSE)
    root.title("4G数据传输系统")
    if osName == 'Windows':

        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop\\WindowMetrics")
        value = _winreg.QueryValueEx(key, "AppliedDPI")[0]

        print "DPI value: " + str(value)

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

        #print "DPI scale: " + str(kGUI.WIN_SCALE)
        
        windowWidth = (570 * WIN_SCALE)
        windowHeight = (250 * WIN_SCALE)

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
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()    
             
