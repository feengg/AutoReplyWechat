# wechat autoreply
import itchat
import requests
import re
# 抓取网页
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
        #itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                        #(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                        # msg['User']['NickName'],
                        # msg['Text']), 'filehelper')
        # 回复给好友
        url = "http://www.tuling123.com/openapi/api?key=39df371b491d4099870bb56b3aebc277&info="
        url = url + msg['Text']
        html = getHtmlText(url)
        message = re.findall(r'\"text\"\:\".*?\"',html)
        reply = eval(message[0].split(':')[1])
        return reply

if __name__ == '__main__':
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
