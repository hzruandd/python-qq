# -*- coding: cp936 -*-

"""
本段程序来源于compass，你可以到这里了解更多：
http://wiki.woodpecker.org.cn/moin/Compass
原作者:HD<mailto:hdcola@gmail.com>
修改：梅劲松
"""

from qq.protocols import byteprotocol
from qq.message import qqmsg
from twisted.internet import reactor

class qqProtocol(byteprotocol.ByteMessageProtocol):
    """缺省qq协议实现"""
    def MessageReceived(self,packet):
        """接收到一条消息，对该消息进行处理"""
        message = qqmsg.qqMessage()
        message.loadMessage(packet)
        # print message
        self.MessageProcess(message)

    def MessageProcess(self, message):
        """调用指定的方法来处理收到的消息"""
        method = getattr(self , "on_%s" % message.msgname, None)
        return method(message)

class qqClientQueueProtocol(qqProtocol):
    """使用滑动窗口队列的qq协议客户端实现"""

    def MessageReceived(self,packet):
        """接收到一条消息，确定该消息是否是已发送出的消息，
        如果是，从发送消息队列中清除该消息。然后按正常的流程执行下去。
        """
        message = qqmsg.inqqMessage(self.qq)
        message.loadMessage(packet)
        # print message
        # 将发出的消息从队列中清楚,当没有在已发送列表中，则加入到接收列表中
        try:
            self.sendMsg.remove(message.head.sequence)
        except ValueError:
            self.recvMsg.append(int(message.head.sequence))
            
        self.MessageProcess(message)

    def connectionMade(self):
        """连接成功了，就可以启动发送线程了"""
        reactor.callInThread(self.sendQueueMesg)

    def sendDataToQueue(self, message):
        """将消息加入待发送队列"""
        if(not self.sendQueue.full()):
            self.sendQueue.put(message)
        else:
            self.call = reactor.callLater(0, self.sendDataToQueue, message)

    def sendQueueMesg(self):
        """将队列中的消息发送出去"""
        if (len(self.sendMsg) < self.WINMAX):
            while (not self.sendQueue.empty()):
                message = self.sendQueue.get()
		#先判断是否是接收到的流水号
                try:
                    self.recvMsg.remove(message.head.sequence)
                except ValueError:
                    # 发送前设置消息的顺序号
                    message.head.sequence = self.sequence
                    # 将已经发送的消息放入已经发送的清单中
                    self.sendMsg.append(self.sequence)
		self.sendData(message.packed())
                self.sequence += 1
		#判断流水号是否大于0xffffffff,大于则清零
		if self.sequence >= 0xffff:
		    self.sequence = 0
                
        self.call = reactor.callLater(0.0001, self.sendQueueMesg)
