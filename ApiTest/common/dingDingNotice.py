import requests,json
from dingtalkchatbot.chatbot import DingtalkChatbot
#测试部URL
url = "https://oapi.dingtalk.com/robot/send?access_token=99c9913b6f5370541f17d56b3e1e32ca4d534b25f17df9fcedf44aa5173968a6"
#小分队URL
# url = "https://oapi.dingtalk.com/robot/send?access_token=21829afa1afbefb42c38dfe171a4f6398448eec4da63bb914310067d22b256fc"

# 初始化机器人小丁
def send_image():
    xiaoding = DingtalkChatbot(url)
    xiaoding.send_text(msg='-李建构吃屎去吧！')
    # xiaoding.send_image(pic_url='https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=1147110391,1099568746&fm=173&app=25&f=JPEG?w=640&h=640&s=4BA43A625AFA7BAF7D302CC60000A0A1')

def send_singleapi_link(isprocess,id,text):
    xiaoding = DingtalkChatbot(url)
    xiaoding.send_link(title='接口详情', text='{}请点击我......'.format(text), message_url='http://localhost:8000/detail/?{}={}'.format(isprocess,id))

def send_process_link(id, text):
    xiaoding = DingtalkChatbot(url)
    xiaoding.send_link(title='接口详情', text='{}请点击我......'.format(text),
                       message_url='http://zhuzhanhao.cn:8000/get_processcase_details/?id={}'.format(id))


def get_phone_number_by_name(name):
    if name == "老张":
        return "15270833545"
    elif name == "老刘":
        return "15279438039"
    elif name == "老李":
        return "13157155198"
    elif name == "老江":
        return "15073326435"
    elif name == "老王":
        return ""
    else:
        return ""

def send_ding(content,head=None):
    l = []
    phone_number = l.append(get_phone_number_by_name(head))
    print(phone_number)
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
    headers = {
        "Content-Type":"application/json"
    }

    f = requests.post(url, data=json.dumps(params), headers=headers)
    if f.status_code==200:
        return True
    else:
        return False


if __name__ == "__main__":
    send_image()
