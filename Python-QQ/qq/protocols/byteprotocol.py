# -*- coding: cp936 -*-

"""
本段程序来源于compass，你可以到这里了解更多：
http://wiki.woodpecker.org.cn/moin/Compass
原作者:HD<mailto:hdcola@gmail.com>
修改：梅劲松
"""

from twisted.internet import protocol, defer
import struct

class ByteMessageProtocol(protocol.DatagramProtocol):
    """二进制流协议处理抽象类"""
    def __init__(self):
        # 接收消息的缓冲区
        self.buffer = ''

    def datagramReceived(self, data,(host, port)):
        """ 查看并解析PDU(protocol data unit)，
        将消息交给rawMessageReceived来进行处理。
        """
	defer.succeed(self.MessageReceived(data))

    def sendData(self, data):
        """将报文发送出去"""
        self.transport.write(data, self.qq.server)

    def MessageReceived(self,packet):
        """加载二进制流消息，一定要继承本方法"""
        pass
