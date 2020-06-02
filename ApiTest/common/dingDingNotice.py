import requests,json
from dingtalkchatbot.chatbot import DingtalkChatbot
import time
import hmac
import hashlib
import base64
import urllib.parse

class DingNotice:

    def __init__(self):
        # Webhook地址
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=153b78f377161db415e453c8e5442a5657694569bb7440e49c3ff14f8aaef583"
        # 加签密钥
        self.secret = "SEC17cc4536b6007bae4e6701a3aec556911042b503af484a20a7cb789fef4a10eb"

    def get_sign_timestamp(self):
        #获取时间戳和签证
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # print(timestamp)
        # print(sign)
        return timestamp,sign

    def send_ding(self,content,head=None):
        #发送文本格式消息
        timestamp,sign = self.get_sign_timestamp()
        url = self.url + "&timestamp=" + timestamp + "&sign=" + sign
        print(url)
        if head:
            l = []
            l.append(head)
            print("你发送的用户是：" + str(l))
            params = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "at": {
                    "atMobiles": l,
                    "isAtAll": False
                }
            }
        else:
            params = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "at": {
                    "atMobiles": [],
                    "isAtAll": False
                }
            }
        headers = {
            "Content-Type":"application/json"
        }
        print(params)
        f = requests.post(url, data=json.dumps(params), headers=headers)
        if f.status_code==200:
            print("发送成功")
            return True
        else:
            return False

    def send_text_bot(self,content,phone=None):
        #Text消息之@指定用户@所有人
        xiaoding = DingtalkChatbot(self.url,secret=self.secret, pc_slide=True)
        if phone:
            at_mobiles = []
            at_mobiles.append(phone)
            xiaoding.send_text(msg='{}'.format(content),at_mobiles=at_mobiles)
        else:
            xiaoding.send_text(msg='{}'.format(content),is_at_all=True)

    def send_image_bot(self,imagepath):
        #发送图片
        xiaoding = DingtalkChatbot(self.url, secret=self.secret, pc_slide=True)
        xiaoding.send_image(pic_url='{}'.format(imagepath))

    def send_link_bot(self,key, id, text):
        xiaoding = DingtalkChatbot(self.url,secret=self.secret)
        xiaoding.send_link(title='接口详情', text='{}请点击我......'.format(text),
                           message_url='http://zhuzhanhao.cn:8000/detail/?{}={}'.format(key, id))




# if __name__ == "__main__":
    # DingNotice().send_ding("","")
    # DingNotice().send_text_bot()