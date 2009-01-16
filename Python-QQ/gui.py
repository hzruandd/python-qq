# -*- coding: utf-8 -*-
"""作者:shhgs.efhilt@gmail.com"""

import  wx
#import ColorPanel
import images

from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor, defer, threads

import qqlib
from qq.message import qqmsg
from qq.protocols import qqp

import os

import time

colourList = [ "Aquamarine", "Black", "Blue", "Blue Violet", "Brown", "Cadet Blue",
               "Coral", "Cornflower Blue", "Cyan", "Dark Grey", "Dark Green",
               "Dark Olive Green",
               ]

class GuiProtocol(qqlib.qqClientProtocol):
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
        pass

    def printl(self,str):#转换编码
        if os.name == 'nt':
            print str.decode('utf-8').encode("cp936")

class LoginDialog(wx.Dialog) :
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,   \
            style=wx.DEFAULT_DIALOG_STYLE                                           \
            ):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, u"登录")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, u"QQ号")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.qid = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.qid, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, u"口令 ")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.pwd = wx.TextCtrl(self, -1, "", size=(80,-1), style = wx.TE_PASSWORD)
        box.Add(self.pwd , 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK, u'登录')
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL, u'取消')
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

class About(wx.Dialog):
    def __init__(self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,   \
            style=wx.DEFAULT_DIALOG_STYLE                                           \
            ):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, u"登陆失败！")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK, u'重试')
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL, u'关闭')
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        
class GUIFrame(wx.Frame) :
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
                    size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE|wx.FULL_REPAINT_ON_RESIZE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        self.qqConnection = None                        ##  在Login方法里面创建
        self.log          = qqlib.initLogging()         ##  ...

        ##-------------------------------------------
        ##  Install Menu
        menuBar = wx.MenuBar()

        menuAccount = wx.Menu()

        menuAccount.Append(101, u"登录", "")
        menuAccount.Append(102, u"退出程序", "")
        self.Bind(wx.EVT_MENU, self.Login, id = 101)
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id = 102)

        menuBar.Append(menuAccount, u"菜单")

        self.SetMenuBar(menuBar)
        self.statusbar = self.CreateStatusBar(1, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusText(u"Python-QQ未登陆", 0)
        
        ##-------------------------------------------

    ##-------------------------------------------
    ##  Menu Event
    def LoginError(self):
        dlg = About(self, -1, u"警告", size=(350, 200),
                         #style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME
                         style = wx.DEFAULT_DIALOG_STYLE
                         )
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            self.conn.login()
            reactor.callLater(1,self.test)
            dlg.Destroy()
        
    def test(self):
            i = 0
            while i < 2:
                if self.qq.login == 1:
                    self.statusbar.SetStatusText(u"Python-QQ登陆成功", 0)
                    return
                time.sleep(1)
                i += 1
            self.statusbar.SetStatusText(u"Python-QQ登陆失败", 0)
            self.LoginError()
           
    def Login(self, event) :
        dlg = LoginDialog(self, -1, u"Python-QQ登录窗口", size=(350, 200),
                         #style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME
                         style = wx.DEFAULT_DIALOG_STYLE
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
            qid = int(dlg.qid.GetValue().strip())
            pwd = dlg.pwd.GetValue().strip()

            self.qq = qqlib.qq(qid, pwd, self.log)
            self.conn = GuiProtocol(self.qq)
            reactor.listenUDP(0, self.conn)

            self.log.info("Python-QQ starts")
            self.conn.login()
            reactor.callLater(1,self.test)

            self.log.info("login success")
            dlg.Destroy()
            

    ##------------------------------------------
    
    def OnCloseWindow(self, event) :
        try:
            defer(self.conn.logout())
            defer(self.conn.logout())
            defer(self.conn.logout())
            defer(self.conn.logout())
            reactor.stop()
            self.Destroy() 
        except:
            reactor.stop()
            self.Destroy() 

class TestApp(wx.App) :
    def OnInit(self) :
        frame = GUIFrame(None, -1, 'Python-QQ', size = (200, 500))
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__" :
    app = TestApp(0)
    reactor.registerWxApp(app)
    reactor.run()
