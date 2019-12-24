import requests,json
import sys,os
cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path_parent = os.path.dirname(os.path.realpath(cur_path))
sys.path.append(cur_path_parent)



class QuickMothod():
    def get(self,url,headers,params):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        r = requests.get(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("GET请求出错",e)
            return r.text



    def post(self,url,headers,params,data):

        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        if data:
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        else:
            r = requests.post(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            return r.text


    def delete(self,url,headers,params,data):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        if data:
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.delete(url, params=params, data=json.dumps(data), headers=headers)
        else:
            r = requests.delete(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            return r.text


    def put(self,url,headers,params,data):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        if data:
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.put(url, params=params, data=json.dumps(data), headers=headers)
        else:
            r = requests.put(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("PUT请求出错",e)
            return r.text


    def uploadfile(self,url,headers,params,data):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        print(data['path'])
        print(type(data['path']))
        print(params)
        print(type(params))
        files = {"file": open(data['path'], "rb")}
        r = requests.post(url, params=params, files=files, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("转换字典失败",e)
            print(r.text)
            return r.text



    def run_main(self,method,url,headers,params,data):
        res = None
        if method == "GET":
            res = self.get(url,headers,params)

        elif method == 'POST':
            res = self.post(url,headers,params,data)

        elif method == 'DELETE':
            res = self.delete(url, headers,params,data)

        elif method == 'PUT':
            res = self.put(url,headers, params,data)

        elif method == "FILE":
            res = self.uploadfile(url,headers,params,data)

        return res




if __name__ == "__main__":
    method = "PUT"
    url = 'http://amberdata.cn/transferapi/v2/transfer_form/update_transfer_form'
    headers = '{"Content-Type": "application/json", "accessToken": "90e83f1becfeddf8234a2690336c86e8"}'
    params = '{"id": "/档案移交/J010/2018/83ab27ef-8444-461d-a47d-08235fd9c2b1"}'
    data ={}
    a = QuickMothod()
    b = a.run_main(method,url=url,headers=headers,params=params,data=data)
