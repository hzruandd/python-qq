# -*- coding: utf-8 -*-

"""
本段程序来源于compass，你可以到这里了解更多：
http://wiki.woodpecker.org.cn/moin/Compass
原作者:HD<mailto:hdcola@gmail.com>
修改：梅劲松
"""

import struct
import tea
import basic
from binascii import b2a_hex, a2b_hex

class ByteMessage:
    """二进制消息基类"""
    
    def __init__(self):
        """初始化一个消息"""
        # 消息头
        # self.head = None
        # 消息体
        # self.body = None
	# 消息尾
	# self.end  = None
        # 消息工具
        # self.msgutilcls = None
        # 当前的消息名称
        # self.msgname = ''
        # 当前协议的名称
        # self.protocolname = ''

    def loadMessage(self, packet):
        """从二进制流中加载出消息对象"""
        # 架载包头
        self.head.loadHead(packet[:len(self.head)])
        self.msgname = basic.commandinfo[self.head.id]
        # 依据消息ID架载包体
        self.body.loadBody(self.msgname, packet[len(self.head):-1])
	self.end.loadEnd(packet[-1:])

    def setMsgName(self, msgname):
        """设置消息名"""
        self.head.setId(basic.nametoid[msgname])
        self.msgname = msgname

    def packed(self):
        """打包消息为二进制流PDU"""
        body = self.body.packed()
        if (body == None):
            return self.head.packed()
        else:
            self.head.setLength(len(self.head) + len(body))
            return self.head.packed() + body + self.end.packed()

    def __str__(self):
        """字符串化"""
        return str(self.head) + '\n' + str(self.body)+ '\n' + str(self.end)

class inByteMessageHead:
    """二进制消息的消息头抽像类"""
    def __init__(self, parent):
        # 头
        self.packhead = basic.QQ_02_head
	# 版本
	self.ver = basic.QQ_ver
        # 命令ID
        self.id = 0
        # 序列号
        self.sequence = 0
        # 他爹
        self.parent = parent

    def __len__(self):
        """包头定长7"""
        return basic.QQ_02_in_head_len

    def setId(self,id):
        """设置命令ID"""
        self.id = id

    def setSequence(self,sequence):
        """设置发送序列"""
        self.sequence = sequence

    def setLength(self, length):
        """包的整长"""
        self.length = length

    def loadHead(self, header):
        """转换一个PDU (protocol data unit)到一个消息头
        消息头的格式为包头(1字节)、版本（2字节）、命令ID（2字节）、流水号（2字节），共7字节长度
        """
        self.packhead,self.ver,self.id,self.sequence = struct.unpack('>BHHH', header)
    
    def packed(self):
        """转换一个消息头为二进制流
        消息头的格式为包头(1字节)、版本（2字节）、命令ID（2字节）、流水号（2字节），共7字节长度
        """
        return struct.pack('>BHHH', self.packhead, self.ver,self.id, self.sequence)
    def __str__(self):
        """字符串化"""
        plist = []
        plist.append("包头:%s" % self.packhead)
	plist.append("版本:%s" % self.ver)
        plist.append("命令ID：%s" % self.id)
        plist.append("消息序列号：%s" % self.sequence)
        return reduce(lambda x,y: x + "\n" + y, plist)

class outByteMessageHead:
    """二进制消息的消息头抽像类"""
    def __init__(self, parent, qq):
        # 头
        self.packhead = basic.QQ_02_head
	# 版本
	self.ver = basic.QQ_ver
        # 命令ID
        self.id = 0
        # 序列号
        self.sequence = 0
        # QQ号码
        self.qq_id = 0
        # 他爹
        self.parent = parent
        #继承QQ用户信息
        self.qq=qq

    def __len__(self):
        """包头定长7"""
        return basic.QQ_02_out_head_len

    def setId(self,id):
        """设置命令ID"""
        self.id = id

    def setSequence(self,sequence):
        """设置发送序列"""
        self.sequence = sequence

    def setLength(self, length):
        """包的整长"""
        self.length = length

    def loadHead(self, header):
        """转换一个PDU (protocol data unit)到一个消息头
        消息头的格式为包头(1字节)、版本（2字节）、命令ID（2字节）、流水号（2字节）、用户QQ号码，共11字节长度
        """
        self.packhead,self.ver,self.id,self.sequence,self.qq_id = struct.unpack('>BHHHI', header)
    
    def packed(self):
        """转换一个消息头为二进制流
        消息头的格式为包头(1字节)、版本（2字节）、命令ID（2字节）、流水号（2字节）、用户QQ号码，共11字节长度
        """
        return struct.pack('>BHHHI', self.packhead, self.ver,self.id, self.sequence, self.qq.id)
    
    def __str__(self):
        """字符串化"""
        plist = []
        plist.append("包头:%s" % self.packhead)
	plist.append("版本:%s" % self.ver)
        plist.append("命令ID：%s" % self.id)
        plist.append("消息序列号：%s" % self.sequence)
        plist.append("用户QQ号:%s" % self.qq_id)
        return reduce(lambda x,y: x + "\n" + y, plist)

class ByteMessageBody:
    """二进制报文的消息体抽像类"""
    def __init__(self, parent,qq):
        # 消息的内容
        self.fields = {}
        self.setField = self.fields.__setitem__
        # 他爹
        self.parent = parent
	#使用qq用户信息
	self.qq=qq

    def loadBody(self, msgname, packet):
        """转换一个二进制流为消息体"""
        # 找到解包的方法
        method = getattr(self.parent , "unpack_%s" %(msgname), None)
        #除了申请令牌包外，其他所有包解密
        if msgname!='qq_pre_login':
            msg=tea.decrypt(packet,self.qq.session)
            if msg == None:
                msg=tea.decrypt(packet,self.qq.md5pwd)
                if msg == None:
                    msg=tea.decrypt(packet,self.qq.initkey)
            packet=msg
        method(packet)
        self.conversionString()
    
    def packed(self):
        """转换消息体为二进制流"""
        # 找到打包方法
        method = getattr(self.parent , "pack_%s" %(self.parent.msgname), None)
        send_msg = method(self.fields)
        if self.parent.msgname == 'qq_pre_login':
            return send_msg
        if self.parent.msgname == 'qq_login':
            return send_msg[:16]+tea.encrypt(send_msg[16:],self.qq.initkey)
        return tea.encrypt(send_msg,self.qq.session)

    def conversionString(self):
        """去除fileds中字符串中的\x00"""
        for field in self.fields.keys():
            if ( isinstance(self.fields[field],str) ):
                index = self.fields[field].find('\0')
                if index > -1:
                    self.fields[field] = self.fields[field][:index]

    def __str__(self):
        """字符串化"""
        if len(self.fields) > 0:
            plist = []
            for field in self.fields.keys():
                plist.append(str(field) + "："  + str(self.fields[field]))
            return reduce(lambda x,y: x + "\n" + y, plist)
        else:
            return ""

    def __len__(self):
        """消息体长度"""
        if len(self.fields) > 0:
            fields_len = 0
            for field in self.fields.keys():
                fields_len += len(str(self.fields[field]))
            return fields_len
        

class ByteMessageEnd:
    """二进制报文的消息尾抽像类"""
    def __init__(self, parent):
        # 包尾
        self.end = 3
    def packed(self):
        """转换一个消息尾为二进制流"""
        return struct.pack('>B',self.end)
    def loadEnd(self,end):
	"""转换一个消息尾"""
        self.end = struct.unpack('>B', end)
