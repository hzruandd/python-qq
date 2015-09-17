# 湖北依赛特开源项目管理中心 #
  * Python-QQ：Python语言实现的QQ客户端。根据QQ协议，使用Python来实现一个跨平台的客户端。充分发挥Python语言快速开发和跨平台运行的优点，特别是让unix用户在使用QQ的时候又多一个选择。

## 更新日志 ##
```
2009-2-4        调整了socket-qq的程序，修改为多线程版，这样可以在控制台下输入命令，并不依赖任何外部包了。

2009-2-4        调整socket的程序，修改为可以手动输入QQ号码和密码，并加上了激活和验证码的判断。

2009-1-20       服务器恢复了，代码也恢复了。朋友们说twisted改动比较大，那就先调试一下socket的能不能用，比较顺利调好了，传一个上来。

2006-10-8       修改登陆包，确定服务器地址。修改了一处处理流水号的错误。不会接收多次同样消息了。

2006-7-22       修改数据包为2006，并修改了根登陆服务器地址。

2005-10-9       增加了对群消息的处理，将Python-QQ-bri做了两个群的桥接。

2005-09-26	将tea算法部分的中文注释提交上来了。

2005-09-10	能发送消息了，不过不稳定。

2005-09-09	增加了qqlib的部分注释。对qqlib的处理方法做了小调整。

2005-09-09	修改了GUI部分，能得到好友列表了，但是发送消息未完成。

2005-09-09	修改了GUI部分，能够正常登陆了。

2005-09-08	增加了对发送消息不成功的判断，但是未自动重发。

2005-08-11	增加了qq.login属性，为1时登陆成功。

2005-08-01	修改了消息处理方式，目前只处理了好友消息和陌生人消息。修正了改变当前状态的一处错误。

2005-07-30	按照limodou和其他朋友的提意，将编码改变为UTF-8，并通过os模块本程序自动在win和*uix下切换编码。将qqlib独立处理，分别进行控制台和图形界面的分工工作。hhgs.efhilt@gmail.com朋友提供了一个gui的程序，但是没有调试通过。将输入密码的地方使用了getpass模块。加上了登陆成功的提示。

2005-07-29	yxxyun@gmail.com朋友的提醒下，发现了一个命令定义错误。更改过来。

2005-07-28	因为朋友们反映在linux下不能使用，于是进行测试，发现2.3不支持某种方法的字典操作，更改update方法后，在FreeBSD 5.3下运行成功。

2005-07-27	释放出第一个版本，环境支持需要Python 2.4 以及twisted 2.01。目前实现的功能有：登陆、发送活动包、列好友、列在线好友、发送消息、接受好友消息、退出登陆。

```
## SVN 使用Tip ##
  * 按照 SVN 官方建议的代码组织方式来管理
  * 每个模块分三类目录，代表不同代码基线
```
 Python-QQ-bri/为分枝|QQ桥,连接多个QQ群的桥.        
 Socket-QQ/    为辅助版本|纯Python支持.        
 Python-QQ/    为主码线版本,Python和Twisted支持.        
```

