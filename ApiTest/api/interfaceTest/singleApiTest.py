# Create your views here.
import json
import threading
import time
import os
from django.http import Http404
from ApiTest.models import SystemRole, SingleApi, LocustApi
from ApiTest.serializers import SingleApiResponseSerializers, LocustApiSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ApiTest.common.requestMothod import RequestMethod

ret = {"code": 1000}


class SingleApiTest(APIView):

    def get_token_ip_by_identity(self, identity):
        '''
        获取角色请求令牌和ip
        :param identity: 用户角色
        :return: 请求令牌
        '''
        token = SystemRole.objects.get(identity=identity).token
        ip = SystemRole.objects.get(identity=identity).ip
        return token, ip

    def check_greater_less_is_exist(self, body):
        '''
        判断请求体或者响应结果中是否存在<>,将其替换为中文的＜＞，layui数据表格bug，暂且这么处理
        :param body:
        :return: 需要替换后的数据
        '''
        if type(body) is str:
            if "＜" in body or "＞" in body:
                print('存在需要替换的符号')
                a = body.replace("＜", "<")
                body_replaced = a.replace("＞", ">")
                return body_replaced
            else:
                return body
        elif type(body) is dict:
            body = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2)
            if "＜" in body or "＞" in body:
                print('存在需要替换的符号')
                a = body.replace("＜", "<")
                body_replaced = a.replace("＞", ">")
                return body_replaced
            else:
                return body

    def check_result_is_fail(self, result):
        '''
        :param body:
        :return: 错误的接口数
        '''
        failed_num = 0
        result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        if "error" in result and "timestamp" in result:
            failed_num += 1
            return failed_num

    def parameter_check(self, identity, url, method):
        """
        验证参数
        :param data:datas
        :return:参数有误
        """
        try:
            # 必传参数 method, url, headers
            if not identity or not url or not method:
                ret["code"] = 1001
                ret["error"] = "必传参数URL。headers、identity不存在"
        except KeyError:
            ret["code"] = 1001
            ret["error"] = "Key错误"
        return ret

    def post(self, request, format=None):
        '''
        接口响应结果，JOSN格式化数据
        '''
        datas = request.data
        content = json.loads(datas.get("request", ""))
        L = []
        for i in content:
            caseid = i.get("caseid", "")
            identity = i.get("identity", "")  # 用户身份
            url = i.get("url", "")  # 登录地址
            method = i.get("method", "")  # 请求方式
            params = i.get("params", "")  # query数据
            body = i.get("body", "")  # body数据
            params = "" if params == None else params
            body = "" if body == None else body
            result = self.parameter_check(identity, url, method)
            if result["code"] == 1001:
                return Response(ret)
            token, ip = self.get_token_ip_by_identity(identity)  # 根据用户身份获取请求头Token数据
            print(token, ip)
            body = self.check_greater_less_is_exist(body)
            try:
                starttime = time.time()
                response = RequestMethod(token).run_main(method, ip + url, params, body)
                L.append(response)
                endtime = time.time()
                runtime = round(endtime - starttime, 3)  # 接口执行的消耗时间
                djson = self.check_greater_less_is_exist(response)
                id = SingleApi.objects.get(caseid=caseid)
                data = {"result": djson, "duration": runtime}

                serializer = SingleApiResponseSerializers(id, data=data)
                # 在获取反序列化的数据前，必须调用is_valid()方法进行验证，验证成功返回True，否则返回False
                if serializer.is_valid():
                    serializer.save()
                else:
                    ret["code"] = 1001
                    ret["error"] = serializer.errors
                    return Response(ret, status=status.HTTP_400_BAD_REQUEST)
            except TypeError as e:
                ret["code"] = 1001
                ret["error"] = "操作或函数应用于不适当类型的对象"
                return Response(ret)
            except json.decoder.JSONDecodeError as e:
                ret["code"] = 1001
                ret["error"] = "json.loads()读取字符串报错"
                return Response(ret)
        # 将[{},{}]数据返回给前端
        ret["msg"] = L
        return Response(ret)


