# -*- coding: utf-8 -*-

import qqlib

from qq.message import qqmsg
from qq.protocols import byteprotocol
from qqconsole import ConsoleProtocol
from socket import *
import md5
import util,struct,tea

from binascii import b2a_hex, a2b_hex

import basic

from Tkinter import *

from time import clock

import string, os, getpass, time ,threading ,sys

class qqrecv(threading.Thread):
    def __init__(self,protocol):
        self.protocol = protocol
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            self.protocol.datagramReceived()

class qqalive(threading.Thread):
    def __init__(self,protocol):
        self.protocol = protocol
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            self.protocol.alive()
            time.sleep(10)
            
class qqinput(threading.Thread):
    def __init__(self,protocol):
        self.protocol = protocol
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            self.cmd(self.input())

    def cmd(self,cmd):
        cmd = string.split(cmd,'/')
        if cmd[0]=='login':
            self.protocol.login()
        elif cmd[0]=='send':
            if len(cmd) != 3:
                self.protocol.printl("输入命令不完整")
            else:
                self.protocol.send(int(cmd[1]),cmd[2])
        elif cmd[0]=='list':
            print dir(self.protocol)
            self.protocol.friend_list.clear()
            self.protocol.get_friend_list(0)
        elif cmd[0]=='online':
            if len(self.protocol.friend_list) == 0:
                self.protocol.printl("请先用list命令获取你的好友列表。")
            else:
                self.protocol.friend_online.clear()
                self.protocol.get_friend_online(0)
        elif cmd[0]=='logout':
            #发送四次
            self.protocol.logout()
            self.protocol.logout()
            self.protocol.logout()
            self.protocol.logout()
        elif cmd[0]=='quit':
            #发送四次
            self.protocol.logout()
            self.protocol.logout()
            self.protocol.logout()
            self.protocol.logout()
            sys.exit(1)
        elif cmd[0]=='help':
            self.protocol.printl('login:登陆你的QQ，并将状态更改为上线。')
            self.protocol.printl('send/qq号码/内容:向指定号码发送消息。')
            self.protocol.printl('list:获取你的好友列表。')
            self.protocol.printl('online:获取你的在线好友。')
            self.protocol.printl('logout:将状态更改为离线。')
            self.protocol.printl('quit：离线并退出程序。')        
        else:
            self.protocol.printl("不能识别的命令，要获取帮助请使用help命令。")

    def input(self):
        #获取命令
        return(raw_input("Python-QQ:"))

def qq():
    log=qqlib.initLogging()
    nownum = 0
    lastuid = ''
    getnum = 0
    start = clock()
    conn=socket(AF_INET, SOCK_DGRAM)
    conn.settimeout(60)
    threads=[]
    if os.name == 'nt':
        qq_id=int(raw_input('请输入你的QQ号码:'.decode('utf-8').encode("cp936")))
        pwd=getpass.getpass('请输入你的QQ密码:'.decode('utf-8').encode("cp936"))
    else:
        qq_id=int(raw_input('请输入你的QQ号码:'))
        pwd=raw_input('请输入你的QQ密码:')
    qq_user=qqlib.qq(qq_id,pwd,log,conn)
    protocol=ConsoleProtocol(qq_user)
    try:
        log.info ('Python-QQ开始运行')
        protocol.pre_login()
    except Exception,ex:
        log.error(ex)
    threads.append(qqrecv(protocol))
    threads.append(qqalive(protocol))
    threads.append(qqinput(protocol))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    log.error('程序运行结束或失败，如有异常情况请和作者联系。')
    log.info( "收到 %d 条", getnum)
    log.info("用时：%.2f 秒", (clock()-start))
    log.info("每秒：%f条", (nownum / (clock()-start)))

def login():
    id=int(qq_id.get())
    pwd=qq_pwd.get()
    qq_user=qqlib.qq(id,pwd,log,conn)
    protocol=ConsoleProtocol(qq_user)
    log.info ('Python-QQ开始运行')
    protocol.pre_login()
    threads.append(qqrecv(protocol))
    threads.append(qqalive(protocol))
    threads.append(qqinput(protocol))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    log.error('程序运行结束或失败，如有异常情况请和作者联系。')
    log.info( "收到 %d 条", getnum)
    log.info("用时：%.2f 秒", (clock()-start))
    log.info("每秒：%f条", (nownum / (clock()-start)))

def abort():
    sys.exit(1)

if __name__ == "__main__":
    log=qqlib.initLogging()
    nownum = 0
    lastuid = ''
    getnum = 0
    start = clock()
    conn=socket(AF_INET, SOCK_DGRAM)
    conn.settimeout(60)
    threads=[]
    
    root = Tk()
    root.geometry("230x120")
    root.title("Python-QQ登陆")
    Label(root,text='Python语言实现的QQ客户端').place(x=8,y=3)
    Label(root,text='QQ号码:').place(x=15,y=30)
    Label(root,text='QQ密码:').place(x=15,y=55)
    qq_id = Entry(root,width = 16)
    qq_pwd = Entry(root,show='*',width = 16)
    qq_id.place(x=65,y=30)
    qq_pwd.place(x=65,y=55)
    button_login = Button(root,text="登陆", command = login)
    button_abort = Button(root, text="退出", command = abort)
    button_login.place(x=180,y=30)
    button_abort.place(x=180,y=55)
    Label(root,text='为了您和佳人的安全，请妥善保管您的密码！').place(x=5,y=85)
    root.mainloop()
