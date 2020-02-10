import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ApiTest.common.quickMthod import QuickMothod
ret = {"code":1000}

class RunQuickTest(APIView):

    def parameter_check(self, datas):
        """
        验证必传参数 method, url, headers
        """
        try:
            if not datas["Method"] or not datas["addURL"]:
                ret["error"] = "必填参数method或URL不存在"
        except Exception as e:
            ret["error"] = "未知错误"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        '''
        :param request: request.data
        :param format: None
        :return: 接口响应结果，JOSN格式化数据
        '''
        datas = request.data
        method=datas["Method"]
        url=datas["addURL"]
        headers=datas["addmergeheaders"]
        params=datas["addmergeformdatas"]
        body=datas["body"]
        #参数校验
        result = self.parameter_check(datas)
        if result:
            return result
        try:
            response = QuickMothod().run_main(method, url, headers, params, body)
            response = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2)
            return Response(response,status=status.HTTP_200_OK)
        except TypeError as e:
            print(e)
            return Response({"code": 400, "msg": "操作或函数应用于不适当类型的对象"}, status=status.HTTP_400_BAD_REQUEST)
        except json.decoder.JSONDecodeError as e:
            print(e)
            return Response({"code": 400, "msg": "json.loads()读取字符串报错"}, status=status.HTTP_400_BAD_REQUEST)
