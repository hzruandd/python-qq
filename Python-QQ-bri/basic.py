# -*- coding: utf-8 -*-

"""Python-QQ，本库中命令码以及包结构，部分来源于OpenQQ、LumaQQ、以及其他网络上的开源资料，部分来源于自己分析。
特别声明：本协议结构分析过程中，没有对腾讯公司的QQ软件进行反编译和其他类似手段取得协议结构。本协议本身只也用于研究
和学习，在法律角度上并没有对深圳腾讯公司造成侵害。
作者：梅劲松
时间：2005-7-13
本文件为Python_QQ基本变量的定义。"""
"""目前只考虑了基本命令部分，没有考虑文件传输，群命令等操作"""


#02为包头的命令码定义
commandinfo = {
    0x0001L : 'qq_logout',                # 退出登陆
    0x0002L : 'qq_alive',                 # 保持自己的在线状态
    0x0003L : 'qq_reg_id_2',              # 注册新ID2
    0x0004L : 'qq_updata_info',           # 更新自己信息
    0x0005L : 'qq_search_user',           # 查找用户
    0x0006L : 'qq_get_user_info',         # 获取好友信息
    0x0009L : 'qq_add_friend_auth',       # 加好友验证
    0x000aL : 'qq_del_friend',            # 删除好友
    0x000bL : 'qq_buddy_auth',            # 发送验证消息
    0x000dL : 'qq_chang_status',          # 改变在线状态
    0x0011L : 'qq_reg_id_1',              # 注册新ID1
    0x0012L : 'qq_ack_sys_msg',           # 确认收到了系统消息
    0x0016L : 'qq_send',                  # 发送消息
    0x0017L : 'qq_recv',                  # 接收消息
    0x001cL : 'qq_remove_self',           # 把自己从对方好友列表中删除
    0x001dL : 'qq_ask_key',               # 请求文件中转和视频等的密钥
    0x0021L : 'qq_cell_phone_1',          # cell phone 1
    0x0022L : 'qq_login',                 # 登陆
    0x0026L : 'qq_get_friend_list',       # 获取好友列表
    0x0027L : 'qq_get_friend_online',     # 获取在线好友
    0x0029L : 'qq_cell_photo_2',          # cell phone 2
    0x002dL : 'qq_send_sms',              # 发送短消息
    0x0030L : 'qq_group_cmd',             # 群命令
    0x0031L : 'qq_test',                  # 连接测试
    0x003cL : 'qq_group_data',            # 分组操作
    0x003dL : 'qq_upload_group',          # 上传分组信息
    0x003eL : 'qq_friend_data',           # 好友相关数据操作
    0x0058L : 'qq_download_group',        # 下载分组信息
    0x005cL : 'qq_level',                 # 好友等级信息
    0x005fL : 'qq_cluster_data',          # 群数据操作
    0x0061L : 'qq_advanced_search',       # 高级查找
    0x0062L : 'qq_pre_login',             # 申请登录码
    0x0066L : 'qq_tmp_op',                # 临时会话操作
    0x0080L : 'qq_msg_sys',               # 接受系统消息
    0x0081L : 'qq_friend_chang_status'    # 好友改变状态 
    }

msg_type = {
    9 : '好友消息',
    10 : '陌生人消息',
    11 : '手机短消息普通用户',
    0x0013L : '手机短消息移动QQ用户',
    0x001FL : '临时会话',
    0x0020L : '未知类型的群消息',
    0x0021L : '加入到群',
    0x0022L : '被踢出群',
    0x0023L : '请求加入群',
    0x0024L : '同意加入群',
    0x0025L : '拒绝对方加入群',
    0x0026L : '加入到群在创建时被加',
    0x002AL : '临时群消息',
    0x002BL : '固定群消息',
    0x0030L : '系统消息',
    0x01L : '同一个QQ号在其他地方登录'
    }

# 通过名称查出消息ID的命令码，反转一次就可以了。
nametoid = {}
for k in commandinfo.keys():
    nametoid[commandinfo[k]] = k
#所模拟的客户端版本号
QQ_ver=0x0e1b
#不需要返回确认包的发送次数,比如退出登录的报文
QQ_send_unknown=4
#QQ服务器端的端口号码
QQ_server_port=8000
#QQ默认文字编码方式
QQ_encoding="GBK"
#在线状态维持包发送时间间隔,单位秒
QQ_ative=500

#02为包头的协议包含了QQ的决大部分功能，以下为02为包头数据包的基本数据

#包头为0x02
QQ_02_head=0x02
#包尾为0x03
QQ_02_end=0x03
#服务器发送到客户端的包头长度，其中依次包括：包头、版本、命令码、流水号
QQ_02_in_head_len=7
#客户端发送到服务器的包头长度，其中依次包括：包头、版本、命令码、流水号、用户的QQ号码
QQ_02_out_head_len=11
#服务器和客户端发送的包尾长度
QQ_02_end_len = 1
#QQ登录包中从16到51字节的内容是固定的。
QQ_login_16_51='0000000000000000000000000000000000000086CC4C352CD3736C14F6F6AFC3FA33A401'
#QQ登陆包中从53到68之间为固定值
QQ_login_53_68='8D8BFAECD552174A86F9A775E632D16D'
#QQ登陆包中从登录码后固定内容的值
QQ_login_end='0B04020001000000000003090000000000000001E90301000000000001F30300000000000001ED0300000000000001EC0300000000000003050000000000000003070000000000000001EE0300000000000001EF0300000000000001EB03000000000000'
#登陆状态
#依次为:正常登陆、隐身登陆
QQ_login={'normal':0x0A, 'hidden':0x28}

#在线状态
#依次为:在线、离线、离开、隐身
QQ_status = {'online':0x0a, 'offline':0x14, 'away':0x1e, 'hidden':0x28}

#登陆时显示有视频头
QQ_video = 0x0001

#获取好友列表的时候进行排序
QQ_friend_list_sorted = 1
        

#QQ回复包
#依次为:操作成功、申请登录码成功、重定向登录包到另外的服务器、登录时密码错误、改变在线状态成功、发送认证消息成功
QQ_replay={'ok':0x00, 'pre_ok':0x00, 'redirect':0x01, 'pwd_error':0x05, 'change_status':0x30, 'add_friend_auth':0x30}

#群命令
GROUP_cmd={'send':0x0A, 'tmp':0x01}




