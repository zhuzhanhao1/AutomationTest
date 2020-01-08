# Create your views here.
import json
import threading
import time

import jsonpath
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets
from ApiTest.models import SystemRole, ProcessApi
from ApiTest.serializers import ProcessApiListSerializers,ProcessApiResponseSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ApiTest.common.requestMothod import RequestMethod

from rest_framework.parsers import JSONParser
'''
JSONParser: 表示只能解析content - type:application / json头
JSONParser: 表示只能解析content - type:application / x - www - form - urlencoded头
'''

class ProcessApiTest(APIView):

    num_progress = 0
    failed_num = 0
    failed_ids = []

    def get(self, request, format=None):
        '''
        :param request:
        :param format:
        :return: 流程进度
        '''
        print('show_api----------' + str(self.num_progress))
        # 当进度百分百的时候，需要吧全局变量初始化，以便下次请求的时候进度条是重0开始，否则默认都是百分之百了
        if self.num_progress == 100:
            self.num_progress = 0
            return Response(100)
        # 当进度不是百分之百的时候，返回当前进度
        else:
            return Response(self.num_progress)

    def get_token_ip_by_identity(self,identity):
        '''
        获取角色请求令牌和IP地址
        :param identity: 用户角色
        :return: 请求令牌
        '''
        token = SystemRole.objects.get(identity=identity).token
        return token

    def check_greater_less_is_exist(self,body):
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
        else:
            body = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2)
            if "＜" in body or "＞" in body:
                print('存在需要替换的符号')
                a = body.replace("＜", "<")
                body_replaced = a.replace("＞", ">")
                return body_replaced
            else:
                return body

    def check_result_is_fail(self,result,caseid):
        '''
        :param body:
        :return: 错误的接口数
        '''
        try:
            result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
            if "error" in result and "timestamp" in result:
                self.failed_num += 1
                self.failed_ids.append(caseid)
                return
            return
        except:
            print("返回结果不是JSON对象")
            return

    def parameter_check(self, identity,url,method):
        """
        验证参数
        :param data:datas
        :return:参数有误
        """
        try:
            # 必传参数 method, url, headers
            if not identity or not url or not method:
                return Response({"code": 400, "msg": "参数有误"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"code": 400, "msg": "参数有误"}, status=status.HTTP_400_BAD_REQUEST)

    def depend_params(self,depend_id):
        id = ProcessApi.objects.get(caseid=depend_id)
        return id


    def post(self, request, format=None):
        '''
        :param request: request.data
        :param format: None
        :return: 接口响应结果，JOSN格式化数据
        '''
        datas = request.data
        content = json.loads(datas["request"])
        if len(content) == 1:
            caseid = content[0].get("caseid","")
            identity = content[0].get("identity", "")    # 用户身份
            url = content[0].get("url", "")              # 登录地址
            method = content[0].get("method", "")        # 请求方式
            params = content[0].get("params", "")        # query数据
            body = content[0].get("body", "")            # body数据
            depend_id = content[0].get("depend_id", "")  # depend_id数据
            check_params = self.parameter_check(identity,url,method)
            token = self.get_token(identity)            # 根据用户身份获取请求头Token数据
            body = self.check_greater_less_is_exist(body)

            if check_params:
                return check_params
            try:
                starttime = time.time()
                response = RequestMethod(token).run_main(method, url, params, body)
                print(response)
                endtime = time.time()
                runtime = round(endtime - starttime, 3)
                djson = self.check_greater_less_is_exist(response)
                id = ProcessApi.objects.get(caseid=caseid)
                data = {"result":djson,"duration":runtime}
                serializer = ProcessApiResponseSerializers(id, data=data)
                # 在获取反序列化的数据前，必须调用is_valid()方法进行验证，验证成功返回True，否则返回False
                if serializer.is_valid():
                    serializer.save()
                    return Response(response, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except TypeError as e:
                print(e)
                return Response({"code": 400, "msg": "操作或函数应用于不适当类型的对象"}, status=status.HTTP_400_BAD_REQUEST)
            except json.decoder.JSONDecodeError as e:
                print(e)
                return Response({"code": 400, "msg": "json.loads()读取字符串报错"}, status=status.HTTP_400_BAD_REQUEST)
        else:

            '''
                选择多个接口运行
            '''
            dic = {}
            num = 0
            process_ids = []
            for i in content:
                caseid = i.get("caseid","")
                identity = i.get("identity", "")    # 用户身份
                url = i.get("url", "")              # 登录地址
                method = i.get("method", "")        # 请求方式
                params = i.get("params", "")        # query数据
                body = i.get("body", "")            # body数据
                depend_id = i.get("depend_id","")
                depend_key = i.get("depend_key","")
                replace_key = i.get("replace_key","")
                replace_position = i.get("replace_position","")

                result = self.parameter_check(identity, url, method)
                token = self.get_token(identity)  # 根据用户身份获取请求头Token数据
                body = self.check_greater_less_is_exist(body)

                if result:
                    return result
                if depend_id:
                    print("我需要依赖别的接口哦！！！")
                    depend_id = depend_id.split(",")
                    # 如果请求的依赖接口只有一个的时候
                    if len(depend_id) == 1:
                        if int(depend_id[0]) in process_ids:
                            print("我所依赖的接口出错了哦")
                            response = "我所依赖的id为" + depend_id[0] + "的接口出错了哦"
                            runtime = 0
                        else:
                            dependid = ProcessApi.objects.get(caseid=depend_id[0])
                            # 获取依赖接口返回的结果
                            result = json.loads(dependid.result)
                            body = json.loads(body) if body != "" else body
                            params = json.loads(params) if params != "" else params
                            # 从前台拿到需替换的key,转为字典，字典的键存入列表
                            replaceKey = eval(replace_key)
                            replaceKey_key = [x for x in replaceKey]
                            print(replaceKey_key)
                            # 从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                            dependkey = eval(depend_key)
                            dependkey_key = [x for x in dependkey]
                            print(dependkey_key)
                            # 判断替换的区域是body还是params，赋值给变量params_body
                            params_body = params if replace_position == "params" else body
                            depend_value = []  # 首先创建依赖的空列表
                            replace_value = []  # 首先创建替换的空列表
                            try:
                                for i in range(len(dependkey)):
                                    # 将依赖的结果集放入一个列表存储
                                    dependvalue = jsonpath.jsonpath(result, dependkey_key[i])[
                                        dependkey[dependkey_key[i]]]
                                    print(dependvalue)
                                    if type(dependvalue) is list:
                                        dependvalue = dependvalue[0]
                                    depend_value.append(dependvalue)
                                    # 将需要替换的结果集放入一个列表存储
                                    replacevalue = jsonpath.jsonpath(params_body, replaceKey_key[i])[
                                        replaceKey[replaceKey_key[i]]]
                                    print(replacevalue)
                                    if type(replacevalue) is list:
                                        replacevalue = replacevalue[0]
                                    replace_value.append(replacevalue)
                                # 将变量params_body转为json字符串，为了之后的字符串替换
                                params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                                # 将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                                for i in range(len(depend_value)):
                                    params_body = params_body.replace(replace_value[i], depend_value[i])
                                print(params_body)
                                starttime = time.time()
                                response = RequestMethod(token).run_main(method, url, params_body, json.dumps(
                                    body)) if replace_position == "params" else RequestMethod(token).run_main(method, url,
                                                                                                   json.dumps(params),
                                                                                                   params_body)
                                endtime = time.time()
                                runtime = round(endtime - starttime, 3)     #接口执行的消耗时间
                            except TypeError as e:
                                print("类型错误")
                                print(e)
                                response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                            except json.decoder.JSONDecodeError as e:
                                print("json解析错误")
                                print(e)
                                response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"
                    # 如果请求的依赖接口不止有一个的时候
                    else:
                        body = json.loads(body) if body != "" else body
                        params = json.loads(params) if params != "" else params
                        # 从前台拿到需替换的key,转为字典，字典的键存入列表
                        replaceKey = eval(replace_key)
                        replaceKey_key = [x for x in replaceKey]
                        print(replaceKey_key)
                        # 从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                        dependkey = eval(depend_key)
                        # 将所有依赖的接口对应的结果的值通过jsonpath[key]替换出来，加入一个列表中
                        depend_value = []
                        for a in range(len(depend_id)):
                            if int(depend_id[a]) in process_ids:
                                response = "我所依赖的id为" + depend_id[a] + "的接口出错了哦"
                                break
                            else:
                                try:
                                    for i in range(len(depend_id)):
                                        dependid = ProcessApi.objects.get(caseid=depend_id[i])
                                        # 通过id获取依赖接口返回的结果
                                        result = json.loads(dependid.result)
                                        print(result)
                                        # 获取需要替换的jsonpath[key]的结果，转为字典，字典的键放入一个列表存储。
                                        dependkey_a = dependkey[i]
                                        print(dependkey_a)
                                        dependkey_ab = [x for x in dependkey_a]
                                        print(dependkey_ab)
                                        #
                                        for ii in range(len(dependkey_ab)):
                                            dependvalue = jsonpath.jsonpath(result, dependkey_ab[ii])[
                                                dependkey_a[dependkey_ab[ii]]]
                                            print(dependvalue)
                                            if type(dependvalue) is list:
                                                dependvalue = dependvalue[0]
                                            depend_value.append(dependvalue)

                                    params_body = params if replace_position == "params" else body
                                    print("体内容取值开开始。。。。")
                                    replace_value = []
                                    for i in range(len(replaceKey_key)):
                                        replacevalue = jsonpath.jsonpath(params_body, replaceKey_key[i])[
                                            replaceKey[replaceKey_key[i]]]
                                        print(replacevalue)
                                        if type(replacevalue) is list:
                                            replacevalue = replacevalue[0]
                                        replace_value.append(replacevalue)
                                    print(replace_value)
                                    # 将变量params_body转为json字符串，为了之后的字符串替换
                                    params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                                    # 将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                                    for i in range(len(depend_value)):
                                        params_body = params_body.replace(replace_value[i], depend_value[i])
                                    print(params_body)
                                    starttime = time.time()
                                    response = RequestMethod(token).run_main(method, url, params_body, json.dumps(
                                        body)) if replace_position == "params" else RequestMethod(token).run_main(method, url,
                                                                                                       json.dumps(params),params_body)
                                    endtime = time.time()
                                    runtime = round(endtime - starttime, 3)  # 接口执行的消耗时间
                                except TypeError as e:
                                    print("类型错误")
                                    print(e)
                                    response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                                except json.decoder.JSONDecodeError as e:
                                    print("json解析错误")
                                    print(e)
                                    response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"
                                break

                else:
                    try:
                        starttime = time.time()
                        response = RequestMethod(token).run_main(method, url, params, body)
                        endtime = time.time()
                        runtime = round(endtime - starttime, 3)     #接口执行的消耗时间

                    except TypeError as e:
                        print(e)
                        response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                    except json.decoder.JSONDecodeError as e:
                        print(e)
                        response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"

                djson = self.check_greater_less_is_exist(response)
                self.check_result_is_fail(response, caseid)

                id = ProcessApi.objects.get(caseid=caseid)
                data = {"result": djson, "duration": runtime}
                serializer = ProcessApiResponseSerializers(id, data=data)
                # 在获取反序列化的数据前，必须调用is_valid()方法进行验证，验证成功返回True，否则返回False
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                num += 1
                ProcessApiTest.num_progress = round(num / len(content) * 100, )
            # 将{}数据返回给前端
            dic["failcases"] = self.failed_ids
            dic["errors"] = self.failed_num
            ProcessApiTest.failed_num = 0
            ProcessApiTest.failed_ids = []
            return Response(dic)




class ProcessApiResultTest(APIView):

    def get(self, request, format=None):
        '''
        :param request:
        :param format:
        :return: 流程接口异常结果
        '''
        caseids = request.GET.get("caseids", "")
        system = request.GET.get("system","")
        if caseids:
            L = []
            for i in json.loads(caseids):
                apilists = ProcessApi.objects.filter(Q(caseid=i) & Q(system=system)).order_by("sortid")
                for weblist in apilists:
                    data = {
                        "caseid":weblist.caseid,
                        "casename": weblist.casename,
                        "result": weblist.result,
                        "head": weblist.head,
                        "duration": weblist.duration,
                    }
                    L.append(data)
            pageindex = request.GET.get('page', "")
            pagesize = request.GET.get("limit", "")
            pageInator = Paginator(L, pagesize)
            # 分页
            contacts = pageInator.page(pageindex)
            res = []
            for contact in contacts:
                res.append(contact)
            datas = {"code": 0, "msg": "", "count": len(L), "data": res}
            return Response(datas)
        else:
            datas = {"code": 0, "msg": "", "count": 0, "data": []}
            return Response(datas)


