# **△须知：项目运行相关事项**
## **因本人上次请求结对无人结对导致测试无法寻求他人设备做连接测试**
## **本项目有两个默认用户“111”和“yjj”，密码分别为“111”和“yjj”，特权功能未开发，项目可查，无需担心安全问题**
### **1、最简单且不出错方法**（缺少结对队友测试，以下均为个人和舍友推测）
1.1.在本人本机开启app.py作服务器端开始运行时（本机只连接校园FZU）<时间段不定，最近电脑看多了头痛，保险在下方>

1.1.1.连接FZU，确保处于同一局域网中

1.1.2.登入网址：http://10.133.73.221:5000   （一般到这里就成功了）

1.1.3.若登入网址失败，则请先win+rR启动cmd命令行工具，输入指令ping 10.133.73.221，看返回信息确认是否可以与本机进行通信

1.1.3.1.无法与本机通信，请先确认当前是否处于局域网FZU中

1.1.3.2.若在**1.1.3**中确认可以与本机通信或在**1.1.3.1**中确认在局域网FZU中，则请暂时关闭设备公用网络的防火墙（有些设备默认防火墙自动操作阻止设备与本机通信）

1.1.4.（放个保险）如果上述步骤都完成后仍无法运行项目，请发邮件到316591862@qq.com  （可能会维护后端文件）

### **2、常规方法**（以下均为个人和舍友推测，如有疏漏，可以尝试问大佬、gpt解决数据库问题，若无法解决参考上方保险）
#### **本项目因个人能力有限，基础功能不出错已是难得可贵，所以采用轻量级且较为简单完成基础功能的SQLite数据库**
2.1.将项目保存在个人喜欢的路径

**！！！！在此处分流！！！！**

2.2.1.已安装SQLite且已经有一定使用熟练度的人和设备

2.2.1.1.编辑器打开项目目录（本人使用VScode；Pycharm可行，其他编辑器不详），在**项目目录**中（app.py和inti1.py所在的页面）win+R启动cmd

2.2.1.2.![image](https://github.com/user-attachments/assets/e13f487a-0041-47a1-a873-942b9a9368dc)


参考这段代码，在cmd中使用pip安装对应环境依赖的库，参考命令为pip install Flask Flask-SQLAlchemy Flask-Login Flask-SocketIO Flask-Migrate
![image](https://github.com/user-attachments/assets/6127a3fa-27fe-4eba-a330-527d2c11136e)


由于本人已经安装好所有依赖库，所以如上

2.2.1.3.初始化数据库（在此对用户们表示歉意，初始化数据库后，本人推测不会有本人为了测试而作的示例，页面极可能十分空虚，不过成功后可以和好友在自己的数据库上面随意恶作剧）

在cmd中执行python init1.py 或者在编辑器里直接点击调试          （只有一个表的原因是能力有限时间有限）

![image](https://github.com/user-attachments/assets/7ee31e36-eb1e-4a6f-8ae9-0aed18d63806)

2.2.1.4.执行app.py

在cmd中执行python app.py 或者在编辑器里直接点击调试

![image](https://github.com/user-attachments/assets/63ca71df-e026-43e7-babe-1d507fd657b7)

会出现以上类似的信息，第一个网址为用户进入操作的地址，第二个网址为用户机可分享给与自己的设备处于同一局域网内的朋友随意操作的地址

**！！！！在此处分流！！！！**

2.2.2.未安装SQLite的设备

2.2.2.1.下载安装SQLite后，参照**2.2.1**的操作

2.2.2.2.因为SQLite是一个轻量级的关系数据库，通常嵌入在应用程序中，因此不需要单独安装，所以直接参照**2.2.1**的操作。（吃书ing，可能不用单独安装也行，但没有可借的调试设备）

（无Python环境的用户们可以考虑搭建虚拟环境，然后参照**2.2.1**的操作）

# **在此再次声明，上述均为本人和舍友基于即学知识和已经历的操作失误进行的推测**
