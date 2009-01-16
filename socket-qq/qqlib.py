# -*- coding: utf-8 -*-

from qq.message import qqmsg
from qq.protocols import qqp
from twisted.internet import reactor, protocol, defer, threads
import Queue
import md5
import util,struct,tea

from binascii import b2a_hex, a2b_hex

import basic

import string, sys, logging

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
        #是否登陆成功，1为成功
        self.login=0
        self.friend_list={}
        self.friend_online={}
        #服务器，这里是个根服务器，将会根据重定向包来决定真正登陆的服务器的IP地址
        self.server=("219.133.40.216",8000)
        self.log=log
        self.start()
        
    def start(self):
        self.initkey=util.initkey()
        self.md5pwd=md5.new(md5.new(self.pwd).digest()).digest()
        
class qqClientProtocol(qqp.qqClientQueueProtocol):
    """建立一个qq客户机的协议处理"""
    def __init__(self,qq):
        # 滑动窗口的大小
        self.WINMAX = 1024
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
        '''
        到这里登陆过程的自动处理完成，开始循环发送活动包，表示自己在线。
        '''
        self.qq.log.info("您当前的状态为：在线")
        #开始每隔1分钟发送一次在线包
        defer.succeed(self.alive())

    def on_qq_reg_id_1(self, message):
        pass

    def on_qq_ack_sys_msg(self, message):
        pass

    def on_qq_send(self, message):
        '''
        当发送消息后，服务器返回的包中，状态不等于00，则没有发送成功。
        '''
        self.send_replay(message)

    def on_qq_recv(self, message):
        self.recv(message)

    def on_qq_remove_self(self, message):
        pass

    def on_qq_ask_key(self, message):
        pass

    def on_qq_cell_phone_1(self, message):
        pass

    def on_qq_login(self,message):
        '''
        这个也是登陆过程中自动处理的一部分，当登陆成功后，self.qq.login这个属性为1，否则则没有登陆成功。
        调用了lib后可以通过这个属性来判断是否登陆成功。
        '''
        if message.body.fields['status'][0]==1:
            #self.transport.connect(util.ip2string(message.body.fields['ip']),8000)
            self.qq.server=(util.ip2string(message.body.fields['ip']),8000)
            defer.succeed(self.pre_login())
        else:
            if message.body.fields['status'][0]==5:
                print message.body.fields['data'][0]
            else:
                self.printl('登陆成功')
                self.qq.login = 1
                self.qq.session=message.body.fields['session']
                message = qqmsg.outqqMessage(self.qq)
                message.setMsgName('qq_chang_status')
                message.body.setField('online',basic.QQ_status['online'])
                message.body.setField('video',basic.QQ_video)
                self.sendDataToQueue(message)

    def on_qq_get_friend_list(self, message):
        '''
        获取好友列表，根据是否还有下一页来判断，是否继续取好友列表。
        '''
        if message.body.fields['start'][0]!=65535:
            defer.succeed(self.get_friend_list(message.body.fields['start'][0]))
            self.qq.friend_list.update(message.body.fields['data'])

        else:
            self.qq.friend_list.update(message.body.fields['data'])
            print "您的好友列表:"
            for i in self.qq.friend_list.keys():
                print str(i)+':'+self.qq.friend_list[i]['name']

    def on_qq_get_friend_online(self, message):
        '''
        获取在线好友列表，根据是否还有下一页来判断，是否继续取在线好友列表。
        '''
        if message.body.fields['start'][0]!=255:
            defer.succeed(self.get_friend_online(message.body.fields['start'][0]))
            self.qq.friend_online.update(message.body.fields['data'])

        else:
            self.qq.friend_online.update(message.body.fields['data'])
            print "您的在线好友列表:"
            for i in self.qq.friend_online.keys():
                print str(i)+':'+self.qq.friend_list[i]['name']

    def on_qq_cell_phone_2(self, message):
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
        '''
        当收到登陆令牌后，判断令牌是否正确。
        然后发送qq_login的报文开始登陆。
        由于这个部分是自动处理的，所以当发送登陆令牌请求包后，会自动工作到改变在线状态为止。
        '''
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



    


