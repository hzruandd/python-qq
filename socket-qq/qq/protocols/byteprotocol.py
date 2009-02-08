# -*- coding: utf-8 -*-

"""
本段程序来源于compass，你可以到这里了解更多：
http://wiki.woodpecker.org.cn/moin/Compass
原作者:HD<mailto:hdcola@gmail.com>
修改：梅劲松
"""

from qq.message import qqmsg
from socket import *
import struct,sys

class ByteMessageProtocol(socket):
    """二进制流协议处理抽象类"""

    def MessageProcess(self, message):
        """调用指定的方法来处理收到的消息"""
        method = getattr(self , "on_%s" % message.msgname, None)
        return method(message)

    def datagramReceived(self):
        """ 查看并解析PDU(protocol data unit)，
        将消息交给rawMessageReceived来进行处理。
        """
        try:
            packet = self.qq.conn.recvfrom(1024)[0]
            message = qqmsg.inqqMessage(self.qq)
            message.loadMessage(packet)
            self.MessageProcess(message)
        except:
            self.printl ('网络中断或已失去活动的网络连接，请重新登陆')
            sys.exit(1)

    def sendData(self, data):
        """将报文发送出去"""
        self.qq.conn.sendto(data.packed(), self.qq.server)
