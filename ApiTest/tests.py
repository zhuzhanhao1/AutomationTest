from django.test import TestCase,Client

class TestUnit(TestCase):

    def test(self):
        # 调用自身的方法
        print(123)
        res = self.client.get('/api/v1/menu/list/')
        print(res)
        # print(res.json())



# c = Client()
# # 客户端发送请求
# c.get('url')