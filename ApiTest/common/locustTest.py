from locust import HttpLocust, TaskSet, task, between
import json,os
import pymysql

class UserBehavior(TaskSet):

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
        print(data)
        print(type(data))
        db.close()
        return data[2],data[3],data[4],data[5],data[6]

    @task(1)
    def profile(self):
        if self.method == "get":
            print("get 请求")
            headers = json.loads(self.headers)
            params = json.loads(self.params) if self.params != "" else None
            print(params)
            with self.client.get(url = self.url, headers=headers, params=params,catch_response=True) as res:
                print(res.json())

        elif self.method == 'post':
            print("post 请求")
            headers = json.loads(self.headers)
            headers["Content-Type"] = "application/json"
            params = json.loads(self.params) if self.params != "" else None
            if self.data:
                data = json.loads(self.data)
                data = data if any(data) == True else None
                with self.client.post(url=self.url, headers=headers, params=params, data=json.dumps(data), catch_response=True) as res:
                    print(res.json())
            else:
                with self.client.post(url=self.url, headers=headers, params=params, catch_response=True) as res:
                    print(res.json())


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 3)

if __name__ == "__main__":
    os.system("locust -f locustTest.py --host=http://amberdata.cn")
