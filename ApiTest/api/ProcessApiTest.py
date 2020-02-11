import json
import time
import jsonpath
from django.core.paginator import Paginator
from django.db.models import Q
from ApiTest.models import SystemRole, ProcessApi
from ApiTest.serializers import ProcessApiResponseSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ApiTest.common.requestMothod import RequestMethod


class ProcessApiTest(APIView):
    num_progress = 0
    failed_num = 0
    failed_ids = []

    def get(self, request, *args, **kwargs):

        '''
        流程进度
        '''
        try:
            print('show_api----------' + str(self.num_progress))
            # 当进度百分百的时候，需要吧全局变量初始化，以便下次请求的时候进度条是重0开始，否则默认都是百分之百了
            if ProcessApiTest.num_progress == 100:
                ProcessApiTest.num_progress = 0
                return Response(100)
            # 当进度不是百分之百的时候，返回当前进度
            else:
                return Response(ProcessApiTest.num_progress)
        except Exception as e:
            return Response(100)

    def get_token_ip_by_identity(self, identity):
        '''
        获取角色请求令牌和IP地址
        '''
        token = SystemRole.objects.get(identity=identity).token
        ip = SystemRole.objects.get(identity=identity).ip
        return token, ip

    def check_english_greater_less_is_exist(self, response):
        '''
        判断请求体或者响应结果中是否存在<>,将其替换为中文的＜＞，layui数据表格bug，暂且这么处理
        '''
        if type(response) is str:
            if "<" in response or ">" in response:
                print('存在需要替换的符号')
                less = response.replace("<", "＜")
                response_replaced = less.replace(">", "＞")
                return response_replaced
            else:
                return response

        elif type(response) is dict or type(response) is list:
            response = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2)
            if "<" in response or ">" in response:
                print('存在需要替换的符号')
                less = response.replace("<", "＜")
                response_replaced = less.replace(">", "＞")
                return response_replaced
            else:
                return response

        elif type(response) is bool:
            return str(response)

        else:
            print(type(response))
            print(response)
            return response

    def check_chinese_greater_less_is_exist(self, body):
        '''
        判断请求体或者响应结果中是否存在<>,将其替换为中文的＜＞，layui数据表格bug，暂且这么处理
        '''
        if type(body) is str:
            if "＜" in body or "＞" in body:
                print('存在需要替换的符号')
                a = body.replace("＜", "<")
                body_replaced = a.replace("＞", ">")
                return body_replaced
            else:
                return body

        elif type(body) is dict or type(body) is list:
            body = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2)
            if "＜" in body or "＞" in body:
                print('存在需要替换的符号')
                a = body.replace("＜", "<")
                body_replaced = a.replace("＞", ">")
                return body_replaced
            else:
                return body

    def check_result_is_fail(self, result, caseid):
        '''
        错误的接口数
        '''
        try:
            if type(result) is dict:
                result = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
                if "error" in result and "timestamp" in result:
                    self.failed_num += 1
                    self.failed_ids.append(caseid)
                    print(self.failed_ids)
                    return
                return
            elif type(result) is str:
                if "sorry我所依赖的序号为" in result:
                    self.failed_num += 1
                    self.failed_ids.append(caseid)
                    print(self.failed_ids)
        except:
            print("返回结果不是JSON对象,且不是自己抛的异常结果")
            return

    def parameter_check(self, identity, url, method):
        """
        验证参数
        """
        try:
            # 必传参数 method, url, headers
            if not identity or not url or not method:
                return Response({"code": 400, "msg": "参数有误"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"code": 400, "msg": "参数有误"}, status=status.HTTP_400_BAD_REQUEST)

    def depend_params(self, depend_id):
        id = ProcessApi.objects.get(caseid=depend_id)
        return id

    def post(self, request, *args, **kwargs):
        '''
        执行流程接口
        '''
        datas = request.data
        content = json.loads(datas["request"])
        dic = {}
        num = 0
        for i in content:

            print("当前执行第" + str(num) + "号接口:" + i.get("casename", ""))
            caseid = i.get("caseid", "")
            identity = i.get("identity", "")  # 用户身份
            url = i.get("url", "")  # 登录地址
            method = i.get("method", "")  # 请求方式
            params = i.get("params", "")  # query数据
            body = i.get("body", "")  # body数据
            depend_id = i.get("depend_id", "")
            depend_key = i.get("depend_key", "")
            replace_key = i.get("replace_key", "")
            replace_position = i.get("replace_position", "")

            result = self.parameter_check(identity, url, method)
            token, ip = self.get_token_ip_by_identity(identity)  # 根据用户身份获取请求头Token数据
            body = self.check_chinese_greater_less_is_exist(body)
            # 验证请求内容是否存在，不存在则直接返回请求内容缺失
            if result:
                return result
            elif depend_id:
                print("我需要依赖别的接口哦！！！")
                depend_id = depend_id.split(",")

                body = json.loads(body) if body != "" else body
                params = json.loads(params) if params != "" else params
                # 从前台拿到需替换的key,转为字典，字典的键存入列表
                replaceKey = eval(replace_key)
                replaceKey_key = [x for x in replaceKey]
                print("需要替换的key的列表集" + str(replaceKey_key))
                # 从前台拿到需要依赖的key,转为字典
                dependkey = eval(depend_key)
                print("需要依赖的字典集" + str(dependkey))
                # 将所有依赖的接口对应的结果的值通过jsonpath[key]替换出来，加入一个列表中
                depend_value = []  # 定义一个结果集存放依赖的结果
                replace_value = []  # 定义一个结果集存放替换的结果
                replace_list = []
                for a in range(len(depend_id)):
                    if int(depend_id[a]) in self.failed_ids or depend_id[a] in self.failed_ids:
                        print("流程依赖的接口" + str(depend_id[a]) + "出错了")
                        response = "sorry我所依赖的序号为" + depend_id[a] + "的接口出错了哦"
                        runtime = 0
                        break
                    else:
                        print("依赖取值开开始。。。。")
                        dependid = ProcessApi.objects.get(caseid=depend_id[a])
                        # 通过id获取依赖接口返回的结果
                        result = json.loads(dependid.result)
                        print("依赖接口的执行结果" + str(result))

                        # 获取需要替换的jsonpath[key]的结果，转为字典，字典的键放入一个列表存储。
                        if type(dependkey) is list:
                            dependkey_a = dependkey[a]  # 第一个需要依赖的对象dict,{"$.XX":0}
                            dependkey_ab = [x for x in dependkey_a]  # 第一个需要依赖的对象key,["$.XX"]
                        else:
                            dependkey_a = dependkey
                            dependkey_ab = [x for x in dependkey_a]
                        # 通过jsonpath将依赖的值从依赖的接口返回结果中替换出来
                        dependvalue = jsonpath.jsonpath(result, dependkey_ab[0])[dependkey_a[dependkey_ab[0]]]
                        if type(dependvalue) is list:
                            dependvalue = dependvalue[0]
                        depend_value.append(dependvalue)
                        print("所有依赖值的列表集" + str(depend_value))

                        # 替换区域的值，0是Query，1是body
                        replace_area = replaceKey[replaceKey_key[a]]
                        try:
                            if replace_area == 0:
                                # 说明需要替换的位置在Query内,默认索引是0
                                replacevalue = jsonpath.jsonpath(params, replaceKey_key[a])[0]
                            elif replace_area == 1:
                                replacevalue = jsonpath.jsonpath(body, replaceKey_key[a])[0]

                            # 如果替换后的内容仍为列表则再次索引第一个位子
                            if type(replacevalue) is list:
                                replacevalue = replacevalue[0]
                            replace_value.append(replacevalue)
                            replace_list.append(replaceKey[replaceKey_key[a]])
                            print("所有替换值的列表集" + str(replace_value))
                            print("所有替换值的区域集" + str(replace_list))
                        except Exception as e:
                            print("替换值的位置错误")
                            response = "异常的id为:" + str(caseid) + "," + "替换值的位置{xx:" + str(replace_area) + "}错误"
                            break

                        # 当执行到最后一个循环的时候，执行接口请求
                        if a == len(depend_id) - 1:
                            # 如果替换的位置为0，只替换Query中的参数
                            try:
                                if int(replace_position) == 0:
                                    params = json.dumps(params, ensure_ascii=False, sort_keys=True, indent=2)
                                    for area in range(len(replace_list)):
                                        params = params.replace(replace_value[area], depend_value[area])
                                    response = RequestMethod(token).run_main(method, ip + url, params, json.dumps(body))

                                # 如果替换的位置为1，只替换body中的参数
                                elif int(replace_position) == 1:
                                    body = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2)
                                    for area in range(len(replace_list)):
                                        body = body.replace(replace_value[area], depend_value[area])
                                    response = RequestMethod(token).run_main(method, ip + url, json.dumps(params), body)

                                # 如果替换的位置为2，替换query和body中的参数
                                elif int(replace_position) == 2:
                                    params = json.dumps(params, ensure_ascii=False, sort_keys=True, indent=2)
                                    body = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2)
                                    for area in range(len(replace_list)):
                                        if area == 0:
                                            params = params.replace(replace_value[area], depend_value[area])
                                        elif area == 1:
                                            body = body.replace(replace_value[area], depend_value[area])
                                    response = RequestMethod(token).run_main(method, ip + url, params, body)

                            except TypeError as e:
                                print("类型错误")
                                print(e)
                                response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                            except json.decoder.JSONDecodeError as e:
                                print("json解析错误")
                                print(e)
                                response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"

            else:
                try:
                    starttime = time.time()
                    response = RequestMethod(token).run_main(method, ip + url, params, body)
                    endtime = time.time()
                    runtime = round(endtime - starttime, 3)  # 接口执行的消耗时间

                except TypeError as e:
                    print(e)
                    response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                except json.decoder.JSONDecodeError as e:
                    print(e)
                    response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"

            djson = self.check_english_greater_less_is_exist(response)
            print(djson)
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
            print("当前这个循环结束-----------------当前的进度是" + str(ProcessApiTest.num_progress))

        # 将{}数据返回给前端
        dic["failcases"] = self.failed_ids  # 失败的用例列表集
        dic["errors"] = self.failed_num  # 失败的总数
        ProcessApiTest.failed_num = 0
        ProcessApiTest.failed_ids = []
        return Response(dic)


class ProcessApiResultTest(APIView):

    def get(self, request, *args, **kwargs):
        '''
        流程接口异常结果
        '''
        try:
            caseids = request.GET.get("caseids", "")
            system = request.GET.get("system", "")
            if caseids:
                L = []
                for i in json.loads(caseids):
                    apilists = ProcessApi.objects.filter(Q(caseid=i) & Q(system=system)).order_by("sortid")
                    for weblist in apilists:
                        data = {
                            "caseid": weblist.caseid,
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
        except:
            datas = {"code": 1001, "msg": "请求异常", "count": 0, "data": []}
            return Response(datas)
