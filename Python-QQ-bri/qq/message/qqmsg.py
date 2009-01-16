# -*- coding: utf-8 -*-

"""
本段程序来源于compass，你可以到这里了解更多：
http://wiki.woodpecker.org.cn/moin/Compass
原作者:HD<mailto:hdcola@gmail.com>
修改：梅劲松
"""

from qq.message import bytemsg
import struct
from binascii import b2a_hex, a2b_hex
import util
import basic

class inqqMessage(bytemsg.ByteMessage):
    """qq 消息基类"""
    def __init__(self,qq):
        # 消息头
        self.head = bytemsg.inByteMessageHead(self)
        # 消息体
        self.body = bytemsg.ByteMessageBody(self,qq)
	# 消息尾
	self.end  = bytemsg.ByteMessageEnd(self)
        # 消息工具
        self.msgutilcls = util
        # 协议名称
        self.protocolname = 'qq'
        # 当前的消息名称
        self.msgname = ''
        #使用qq用户信息
        self.qq=qq

    def unpack_qq_logout(self, packet):
        """Logout请求包，这个包没有服务器的应答"""
        pass

    def unpack_qq_alive(self, packet):
        self.body.fields['data']=\
            struct.unpack('>'+str(len(packet))+'s',packet)

    def unpack_qq_reg_id_2(self, packet):
        pass

    def unpack_qq_updata_info(self, packet):
        pass

    def unpack_qq_search_user(self, packet):
        pass

    def unpack_qq_get_user_info(self, packet):
        pass

    def unpack_qq_add_friend_auth(self, packet):
        pass

    def unpack_qq_del_friend(self, packet):
        pass

    def unpack_qq_buddy_auth(self, packet):
        pass

    def unpack_qq_chang_status(self, packet):
        self.body.fields['status']=\
            struct.unpack(str(len(packet))+'s',packet)

    def unpack_qq_reg_id_1(self, packet):
        pass

    def unpack_qq_ack_sys_msg(self, packet):
        pass

    def unpack_qq_send(self, packet):
        self.body.fields['status']=\
            struct.unpack(str(len(packet))+'s',packet)
        
    def unpack_qq_recv(self, packet):
        self.body.fields['send_qq'],\
            self.body.fields['recv_qq'],\
            self.body.fields['msg_id'],\
            self.body.fields['send_ip'],\
            self.body.fields['send_port'],\
            self.body.fields['type']=\
            struct.unpack('>IIIIHH',packet[0:20])
        #好友消息
        if self.body.fields['type'] == 9:
            self.body.fields['type'] = basic.msg_type[0x0009L]
            self.body.fields['send_ver'],\
                self.body.fields['send_qq1'],\
                self.body.fields['recv_qq2'],\
                self.body.fields['msg_md5'],\
                self.body.fields['type1'],\
                self.body.fields['session_id'],\
                self.body.fields['send_time'],\
                self.body.fields['unknown'],\
                self.body.fields['send_face'],\
                self.body.fields['send_font'],\
                self.body.fields['msg_pass'],\
                self.body.fields['pass_id'],\
                self.body.fields['msg_id1'],\
                self.body.fields['msg_type'],\
                self.body.fields['msg_data'],\
                self.body.fields['msg_link'],\
                self.body.fields['msg_end'],\
                self.body.fields['msg_red'],\
                self.body.fields['msg_green'],\
                self.body.fields['msg_blue'],\
                self.body.fields['unknown1'],\
                self.body.fields['encoding'],\
                self.body.fields['info'],\
                self.body.fields['len']=\
                struct.unpack('>HII16sHHIBBIBBHB'+str(len(packet)-65-14)+'s'+'2sBBBBBH4sB',packet[20:])
        #陌生人消息
        elif self.body.fields['type'] == 10:
            self.body.fields['type'] = basic.msg_type[0x000AL]
            self.body.fields['send_ver'],\
                self.body.fields['send_qq1'],\
                self.body.fields['recv_qq2'],\
                self.body.fields['msg_md5'],\
                self.body.fields['type1'],\
                self.body.fields['session_id'],\
                self.body.fields['send_time'],\
                self.body.fields['unknown'],\
                self.body.fields['send_face'],\
                self.body.fields['send_font'],\
                self.body.fields['msg_pass'],\
                self.body.fields['pass_id'],\
                self.body.fields['msg_id1'],\
                self.body.fields['msg_type'],\
                self.body.fields['msg_data'],\
                self.body.fields['msg_link'],\
                self.body.fields['msg_end'],\
                self.body.fields['msg_red'],\
                self.body.fields['msg_green'],\
                self.body.fields['msg_blue'],\
                self.body.fields['unknown1'],\
                self.body.fields['encoding'],\
                self.body.fields['info'],\
                self.body.fields['len']=\
                struct.unpack('>H'+str(len(packet)-65-14)+'s'+'2sBBBBBH4sB',packet[20:])
        #手机短消息普通用户
        elif self.body.fields['type'] == 11:
            self.body.fields['type'] = basic.msg_type[0x000BL]
        #手机短消息移动QQ用户
        elif self.body.fields['type'] == 0x0013L:
            self.body.fields['type'] = basic.msg_type[0x0013L]
        #未知类型的群消息
        elif self.body.fields['type'] == 0x0020L:
            self.body.fields['type'] = basic.msg_type[0x0020L]
        #加入到群
        elif self.body.fields['type'] == 0x0021L:
            self.body.fields['type'] = basic.msg_type[0x0021L]
        #被踢出群
        elif self.body.fields['type'] == 0x0022L:
            self.body.fields['type'] = basic.msg_type[0x0022L]
        #请求加入群
        elif self.body.fields['type'] == 0x0023L:
            self.body.fields['type'] = basic.msg_type[0x0023L]
        #同意加入群
        elif self.body.fields['type'] == 0x0024L:
            self.body.fields['type'] = basic.msg_type[0x0024L]
        #拒绝对方加入群
        elif self.body.fields['type'] == 0x0025L :
            self.body.fields['type'] = basic.msg_type[0x0025L]
        #加入到群在创建时被加
        elif self.body.fields['type'] == 0x0026L :
            self.body.fields['type'] = basic.msg_type[0x0026L]
        #临时群消息
        elif self.body.fields['type'] == 0x002AL :
            self.body.fields['type'] = basic.msg_type[0x002AL]
        #固定群消息
        elif self.body.fields['type'] == 0x002BL :
            self.body.fields['type'] = basic.msg_type[0x002BL]
            self.body.fields['group_id'],\
                self.body.fields['group_type'],\
                self.body.fields['send_qq1'],\
                self.body.fields['unknown'],\
                self.body.fields['msg_sq'],\
                self.body.fields['time'],\
                self.body.fields['ver_id'],\
                self.body.fields['len'],\
                self.body.fields['con_type'],\
                self.body.fields['msg_pass'],\
                self.body.fields['msg_pass_id'],\
                self.body.fields['msg_id1'],\
                self.body.fields['unknown1']=\
                struct.unpack('>IBIHHIIHHBBHI',packet[20:53])
            self.body.fields['msg_data']=\
                struct.unpack('>'+str(self.body.fields['len']-10-13)+'s',packet[53:53+self.body.fields['len']-10-13])                
                
        #系统消息
        elif self.body.fields['type'] == 0x0030L :
            self.body.fields['type'] = basic.msg_type[0x0030L]
        #同一个QQ号在其他地方登录
        elif self.body.fields['type'] == 0x01L :
            self.body.fields['type'] = basic.msg_type[0x01L]
            

    def unpack_qq_remove_self(self, packet):
        pass

    def unpack_qq_ask_key(self, packet):
        pass

    def unpack_qq_cell_phone_1(self, packet):
        pass

    def unpack_qq_login(self, packet):
        """login报文解包"""
        self.body.fields['status']=struct.unpack('B',packet[0])
	if self.body.fields['status'][0]==0:
            #返回登陆包
            self.body.fields['session'],\
                self.body.fields['qq_id'],\
                self.body.fields['user_ip'],\
                self.body.fields['user_port'],\
                self.body.fields['server_id'],\
                self.body.fields['server_port'],\
                self.body.fields['login_time'],\
                self.body.fields['unknown'],\
                self.body.fields['unknown1'],\
                self.body.fields['unknown2'],\
                self.body.fields['unknown3'],\
                self.body.fields['unknown4'],\
                self.body.fields['unknown5'],\
                self.body.fields['unknown6'],\
                self.body.fields['client_key'],\
                self.body.fields['unknown7'],\
                self.body.fields['up_ip'],\
                self.body.fields['up_time'],\
                self.body.fields['unknown8']=\
                struct.unpack('>16sIIHIHI26sIHIH2s2s32s12sII8s',packet[1:139])
        if self.body.fields['status'][0]==1:
            #返回重定向包
            self.body.fields['qq_id'],\
                self.body.fields['ip'],\
                self.body.fields['port']=\
                struct.unpack('>IIH',packet[1:13])
	if self.body.fields['status'][0]== 5:
	    #密码错误
	    self.body.fields['data']=\
		struct.unpack(str(len(packet)-1)+'s',packet[1:])
	    
    def unpack_qq_get_friend_list(self, packet):
        self.body.fields['start']=\
            struct.unpack('>H',packet[:2])
        packet = packet[2:]
        i=0
        qq_list={}
        while len(packet) != 0:
            p=struct.unpack('>I',packet[:4])[0]
            qq_list[p]={}
            qq_list[p]['face']=struct.unpack('>H',packet[4:6])[0]
            qq_list[p]['age']=struct.unpack('>B',packet[6:7])[0]
            qq_list[p]['sex']=struct.unpack('>B',packet[7:8])[0]
            qq_list[p]['namelen']=struct.unpack('>B',packet[8:9])[0]
            namelen=qq_list[p]['namelen']
            qq_list[p]['name']=struct.unpack('>'+str(namelen)+'s',packet[9:9+int(namelen)])[0]
            qq_list[p]['unknown']=struct.unpack('>H',packet[9+int(namelen):9+int(namelen)+2])[0]
            qq_list[p]['show']=struct.unpack('>B',packet[9+int(namelen)+2:9+int(namelen)+3])[0]
            qq_list[p]['flag']=struct.unpack('>B',packet[9+int(namelen)+3:9+int(namelen)+4])[0]
            packet=packet[9+int(namelen)+4:]
        self.body.fields['data']=qq_list

    def unpack_qq_get_friend_online(self, packet):
        self.body.fields['start']=\
            struct.unpack('>B',packet[:1])
        packet = packet[1:]
        i=0
        qq_list={}
        while len(packet) != 0:
            p=struct.unpack('>I',packet[:4])[0]
            qq_list[p]={}
            qq_list[p]['unknown']=struct.unpack('>B',packet[4:5])[0]
            qq_list[p]['ip']=struct.unpack('>I',packet[5:9])[0]
            qq_list[p]['port']=struct.unpack('>H',packet[9:11])[0]
            qq_list[p]['unknown1']=struct.unpack('>B',packet[11:12])[0]
            qq_list[p]['state']=struct.unpack('>B',packet[12:13])[0]
            qq_list[p]['unknown2']=struct.unpack('>H',packet[13:15])[0]
            qq_list[p]['key']=struct.unpack('>16s',packet[15:31])[0]
            qq_list[p]['unknown3']=struct.unpack('>H',packet[31:33])[0]
            qq_list[p]['show']=struct.unpack('>B',packet[33:34])[0]
            qq_list[p]['flag']=struct.unpack('>B',packet[34:35])[0]
            qq_list[p]['unknown4']=struct.unpack('>H',packet[35:37])[0]
            qq_list[p]['unknown5']=struct.unpack('>B',packet[37:38])[0]
            packet=packet[38:]
        self.body.fields['data']=qq_list	    

    def unpack_qq_cell_phone_2(self, packet):
        pass

    def unpack_qq_send_sms(self, packet):
        pass

    def unpack_qq_group_cmd(self, packet):
        self.body.fields['type']=\
            struct.unpack('>B',packet[:1])
        #发送群消息的返回包
        if self.body.fields['type'][0]==basic.GROUP_cmd['send']:
            self.body.fields['status'],\
                self.body.fields['id']=\
                struct.unpack('>BI',packet[1:])

    def unpack_qq_test(self, packet):
        pass

    def unpack_qq_group_data(self, packet):
        pass

    def unpack_qq_upload_group(self, packet):
        pass

    def unpack_qq_friend_data(self, packet):
        pass

    def unpack_qq_download_group(self, packet):
        pass

    def unpack_qq_level(self, packet):
        pass

    def unpack_qq_cluster_data(self, packet):
        pass

    def unpack_qq_advanced_search(self, packet):
        pass

    def unpack_qq_pre_login(self, packet):
        """pre_login报文解包"""
        self.body.fields['status'], \
            self.body.fields['pre_len']=\
            struct.unpack('BB',packet[:2])
        self.body.fields['pre']=\
	    struct.unpack(str(self.body.fields['pre_len'])+'s',packet[2:])

    def unpack_qq_msg_sys(self, packet):
        pass

    def unpack_qq_friend_chang_status(self, packet):
        pass

            
