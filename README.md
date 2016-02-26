# netfilter
##介绍
本工具基于scapy和nfqueue，实时对抓取的网络流量进行筛选和修改。可以截获IP层及以上的数据包(因为通过修改iptables的方法截获流量，无法捕获Ethernet层的包)。

##环境
python 2.7
linux

##安装依赖
Debian 系列linux下的安装依赖方式如下

`sudo apt-get python-nfqueue python-scapy`

##使用
使用之前需要编写filter脚本，filter_expamles目录下为示例脚本。
```
python main.py [-h] [--log-level {debug,info}] -F FILTER [-m MODE] [-d]

参数:
  -h, --help            显示帮助信息
  -F FILTER, --filter FILTER
                        选择应用的修改脚本
  -m MODE[i/o/f], --mode 
选择捕获流量模式，i 表示进入本机的流量，o 表示输出的流量 ,f 表示转发的流量
  -d, --debug           显示调试信息
```  
  
##示例
###例1
本例展示如何修改本机发出的http请求包。使用到的filter脚本http.py内容如下：

 ![image](https://cloud.githubusercontent.com/assets/9067927/13340838/79565350-dc6e-11e5-8d38-0a2aa8dc4de5.png)
 
使用packet查看和修改抓取的包的内容。packet是scapy的对象，详细内容见http://www.secdev.org/projects/scapy/doc/usage.html 。
位于try块内容中的两行代码将http版本由1.1改为1.0。
将http的内容修改过后，修改IP包头和TCP包头的长度和校验码，删除校验码的时候scapy会自动生成新的校验码。也可以直接使用scapy重新构造新新的数据包，构造新的数据包时，scapy会自动计算长度和校验码。最后使用payload.set_verdict_modified将修改后的包发送出去。

执行命令启动工具：
`sudo python main.py -m o -F filter_examples/http.py -d`

在命令行中执行wget www.baidu.com, 工具输出如下：

 ![image](https://cloud.githubusercontent.com/assets/9067927/13340841/805cfaa0-dc6e-11e5-84fc-be997921aa1b.png)

###例二
	本例展示如何修改dns查询返回的数据包。示例文件为nds.py, 内容如下图。spoofIP是将DNS答复修改为的假IP地址。
	
 ![image](https://cloud.githubusercontent.com/assets/9067927/13340845/88f518f0-dc6e-11e5-905d-3cd59a2a496f.png)

执行`sudo python main.py -m o -F filter_examples/dns.py -d `启动工具。

执行dig命令，发现dns响应已被修改。

 ![image](https://cloud.githubusercontent.com/assets/9067927/13340847/8ba608c0-dc6e-11e5-9679-6d5923e75bef.png)