## 项目列表 ##
|'''项目缩写'''|'''语言'''|'''项目说明'''|'''管理员'''|
|:---------|:-------|:---------|:--------|
|[Python-QQ](http://code.google.com/p/python-qq)|Python  |基于Python语言的客户端|梅劲松      |

## 项目成员列表 ##
|wansongying|wansongying@hotmail.com|目前主要学习python，想有机会参与一些python项目|完全是个人喜好，呵呵！|
|:----------|:----------------------|:----------------------------|:----------|
|bioworker  |zt\_bio@tom.com        |目前主要使用JAVA写程序，开发过JSP网络管理系统，已学习PYTHON二年，开发过小的pygame程序，想有机会参与一些python项目|个人喜好，呵呵！   |
|cls        |526044268@qq.com       |刚开始学习python，                 |主要是因为google，呵呵|
|Whidbey    |oopilix@gmail.com      |学习python不久，当前工作主要用c++        |喜欢python,django的优雅|
|Daniel     |danielruru@gmail.com   |刚刚开始学习python，以前一直使用C++（5年）   |无          |
|Ivan.liu   |mingchong@tom.com      |了解令人兴奋新技术学习开发经验              |无          |
|Gavin      |chinawujie@gmail.com   |参与项目,学习项目开发经验                |无          |
|梅          |stephen.cn@gmail.com   |管理项目并负责Python-QQ的socket部分    |无          |
|Hoxide     |Hoxide\_dirac@yahoo.com.cn|负责Python-QQ的加密部分             |无          |
|Fit荣       |seasion@163.com        |负责项目测试,架构分析,了解python好几年了，    |一直研究Python |
|暗夜精灵       |ghostwwl@gmail.com     |名曰:参与测试，分析数据结构，算法gui学习中      |无          |
|树上蹭灰       |cn-poper@126.com       |参与测试，参考大家代码，学习               |无          |
|yxxyun     |yxxyun@gmail.com       |参考大家代码，学习项目开发经验              |无          |
|HackGou    |HackGou@Gmail.com      |参与项目测试，并学习ing                |无          |
|metaphy    |moonlinking@hotmail.com|可以参与GUI方面的开发                 |现在J2EE下做开发 |
|playing    |playing5460@hotmail.com|现在做网络工作，使用JAVA写程序，学习PYTHON一年，想参与一些项目|无          |
|星尘细雨       |python23@163.com       |可参与部分开发，linux平台下的测试，debug等，使用python已经3年了，使用过Twisted，在公司也用，主要在linux平台上开发，对Python-QQ项目非常感兴趣|目前做linux下的C/C++开发|
|东方晓        |wjcroom@yahoo.com      |使用JAVA写程序，学习PYTHON二年，开发过gui程序，正开始学作soap开发，想参与一些项目|无          |
|开拓者        |bigbird91@gmail.com    |学习项目开发经验，参考代码                |无          |
|曾 经 沧 海    |boyxd@tom.com          |现在用python做开发，希望一个月后参与本项目，最近忙，|无          |
|healer     |healer\_kx@263.net     |没有做过Python项目,但是做C++和Java3年了.想关注一下项目的情况|无          |
|Net Fetch  |CnNetFetch@Gmail.com   |Python处于学习阶段,熟悉多种B/S技术了,有过软件开发、DBA以及软件预测经验.|无          |
|Hovering   |hoverzero@Gmail.com    |了解python好几年了，一直没静下心来学，现在有机会努力学习并投入正式应用了|无          |
|刘鹏         |liupengf12@Gmail.com   |刚刚接触Python，很是喜欢，希望能多了解这个项目，如果能贡献自己的力量更好了！|无          |
|杜杰         |dujie13579@sohu.com    |学习项目开发经验，参考代码                |无          |
|夜猫         |qsx76@hotmail.com      |学习项目开发经验，爱凑热闹，目前只会python的print语句 哈哈，参考代码|无          |
|冷剑         |xiaoping.tang@gmail.com|看了两本Python书籍，小有收获，没有经验，多多关照！ |无          |
|icgre      |icgre@163.com          |以前一直用zope，现在开始研究python，请多多指教！|无          |
|亦寒         |yihanfost@gmail.com    |非常喜欢Python，希望通过参加此项目学习并贡献一份力量|无          |
|shanjunxu  |shanjunxu@163.com      |我对python非常感兴趣，现在也在用python来写一些东西，我想通过编写python版ＱＱ来提高自己的水平。|无          |
|曲健宁        |redfox.qu@gmail.com    |学习Python3个月，很是喜欢，希望能多了解这个项目，如果能贡献自己的力量更好了！|无          |
|萧风         |zhuxiangguo@msn.com    |学习python,爱上python            |现在用Delphi开发DRP|
|xxandxx    |xxandxx@163.com        |学习python,希望参与这个项目,得到更多编程经验.我经验不多,但会努力|无          |
|guorke     |guorke@gmail.com       |**nix环境下 coder,关注python**|无          |
|Andrew     |andy\_wts@21cn.com     |关注python,共享python.希望能参与这个项目并结交更多的朋友|目前从事Linux相关开发，对内核和底层驱动比较熟|
|armit      |armit6826@21cn.com     |学习python,参考代码,这是我的第一个编程语言,一定要学好.|无          |
|mazha      |bg5hfc@gmail.com       | 在做类似的项目,希望借鉴经验              |无          |
|xgz        |xianggzh@hotmail.com   | 热爱驱使我来到这里，对QQ太多收费不满 。以前从事linux c，perl，shell等开发，java，vb，delphi等开发 |从事管理工作     |
|cngump     |cngump@gmail.com       |熟悉java,python编程。             |无          |
|weiqiboy   |weiqiboy@gmail.com     |正学习PYTHON,希望参与这个项目           |无          |
|shxiao     |shxiaole@gmail.com     |学了很长python了，希望能够参加这个项目       |无          |
|Tina       |2003220545@163.com     |学习python中,希望能参与这个项目          |从事项目管理工作   |
|JOESHOW    |joeshow79@gmail.com    |C++ Coder,学习PYTHON半年多，了解TWISTED，希望为PATHON-QQ添砖加瓦|无          |
|est        |electroniXtar@Gmail.com|脚本语言狂热份子，进来凑凑，看过QQ的协议，希望用PyQQ来搞应用|无          |
|Final      |finalmdj@gmail.com     |热爱Python,热衷于用python开发web     |以前从事过MUD,ASP,PHP相关项目|
|Night      |night2008@gmail.com    |学习Python,但没有编程经验,希望通过项目向大家学习 |无          |
|骆驼         |luotuo85@163.com       |接触Python时间不长，但是觉得她很好用，不需要考虑太多，让我可以专注于解决问题|嵌入式软件设计以前从事串口，USB通信软硬件设计|
|Jason      |tosa\_chang@163.com    |正在学习Python，希望为这个项目做些贡献，多交一些朋友|以前从事嵌入式软件开发，现在想转行做互联网|
|始作俑者       |zihe-liu@163.com       |正在学习Python                   |无          |
|夏旭         |flymao@gmail.com       |做网络路由交换的,有时候用编些WEB语言,刚学Python,希望能参与此项目|无          |
|李炜         |web2wap@gmail.com      |做过短信网关,主要语言c# 刚开始学python ,希望在这里学习.|无          |
|pinkfog    |pinkfog@163.com        |C++,使用过python写测试脚本           |无          |
|李李         |py.7@163.com           |编程语言也是一种信仰。我的信仰是python，持续学习使用中，希望加入一个socket项目以更多的了解他|无          |
|stonesun   |mazhenli@msn.com       |开始学习python，j2me一年多，希望参与其中。   |无          |
|copywater  |copywater@163.com      |刚刚接触Ｐｙｔｈｏｎ　就非常喜欢正在使用学习Ｃ＃，希望有机会和大家一起学|无          |
|pythonbin  |pythonbin@sina.com     |正学习python，希望与大家共勉！！！         |无          |
|yuejj      |yue.jinjiang@gmail.com |正在学习python，希望加入              |无          |
|yaoms      |yms541@gmail.com       |正在学习python，希望加入，向大家学习。从事过php的网站开发|无          |
|bluker     |bluker2599@gmail.com   |刚学习python，很有激情               |从事php的网站开发 |
|brian      |yaou.li@gmail.com      |喜欢python，在使用python作一些web开发   |工作内容 j2ee  |
|louwbc     |louwbc@gmail.com       |正在学习python,很希望参加一个实际项目,在实际项目中学习python.|无          |
|ffox       |ffoxzs@126.com         |学习python中,希望有个机会锻炼一下.        |无          |
|Donne      |fanglinyuan@163.com    |目前也在使用python做自动化测试框架,希望多结交Python朋友，多些交流.|无          |

## 项目邮件列表及讨论组 ##
> [Google提供的邮件列表及讨论组](http://groups.google.com/group/python-qq/)
## 错误反馈页面 ##
> 这里的代码托管能反馈吗？
# 维护 #
    * 2009年1月16日，今天终于从原来的trac服务器上将Python-QQ的代码拷贝出来了。恢复到google上，看了一下，最后一次更新代码是2006年10月8日。
    * 梅劲松::20050729 创立环境...


[湖北依赛特](http://www.easiest.cn)


Add your content here.


# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages