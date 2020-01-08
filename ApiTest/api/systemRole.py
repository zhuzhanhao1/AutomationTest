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
                print(serializer.data)
                print(type(serializer.data))
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
        serializer = SystemRoleUpdateInfoSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"code": "200", "msg": "操作成功"},status=status.HTTP_200_OK)
        print(serializer.errors)
        print(type(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

