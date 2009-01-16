# -*- coding: cp936 -*-

from qq.message import qqmsg
from qq.protocols import qqp
from twisted.internet import reactor, protocol, defer, threads
from time import clock
import Queue
import md5
import util,struct,tea

import time

from binascii import b2a_hex, a2b_hex

import basic

import string, sys, logging

# 定义了滑动窗口的大小
WINMAX = 1024

def initLogging ():
    log = logging.getLogger ()
    hldr = logging.FileHandler('Python-QQ.log')
    hldr.setFormatter (logging.Formatter("%(asctime)s 级别:%(levelname)s [程序名称:%(module)s  第%(lineno)d行]   内容：%(message)s"))
    log.addHandler(hldr)
    log.setLevel(logging.NOTSET)
    return log

class qq:
    #建立QQ用户对象
    def __init__(self,id,pwd,log):
        self.id=id
        self.pwd=pwd
        self.initkey=''
        self.md5pwd=''
        #初始化会话密钥，因为使用会话密钥最多，所以这里初始化，用于解密时进行判断。
        self.session=chr(00)*16
        #发送消息id需要变化
        self.session_id = 0
        self.friend_list={}
        self.friend_online={}
        #服务器
        self.server=("61.144.238.145",8000)
        self.log=log
        self.start()
        
    def start(self):
        self.initkey=util.initkey()
        self.md5pwd=md5.new(md5.new(self.pwd).digest()).digest()
        
