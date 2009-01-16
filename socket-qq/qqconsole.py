# -*- coding: utf-8 -*-

import qqlib

from qq.message import qqmsg
from qq.protocols import byteprotocol
from socket import *
import md5
import util,struct,tea

from binascii import b2a_hex, a2b_hex

import basic

from time import clock

import string, os, getpass, time

class ConsoleProtocol(qqlib.qqClientProtocol):
    def logout(self):
        """
        序号不自动，指定为0xFFFF
        用session key加密的password key
        """
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_logout')
        message.head.sequence=0xffff
        message.body.setField('key',self.qq.md5pwd)
        self.sendData(message)

    def alive(self):
        """
        用户QQ号的字符串形式，其他地方是数字方式。
        """
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_alive')
        message.body.setField('qq',str(self.qq.id))
        self.sendData(message)

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
        self.sendData(message)

    def recv(self, message):
        #将收到的消息的前16位返回给服务器，表示已经收到消息
        if message.body.fields['type'] == '好友消息' or message.body.fields['type'] == '陌生人消息':
            self.printl(message.body.fields['type'])
        try:
            print self.qq.friend_list[message.body.fields['send_qq']]['name']+':'+\
                message.body.fields['msg_data']
        except KeyError:
            print str(message.body.fields['send_qq'])+':'+\
                message.body.fields['msg_data']
        self.send(message.body.fields['send_qq'],'我正在使用www.easiest.cn的挂机服务，你也来吗？'.decode('utf-8').encode("gb2312"))
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
        self.sendData(message)
    
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
        self.sendData(message)

    def get_friend_online(self, start):
        message = qqmsg.outqqMessage(self.qq)
        message.setMsgName('qq_get_friend_online')
        message.body.setField('type', 0x02)
        message.body.setField('start', start)
        message.body.setField('unknown',0)
        message.body.setField('unknown1',0)
        self.sendData(message)

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
        self.sendData(message)

    def msg_sys(self):
        pass

    def friend_chang_status(self):
        pass


    #协议的操作部分

    def printl(self,str):#转换编码
        if os.name == 'nt':
            print str.decode('utf-8').encode("cp936") 


def main():
    log=qqlib.initLogging()
    nownum = 0
    lastuid = ''
    getnum = 0
    start = clock()
    conn=socket(AF_INET, SOCK_DGRAM)
    conn.settimeout(8)
    qq_user=qqlib.qq(422962869,'python',log,conn)
    protocol=ConsoleProtocol(qq_user)
    protocol.pre_login()
    while 1:
        protocol.datagramReceived()
	if qq_user.session != chr(00)*16:
	    time.sleep(1)
	    protocol.alive()

    """try:
        conn=socket(AF_INET, SOCK_DGRAM)
        conn.settimeout(5)
        qq_user=qqlib.qq(422962869,'python',log,conn)
        protocol=ConsoleProtocol(qq_user)
        protocol.pre_login()
	while 1:
		protocol.datagramReceived()
    except Exception,ex:
        log.error(ex)
    log.info( "收到 %d 条", getnum)
    log.info("用时：%.2f 秒", (clock()-start))
    log.info("每秒：%f条", (nownum / (clock()-start)))"""

if __name__ == "__main__":
    main()
