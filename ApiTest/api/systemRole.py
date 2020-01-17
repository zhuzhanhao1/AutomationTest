# Create your views here.
import json

import requests
from rest_framework import viewsets
from ApiTest.models import SystemRole
from ApiTest.serializers import SystemRoleSerializers,TokenSerializers,SystemRoleUpdateInfoSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class SystemRoleList(APIView):

    def get(self, request, format=None):
        '''
        :param request:
        :param format:
        :return: 系统用户角色列表
        '''
        system_role_info = SystemRole.objects.all()
        serializer = SystemRoleSerializers(system_role_info, many=True)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": serializer.data})

class GetTokenByRole(APIView):

    def get_token(self,role,ip):
        '''
        :param role: 用户角色名
        :return: 系统用户登录的令牌、系统用户的id
        '''
        id = SystemRole.objects.get(identity=role)
        username = SystemRole.objects.get(identity=role).username
        password = SystemRole.objects.get(identity=role).password
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "loginName": username,
            "password": password
        }
        response = requests.post(url="{0}/adminapi/user/login".format(ip), headers=headers, data=json.dumps(params))
        res = response.json()['accessToken']
        print(res)
        return res,id

    def post(self, request, format=None):
        '''
        :param request: 系统用户的角色名的列表
        :param format:
        :return:
        '''
        datas = request.data
        role = json.loads(datas["role"])
        ip = datas["ip"]
        print(ip)
        for i in role:
            token,id = self.get_token(i,ip)
            data = {"token":token,"ip":ip}
            serializer = TokenSerializers(id,data=data)
            # 在获取反序列化的数据前，必须调用is_valid()方法进行验证，验证成功返回True，否则返回False
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"code": 200, "msg": "操作成功"}, status=status.HTTP_201_CREATED)


class UpdateSystemRole(APIView):
    """
    更新单一接口
    """
    def get_object(self, pk):
        try:
            print(pk)
            return SystemRole.objects.get(identity=pk)
        except SystemRole.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        #编辑用户
        serializer = SystemRoleUpdateInfoSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"code": "200", "msg": "操作成功"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSystemRole(APIView):
    '''
    创建系统用户`
    '''
    def get_role_by_identity(self,identity):
        role = ""
        if identity == "admin":
            role = "单位管理员"
        elif identity == "sysadmin":
            role = "单位管理员"
        elif identity == "ast":
            role = "单位档案员"
        elif identity == "tdradmin":
            role = "数据管理员"
        return role

    def check_identity_is_exist(self,identity):
        id = SystemRole.objects.filter(identity=identity)
        if id.count() > 0:
            return Response({"code":"500","msg":"该身份下已存在用户，请您编辑系统角色信息"})
        else:
            return True

    def post(self, request, format=None):
        '''
        添加系统角色
        :param request:
        :param format:
        :return:
        '''
        data = request.data
        identity = data["identity"]
        res = self.check_identity_is_exist(identity)
        if res == True:
            role = self.get_role_by_identity(identity)
            dic = {}
            dic["identity"] = identity
            dic["system"] = data["system"]
            dic["role"] = role
            dic["username"] = data["username"]
            dic["password"] = data["password"]

            serializer = SystemRoleSerializers(data=dic)
            if serializer.is_valid():
                #.save()是调用SnippetSerializer中的create()方法
                serializer.save()
                return Response(data={"code": "201", "msg": "操作成功"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return res