class qqClientProtocol(qqp.qqClientQueueProtocol):
    """建立一个qq客户机的协议处理"""
    def __init__(self,qq):
        # 滑动窗口的大小
        self.WINMAX = WINMAX
        # 等待发送的报文队列
        self.sendQueue = Queue.Queue(self.WINMAX)
        # 已经发出的报文序列ID
        self.sendMsg = []
        # 已经接受的报文序列ID
        self.recvMsg = []
        # 使用的消息ID
        self.sequence = 1
        #使用qq属性
        self.qq=qq
    
    #服务器来数据包后的操作
    def on_qq_logout(self, message):
        pass

    def on_qq_alive(self, message):
        if message.body.fields['data'][0][0]!= '0':
            print "发送活动维持包失败"

    def on_qq_reg_id_2(self, message):
        pass

    def on_qq_updata_info(self, message):
        pass

    def on_qq_search_user(self, message):
        pass

    def on_qq_get_user_info(self, message):
        pass

    def on_qq_add_friend_auth(self, message):
        pass

    def on_qq_del_friend(self, message):
        pass

    def on_qq_buddy_auth(self, message):
        pass

    def on_qq_chang_status(self, message):
        self.qq.log.info("您当前的状态为：在线")
        #开始每隔1分钟发送一次在线包
        defer.succeed(self.alive())

    def on_qq_reg_id_1(self, message):
        pass

    def on_qq_ack_sys_msg(self, message):
        pass

    def on_qq_send(self, message):
        pass

    def on_qq_recv(self, message):
        #将收到的消息的前16位返回给服务器，表示已经收到消息
        try:
            print self.qq.friend_list[message.body.fields['send_qq']]['name']+':'+\
                message.body.fields['msg_data']
        except KeyError:
            print str(message.body.fields['send_qq'])+':'+\
                message.body.fields['msg_data']
            
            
        send_qq = message.body.fields['send_qq']
        recv_qq = message.body.fields['recv_qq']
        msg_id = message.body.fields['msg_id']
        send_ip = message.body.fields['send_ip']
        #将接受到的流水号发送出去。
        sequence = message.head.sequence
        message = qqmsg.outqqMessage(self.qq)
        message.head.sequence = sequence
        message.setMsgName('qq_recv')
        message.body.setField('send_qq',send_qq)
        message.body.setField('recv_qq',recv_qq)
        message.body.setField('msg_id',msg_id)
        message.body.setField('send_ip',send_ip)
        self.sendDataToQueue(message)

    def on_qq_remove_self(self, message):
        pass

    def on_qq_ask_key(self, message):
        pass

    def on_qq_cell_phone_1(self, message):
        pass

    def on_qq_login(self,message):
        if message.body.fields['status'][0]==1:
            #self.transport.connect(util.ip2string(message.body.fields['ip']),8000)
            self.qq.server=(util.ip2string(message.body.fields['ip']),8000)
            defer.succeed(self.pre_login())
        else:
            if message.body.fields['status'][0]==5:
                print message.body.fields['data'][0]
            else:
                self.qq.session=message.body.fields['session']
                message = qqmsg.outqqMessage(self.qq)
                message.setMsgName('qq_chang_status')
                send_data = str(basic.QQ_status['online'])+basic.QQ_video
                send_data = tea.encrypt(send_data,self.qq.session)
                message.body.setField('data',send_data)
                self.sendDataToQueue(message)

    def on_qq_get_friend_list(self, message):
        if message.body.fields['start'][0]!=65535:
            defer.succeed(self.get_friend_list(message.body.fields['start'][0]))
            self.qq.friend_list.update(message.body.fields['data'].items())

        else:
            self.qq.friend_list.update(message.body.fields['data'].items())
            print "您的好友列表:"
            for i in self.qq.friend_list.keys():
                print str(i)+':'+self.qq.friend_list[i]['name']

    def on_qq_get_friend_online(self, message):
        if message.body.fields['start'][0]!=255:
            defer.succeed(self.get_friend_online(message.body.fields['start'][0]))
            self.qq.friend_online.update(message.body.fields['data'].items())

        else:
            self.qq.friend_online.update(message.body.fields['data'].items())
            print "您的在线好友列表:"
            for i in self.qq.friend_online.keys():
                print str(i)+':'+self.qq.friend_list[i]['name']

    def on_qq_cell_photo_2(self, message):
        pass

    def on_qq_send_sms(self, message):
        pass

    def on_qq_group_cmd(self, message):
        pass

    def on_qq_test(self, message):
        pass

    def on_qq_group_data(self, message):
        pass

    def on_qq_upload_group(self, message):
        pass

    def on_qq_friend_data(self, message):
        pass

    def on_qq_download_group(self, message):
        pass

    def on_qq_level(self, message):
        pass

    def on_qq_cluster_data(self, message):
        pass

    def on_qq_advanced_search(self, message):
        pass

    def on_qq_pre_login(self,message):
        status=message.body.fields['status']
        pre_len=message.body.fields['pre_len']
        pre=message.body.fields['pre']
        if status != 0:
            print '申请登陆令牌错！'
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_login')
        message.body.setField('initkey',self.qq.initkey)
        message.body.setField('md5',tea.encrypt('',self.qq.md5pwd))
        message.body.setField('16_51',a2b_hex(basic.QQ_login_16_51))
        message.body.setField('login_status',chr(basic.QQ_login['normal']))
        message.body.setField('53_68',a2b_hex(basic.QQ_login_53_68))
        message.body.setField('pre_len',chr(pre_len))
        message.body.setField('pre',pre[0])
        message.body.setField('unknown',chr(0x40))
        message.body.setField('login_end',a2b_hex(basic.QQ_login_end))
        message.body.setField('end',(416-len(message.body))*chr(00))
        self.sendDataToQueue(message)

    def on_qq_msg_sys(self, message):
        pass

    def on_qq_friend_chang_status(self, message):
        pass

    #客户端的操作。
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

    def cell_photo_2(self):
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


    def cmd(self,cmd):
        cmd = string.split(cmd,'/')
        if cmd[0]=='login':
            defer.succeed(self.login())
        elif cmd[0]=='send':
            if len(cmd) != 3:
                print "输入命令不完整"
            else:
                defer.succeed(self.send(int(cmd[1]),cmd[2]))
        elif cmd[0]=='list':
            self.qq.friend_list.clear()
            defer.succeed(self.get_friend_list(0))
        elif cmd[0]=='online':
            if len(self.qq.friend_list) == 0:
                print "请先用list命令获取你的好友列表。"
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
            print 'login:登陆你的QQ，并将状态更改为上线。'
            print 'send/qq号码/内容:向指定号码发送消息。'
            print 'list:获取你的好友列表。'
            print 'online:获取你的在线好友。'
            print 'quit：离线并退出程序。'
            
        else:
            print "不能识别的命令，要获取帮助请使用help命令。"
        reactor.callLater(0, self.input)

    def input(self):
        #获取命令
        cmd = threads.deferToThread(raw_input, "Python-QQ:")
        cmd.addCallback(self.cmd)


    
def main():
    log=initLogging()
    nownum = 0
    lastuid = ''
    getnum = 0
    start = clock()
    qq_id=int(raw_input('请输入你的QQ号码:'))
    pwd=raw_input('请输入你的QQ密码:')
    qq_user=qq(qq_id,pwd,log)
    try:
        reactor.listenUDP(0, qqClientProtocol(qq_user))
        log.info ('Python-QQ开始运行')
    except:
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