class outqqMessage(bytemsg.ByteMessage):
    """qq 消息基类"""
    def __init__(self,qq):
        # 消息头
        self.head = bytemsg.outByteMessageHead(self,qq)
        # 消息体
        self.body = bytemsg.ByteMessageBody(self,qq)
	# 消息尾
	self.end  = bytemsg.ByteMessageEnd(self)
        # 消息工具
        self.msgutilcls = util
        # 协议名称
        self.protocolname = 'qq'
        # 当前的消息名称
        self.msgname = ''
        #使用qq用户信息
        self.qq=qq

    def pack_qq_logout(self, fields):
        return struct.pack('>'+str(len(fields['key']))+'s',
                fields['key']
                )

    def pack_qq_alive(self, fields):
        return struct.pack('>'+str(len(fields['qq']))+'s',
                fields['qq']
                )

    def pack_qq_reg_id_2(self, fields):
        pass

    def pack_qq_updata_info(self, fields):
        pass

    def pack_qq_search_user(self, fields):
        pass

    def pack_qq_get_user_info(self, fields):
        pass

    def pack_qq_add_friend_auth(self, fields):
        pass

    def pack_qq_del_friend(self, fields):
        pass

    def pack_qq_buddy_auth(self, fields):
        pass

    def pack_qq_chang_status(self,fields):
        return struct.pack('>BI',
		fields['online'],
                fields['video']           
                )

    def pack_qq_reg_id_1(self, fields):
        pass

    def pack_qq_ack_sys_msg(self, fields):
        pass

    def pack_qq_send(self,fields):
        return struct.pack('>IIHII16sHHIHIHHB'+str(len(fields['msg_data']))+'s'+\
                '2sBBBBBH4sB',
		fields['send_qq'],
                fields['recv_qq'],
                fields['ver'],
                fields['send_qq1'],
                fields['recv_qq1'],
                fields['md5'],
                fields['type'],
                fields['session_id'],
                fields['send_time'],
                fields['send_face'],
                fields['font_info'],
                fields['msg_pass'],
                fields['msg_id'],
                fields['msg_type'],
                fields['msg_data'],
                fields['msg_link'],
                fields['msg_end'],
                fields['msg_red'],
                fields['msg_green'],
                fields['msg_blue'],
                fields['unknown'],
                fields['encoding'],
                fields['info'],
                fields['len']
                )

    def pack_qq_recv(self,fields):
        return struct.pack('>IIII',
                fields['send_qq'],
                fields['recv_qq'],
                fields['msg_id'],
                fields['send_ip']
                )
    
    def pack_qq_remove_self(self, fields):
        pass

    def pack_qq_ask_key(self, fields):
        pass

    def pack_qq_cell_phone_1(self, fields):
        pass

    def pack_qq_login(self, fields):
        """login报文打包"""
        return struct.pack('>16s16s36ss16ss'+str(ord(fields['pre_len']))+'ss94s'+str(len(fields['end']))+'s',
                fields['initkey'],
                fields['md5'],
                fields['16_51'],
                fields['login_status'],
                fields['53_68'],
                fields['pre_len'],
                fields['pre'],
                fields['unknown'],
                fields['login_end'],
                fields['end'],
                )

    def pack_qq_get_friend_list(self, fields):
        return struct.pack('>HB',
                fields['start'],
                fields['sorted']
                )
    
    def pack_qq_get_friend_online(self, fields):
        return struct.pack('>BBBH',
                fields['type'],
                fields['start'],
                fields['unknown'],
                fields['unknown1']
                )

    def pack_qq_cell_phone_2(self, fields):
        pass

    def pack_qq_send_sms(self, fields):
        pass

    def pack_qq_group_cmd(self, fields):
        struct.pack('>BIH'+str(len(fields['msg_data']))+'s'+\
                '2sBBBBBH4s',
                fields['cmd_type'],
                fields['recv_group'],
                fields['len'],
                fields['msg_data'],
                fields['msg_link'],
                fields['msg_end'],
                fields['msg_red'],
                fields['msg_green'],
                fields['msg_blue'],
                fields['unknown'],
                fields['encoding'],
                fields['info']
                )
        return struct.pack('>BIH'+str(len(fields['msg_data']))+'s'+\
                '2sBBBBBH4sB',
                fields['cmd_type'],
                fields['recv_group'],
                fields['len'],
                fields['msg_data'],
                fields['msg_link'],
                fields['msg_end'],
                fields['msg_red'],
                fields['msg_green'],
                fields['msg_blue'],
                fields['unknown'],
                fields['encoding'],
                fields['info'],
                fields['end_len']
                )

    def pack_qq_test(self, fields):
        pass

    def pack_qq_group_data(self, fields):
        pass

    def pack_qq_upload_group(self, fields):
        pass

    def pack_qq_friend_data(self, fields):
        pass

    def pack_qq_download_group(self, fields):
        pass

    def pack_qq_level(self, fields):
        pass

    def pack_qq_cluster_data(self, fields):
        pass

    def pack_qq_advanced_search(self, fields):
        pass

    def pack_qq_pre_login(self, fields):
        """pre_login报文打包"""
        return struct.pack('>B',
                fields['unknown']
                )

    def pack_qq_msg_sys(self, fields):
        pass

    def pack_qq_friend_chang_status(self, fields):
        pass
