from tkinter import *
# wechat autoreply
import itchat
import requests
import re
class Reg (Frame):
    def __init__(self,master):
        #界面
        master.geometry("600x360")
        frame = Frame(master)
        frame.grid(row = 0, column = 0,pady=25,padx=40)
        self.lab1 = Label(frame,text = "请输入api:")
        self.lab1.grid(row = 0,column = 0,sticky = W,padx=5)
        self.apikey = Entry(frame,width=60)
        self.apikey.grid(row = 0,column = 1,sticky = W)
        self.auto_reply_button = Button(frame,text="启动自动回复",command=self.auto_reply)
        self.auto_reply_button.grid(row=1,column=1,sticky=W)
    # 抓取网页函数
    def getHtmlText(url):
        try:
            r = requests.get(url,timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return ""
    # 自动回复
    # 封装好的装饰器，当接收到的消息是Text，即文字消息
    @itchat.msg_register(['Text','Map', 'Card', 'Note', 'Sharing', 'Picture'])
    def text_reply(msg):
    # 当消息不是由自己发出的时候
        if not msg['FromUserName'] == Name["Jestiao"]:
        # 发送一条提示给文件助手
            itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                        msg['User']['NickName'],
                        msg['Text']), 'filehelper')
        # 回复给好友
            apikey = self.apikey.get()
            api_key = ""
	        url = "http://www.tuling123.com/openapi/api?key=" + api_key + "&info="
            url = url + msg['Text']
            html = getHtmlText(url)
            message = re.findall(r'\"text\"\:\".*?\"',html)
            reply = eval(message[0].split(':')[1])
            return reply

    def auto_reply(self):
        itchat.auto_login()
        # 获取自己的UserName
        friends = itchat.get_friends(update=True)[0:]
        Name = {}
        Nic = []
        User = []
        for i in range(len(friends)):
            Nic.append(friends[i]["NickName"])
            User.append(friends[i]["UserName"])
        for i in range(len(friends)):
            Name[Nic[i]] = User[i]
        itchat.run()

root = Tk()
root.title("微信自动回复")
app = Reg(root)
root.mainloop()
