from locust import HttpLocust, TaskSet, task, between
import json,os
import pymysql

class LocustTest(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.ip = "http://amberdata.cn"
        self.url, self.method, self.headers, self.params, self.data= self.conn_db()

    def conn_db(self):
        # 打开数据库连接
        db = pymysql.connect(host="localhost", user="root", password="123456",
                             port=3306, database="AutomationTest", charset='utf8')
        cursor = db.cursor()
        cursor.execute("select * from ApiTest_locustapi where caseid ='1'")
        db.commit()
        data = cursor.fetchone()
        #关闭数据库链接
        db.close()
        return data[2],data[3],data[4],data[5],data[6]

    @task(1)
    def profile(self):
        if self.method == "get":
            print("get 请求")
            headers = json.loads(self.headers)
            params = json.loads(self.params) if self.params != None  else None
            with self.client.get(url = self.url, headers=headers, params=params,catch_response=True) as res:
                pass
            try:
                print(json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=2))
            except Exception as e:
                return res.text

        elif self.method == 'post':
            print("post 请求")
            headers = json.loads(self.headers)
            headers["Content-Type"] = "application/json"
            params = json.loads(self.params) if self.params != None else None
            if self.data:
                data = json.loads(self.data)
                data = data if any(data) == True else None
                with self.client.post(url=self.url, headers=headers, params=params, data=json.dumps(data), catch_response=True) as res:
                    pass
            else:
                with self.client.post(url=self.url, headers=headers, params=params, catch_response=True) as res:
                    pass
            try:
                print(json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=2))
            except Exception as e:
                return res.text

        elif self.method == "put":
            print("put 请求")
            headers = json.loads(self.headers)
            headers["Content-Type"] = "application/json"
            params = json.loads(self.params) if self.params != None else None
            if self.data == '[]':
                data = json.loads(self.data)
                res = self.client.put(url=self.url, params=params, data=json.dumps(data), headers=headers)
            elif self.data:
                # data = eval(data)
                data = json.loads(self.data)
                data = data if any(data) == True else None
                res = self.client.put(url=self.url, params=params, data=json.dumps(data), headers=headers)
            else:
                res = self.client.put(url=self.url, params=params, data=None, headers=headers)
            try:
                print(json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=2))
            except Exception as e:
                return res.text

        elif self.method == "delete":
            print("delete 请求")
            headers = json.loads(self.headers)
            params = json.loads(self.params) if self.params != None else None
            if self.data:
                headers["Content-Type"] = "application/json"
                data = json.loads(self.data)
                with self.client.delete(url=self.url, headers=headers, params=params, data=json.dumps(data), catch_response=True) as res:
                    pass
            else:
                with self.client.delete(url=self.url, headers=headers, params=params, catch_response=True) as res:
                    pass
            try:
                print(json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=2))
            except Exception as e:
                return res.text


class WebsiteUser(HttpLocust):
    task_set = LocustTest   #定义此 HttpLocust 的执行行为的 TaskSet 类
    wait_time = between(1, 3)

if __name__ == "__main__":
    os.system("locust -f locustTest.py --host=http://amberdata.cn")
