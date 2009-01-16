# -*- coding: utf-8 -*-

import qqlib

from qq.message import qqmsg
from qq.protocols import qqp
from twisted.internet import reactor, protocol, defer, threads
import Queue
import md5
import util,struct,tea

from binascii import b2a_hex, a2b_hex

import basic

from time import clock

import string, os, getpass

class ConsoleProtocol(qqlib.qqClientProtocol):
    def logout(self):
        pass

    def alive(self):
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_alive')
        message.body.setField('qq',str(self.qq.id))
        self.sendDataToQueue(message)
        reactor.callLater(60, self.alive)

    def reg_id_2(self):
        pass

    def updata_info(self):
        pass

    def search_user(self):
        pass

    def get_user_info(self):
        pass

    def add_friend_auth(self):
        pass

    def del_friend(self):
        pass

    def buddy_auth(self):
        pass

    def chang_status(self):
        pass

    def reg_id_1(self):
        pass

    def ack_sys_msg(self):
        pass

    def send(self, recv_qq, msg):
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_send')
        self.qq.session_id += 1
        message.body.setField('send_qq',self.qq.id)
        message.body.setField('recv_qq',recv_qq)
        message.body.setField('ver',basic.QQ_ver)
        message.body.setField('send_qq1',self.qq.id)
        message.body.setField('recv_qq1',recv_qq)
        message.body.setField('md5',md5.new(str(self.qq.id)+self.qq.session).digest())
        message.body.setField('type',11)
        message.body.setField('session_id',self.qq.session_id)
        message.body.setField('send_time',recv_qq)
        message.body.setField('send_face',0)
        message.body.setField('font_info',1)
        message.body.setField('msg_pass',1)
        message.body.setField('msg_id',1)
        message.body.setField('msg_type',1)
        message.body.setField('msg_data',msg)
        message.body.setField('msg_link',' '+chr(00))
        message.body.setField('msg_end',9)
        message.body.setField('msg_red',0)
        message.body.setField('msg_green',0)
        message.body.setField('msg_blue',0)
        message.body.setField('unknown',0)
        message.body.setField('encoding',0x8602)
        message.body.setField('info',a2b_hex('cbcecce5'))
        #尾部分长度固定为9
        message.body.setField('len',len(message.body.fields['msg_data'])+9)
        self.sendDataToQueue(message)

    def recv(self):
        pass
    
    def remove_self(self):
        pass

    def ask_key(self):
        pass

    def cell_phone_1(self):
        pass

    def login(self):
        self.pre_login()

    def get_friend_list(self, start):
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_get_friend_list')
        message.body.setField('start', start)
        message.body.setField('sorted',basic.QQ_friend_list_sorted)
        self.sendDataToQueue(message)

    def get_friend_online(self, start):
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_get_friend_online')
        message.body.setField('type', 0x02)
        message.body.setField('start', start)
        message.body.setField('unknown',0)
        message.body.setField('unknown1',0)
        self.sendDataToQueue(message)

    def cell_phone_2(self):
        pass

    def send_sms(self):
        pass

    def group_cmd(self):
        pass

    def test(self):
        pass

    def group_data(self):
        pass

    def upload_group(self):
        pass

    def friend_data(self):
        pass

    def download_group(self):
        pass

    def level(self):
        pass

    def cluster_data(self):
        pass

    def advanced_search(self):
        pass

    def pre_login(self):
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_pre_login')
        message.body.setField('unknown',0)
        self.sendDataToQueue(message)
        qqp.qqClientQueueProtocol.connectionMade(self)

    def msg_sys(self):
        pass

    def friend_chang_status(self):
        pass


    #协议的操作部分
    def goip(self,domain):#解析域名到ip
        return reactor.resolve(domain).result

    def startProtocol(self):
        """连接成功后开始发送报文"""
        reactor.callInThread(self.input)

    def printl(self,str):#转换编码
        if os.name == 'nt':
            print str.decode('utf-8').encode("cp936") 

    def cmd(self,cmd):
        cmd = string.split(cmd,'/')
        if cmd[0]=='login':
            defer.succeed(self.login())
        elif cmd[0]=='send':
            if len(cmd) != 3:
                self.printl("输入命令不完整")
            else:
                defer.succeed(self.send(int(cmd[1]),cmd[2]))
        elif cmd[0]=='list':
            self.qq.friend_list.clear()
            defer.succeed(self.get_friend_list(0))
        elif cmd[0]=='online':
            if len(self.qq.friend_list) == 0:
                self.printl("请先用list命令获取你的好友列表。")
            else:
                self.qq.friend_online.clear()
                defer.succeed(self.get_friend_online(0))
        elif cmd[0]=='quit':
            #发送四次
            defer.succeed(self.logout())
            defer.succeed(self.logout())
            defer.succeed(self.logout())
            defer.succeed(self.logout())
            reactor.stop() 
        elif cmd[0]=='help':
            self.printl('login:登陆你的QQ，并将状态更改为上线。')
            self.printl('send/qq号码/内容:向指定号码发送消息。')
            self.printl('list:获取你的好友列表。')
            self.printl('online:获取你的在线好友。')
            self.printl('quit：离线并退出程序。')
            
        else:
            self.printl("不能识别的命令，要获取帮助请使用help命令。")
        reactor.callLater(0, self.input)

    def input(self):
        #获取命令
        cmd = threads.deferToThread(raw_input, "Python-QQ:")
        cmd.addCallback(self.cmd)


def main():
    log=qqlib.initLogging()
    nownum = 0
    lastuid = ''
    getnum = 0
    start = clock()
    if os.name == 'nt':
        qq_id=int(raw_input('请输入你的QQ号码:'.decode('utf-8').encode("cp936")))
        pwd=getpass.getpass('请输入你的QQ密码:'.decode('utf-8').encode("cp936"))
    else:
        qq_id=int(raw_input('请输入你的QQ号码:'))
        pwd=raw_input('请输入你的QQ密码:')
    qq_user=qqlib.qq(qq_id,pwd,log)
    try:
        reactor.listenUDP(0, ConsoleProtocol(qq_user))
        log.info ('Python-QQ开始运行')
    except Exception,ex:
        log.error(ex)
    try:
        reactor.run()
    except:
        log.error('程序运行失败，程序终止，请和作者联系。')
    log.info( "收到 %d 条", getnum)
    log.info("用时：%.2f 秒", (clock()-start))
    log.info("每秒：%f条", (nownum / (clock()-start)))

if __name__ == "__main__":
    main()