class RepeatRunSingleApi(SingleApiTest):
    num_progress = 0
    repeat_result = {}

    def get(self, request, format=None):
        print('show_api----------' + str(RepeatRunSingleApi.num_progress))
        # 当进度百分百的时候，需要吧全局变量初始化，以便下次请求的时候进度条是重0开始，否则默认都是百分之百了
        if RepeatRunSingleApi.num_progress == 100:
            RepeatRunSingleApi.num_progress = 0
            return Response(100)
        # 当进度不是百分之百的时候，返回当前进度
        else:
            return Response(RepeatRunSingleApi.num_progress)

    def post(self, request, format=None):
        '''
        :param request: request.data
        :param format: None
        :return: 接口响应结果，JOSN格式化数据
        '''
        datas = request.data
        content = json.loads(datas["request"])
        runtime = json.loads(datas["runtime"])
        try:
            concurrency = json.loads(datas["concurrency"])
            print("多线程运行")
            runtime_concurrency = int(concurrency) * int(runtime)
            # 构造线程组
            L = {}
            for i in range(int(concurrency)):
                L[i * int(runtime)] = (i + 1) * int(runtime)
            print(L)
            thread = []
            for start, end in L.items():
                t = threading.Thread(target=self.repeat_run,
                                     args=(start, end, content, runtime_concurrency, int(concurrency)))
                thread.append(t)

            starttime = time.time()
            for i in range(len(thread)):
                thread[i].start()

            for w in range(len(thread)):
                thread[w].join()
            endtime = time.time()

            runtimes = round(endtime - starttime, 3)
            print("运行已结束")
            if type(self.repeat_result) != dict:
                dic = {}
                dic["重复执行结果"] = self.repeat_result
                self.repeat_result = dic
            self.repeat_result["总消耗时间"] = str(runtimes) + "秒"
            self.repeat_result["平均响应时间"] = str(round(runtimes / int(runtime), 3) * 1000) + "毫秒"
            self.repeat_result["重复执行次数"] = end
            return Response(self.repeat_result)
        except:
            print("单线程运行")
            L = {0: int(runtime)}
            thread = []
            for start, end in L.items():
                t = threading.Thread(target=self.repeat_run, args=(start, end, content))
                thread.append(t)

            starttime = time.time()
            for i in range(len(thread)):
                thread[i].start()

            for w in range(len(thread)):
                thread[w].join()
            endtime = time.time()
            runtimes = round(endtime - starttime, 3)
            print("运行已结束")
            if type(self.repeat_result) != dict:
                dic = {}
                dic["重复执行结果"] = self.repeat_result
                self.repeat_result = dic
            self.repeat_result["总消耗时间"] = str(runtimes) + "秒"
            self.repeat_result["平均响应时间"] = str(round(runtimes / int(runtime), 3) * 1000) + "毫秒"
            self.repeat_result["执行次数"] = end
            return Response(self.repeat_result)

    def repeat_run(self, start, end, content, runtime_concurrency=None, concurrency=None):
        cnt = 0
        for num in range(start, end):
            L = []
            for i in content:
                identity = i.get("identity", "")  # 用户身份
                url = i.get("url", "")  # 登录地址
                method = i.get("method", "")  # 请求方式
                params = i.get("params", "")  # query数据
                body = i.get("body", "")  # body数据
                params = "" if params == None else params
                body = "" if body == None else body
                # result = self.parameter_check(identity, url, method)
                # if result["code"] == 1001:
                #     return Response(ret)
                token, ip = self.get_token_ip_by_identity(identity)  # 根据用户身份获取请求头Token数据
                body = self.check_greater_less_is_exist(body)
                try:
                    response = RequestMethod(token).run_main(method, ip + url, params, body)
                    L.append(response)
                except TypeError as e:
                    self.repeat_result = {"code": 400, "msg": "操作或函数应用于不适当类型的对象"}
                except json.decoder.JSONDecodeError as e:
                    self.repeat_result = {"code": 400, "msg": "json.loads()读取字符串报错"}
                if concurrency:
                    cnt += concurrency
                    all_num = runtime_concurrency * len(content)
                else:
                    cnt += 1
                    all_num = len(content) * end
                print("进度条计数=" + str(RepeatRunSingleApi.num_progress))
                RepeatRunSingleApi.num_progress = round(cnt / (all_num) * 100, )
                print("进度条计数=" + str(RepeatRunSingleApi.num_progress))
        # 将[{},{}]数据赋值给类变量repeat_result
        self.repeat_result = {"多接口重复执行结果": L}


class LocustSingApi(APIView):
    '''
    性能测试
    '''

    def get_token_ip_by_identity(self, identity):
        '''
        :param identity: 用户角色
        :return: 角色请求令牌、ip
        '''
        token = SystemRole.objects.get(identity=identity).token
        ip = SystemRole.objects.get(identity=identity).ip
        return token, ip

    def get_object(self, pk):
        try:
            return LocustApi.objects.get(caseid=pk)
        except LocustApi.DoesNotExist:
            raise Http404

    def get(self, request):
        '''
        关闭蝗虫(性能测试端口)
        '''
        locust_process = os.popen('lsof -i:8089').readlines()[-1]
        res = locust_process.split(" ")
        res_filter = list(filter(None, res))
        try:
            command = "kill -9 {}".format(res_filter[1])
            print(command)
            os.system(command)
            ret["msg"] = "Successful closing locust"
        except Exception as e:
            print(e)
            ret["code"] = 1001
            ret["error"] = "Failed closing locust"
        return Response(ret)

    def put(self, request, pk):
        '''
        :param request: 请求压测的接口参数
        :param pk: 唯一id
        :return:蝗虫任务8089端口开启，返回成功提示
        '''
        datas = request.data
        content = json.loads(datas["request"])[0]
        identity = content.get("identity", "")  # 用户身份

        token, ip = self.get_token_ip_by_identity(identity)  # 根据用户身份获取请求头Token数据和IP
        headers = json.dumps({"accessToken": token})
        content["header"] = headers
        content["ip"] = ip
        print(content)
        snippet = self.get_object(pk)
        serializer = LocustApiSerializers(snippet, data=content)
        if serializer.is_valid():
            serializer.save()
            # 天坑，不后台运行，应该就是阻塞了，Response返回的消息不能返回，暂时使用后台运行解决
            os.system("nohup locust -f ApiTest/common/locustTest.py --host={} &".format(ip))
            ret["msg"] = "Successful opening locust"
            return Response(ret)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
