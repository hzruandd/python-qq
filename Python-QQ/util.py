# -*- coding: cp936 -*-

"""Python-QQ，常用函数
作者：梅劲松
时间：2005-7-13
"""


from random import randint as _randint

#生成QQ所需要的初始化密钥，用于登陆包。
def initkey():
    i=0
    fills=''
    while i < 16:
        fills = fills + chr(_randint(0, 0xff))
        i += 1
    return fills

#因为QQ返回的ip地址是按照数字表示的，所以需要转换，这里是将数字转换为ip字符串了。
#以下两个相关函数由dejava提供,QQ:18505105
def ip2string( ip ):
    a = (ip & 0xff000000) >> 24
    b = (ip & 0x00ff0000) >> 16
    c = (ip & 0x0000ff00) >> 8
    d = ip & 0x000000ff
    return "%d.%d.%d.%d" % (a,b,c,d)

#这里是将ip字符串转换为数字了。
def string2ip( str ):
    ss = string.split(str,'.')
    ip = 0L
    for s in ss:
        ip = (ip << 8) + string.atoi(s)
    return ip

def getCommandinfo():
    """获取命令信息"""
    return self.commandinfo

def getCommandName(commandid):
    """根据二进制代码获取命令"""
    return commandinfo[commandid]

def getCommandName(sname):
    """根据命令获取二进制代码"""
    return nametoid[name]
