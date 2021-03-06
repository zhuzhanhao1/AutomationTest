import requests,json
import sys
import os

cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path1 = os.path.dirname(os.path.realpath(cur_path))
cur_path2 = os.path.dirname(os.path.realpath(cur_path1))
sys.path.append(cur_path2)


class RequestMethod:

    def __init__(self,token):
        self.token = token

    def get(self,url,params):
        headers = {
            "accessToken": self.token
        }
        params = json.loads(params) if params != "" else None
        r = requests.get(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("GET请求出错",e)
            return r.text



    def post(self,url,params,data):
        headers = {
            "accessToken": self.token,
            "Content-Type": "application/json"
        }
        params = json.loads(params) if params != "" else None
        if data:
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        else:
            r = requests.post(url, params=params, data=None, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            return r.text

    def delete(self,url,params,data):
        params = json.loads(params) if params != "" else None
        if data:
            headers = {
                "accessToken": self.token,
                "Content-Type": "application/json"
            }
            data = json.loads(data)
            r = requests.delete(url, params=params, data=json.dumps(data), headers=headers)
        else:
            headers = {"accessToken": self.token}
            r = requests.delete(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            return r.text

    def put(self,url,params,data):
        headers = {
            "accessToken": self.token,
            "Content-Type": "application/json"
        }
        params = json.loads(params) if params != "" else None
        if data == '[]':
            # data = eval(data)
            print("body传的是一个空数组的情况下，我被执行了！")
            data = json.loads(data)
            # data = data if any(data) == True else None
            r = requests.put(url, params=params, data=json.dumps(data), headers=headers)
        elif data:
            # data = eval(data)
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.put(url, params=params, data=json.dumps(data), headers=headers)

        else:
            r = requests.put(url, params=params, data=None, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("PUT请求出错",e)
            return r.text

    def uploadfile(self,url,params,data):
        params = json.loads(params) if params != "" else None
        if data:
            # data = eval(data)
            data = json.loads(data)
            data = data if any(data) == True else None
        print(data['path'])
        print(type(data['path']))
        print(params)
        print(type(params))
        headers = {
            "accessToken": self.token
        }
        files = {"file": open(data['path'], "rb")}
        r = requests.post(url, params=params, files=files, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("上传文件失败",e)
            print(r.text)
            return r.text

    def run_main(self,method,url,params,data):
        res = None
        if method == "get":
            res = self.get(url,params)

        elif method == 'post':
            res = self.post(url,params,data)

        elif method == 'delete':
            res = self.delete(url,params,data)

        elif method == 'put':
            res = self.put(url, params,data)

        elif method == "file":
            res = self.uploadfile(url,params,data)

        return res


if __name__ == "__main__":
    pass