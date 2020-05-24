import json
import requests
from django.core.paginator import Paginator
from ApiTest.models import SystemRole
from ApiTest.serializers import SystemRoleSerializers,TokenSerializers,RoleSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SystemRoleList(APIView):
    '''
        系统角色
    '''
    def get(self, request, *args, **kwargs):
        '''
            获取被测系统用户角色列表
        '''
        system = request.GET.get("system")
        if system:
            system_role_info = SystemRole.objects.filter(system=system)
            if system_role_info:
                serializer = SystemRoleSerializers(system_role_info, many=True)
                pageindex = request.GET.get('page', 1)  # 页数
                pagesize = request.GET.get("limit", 10)  # 每页显示数量
                pageInator = Paginator(serializer.data, pagesize)
                # 分页
                contacts = pageInator.page(pageindex)
                res = []
                for contact in contacts:
                    res.append(contact)
                return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": res})
            else:
                return Response(data={"code": 0, "msg": "", "count": 0, "data": []})
        else:
            return Response(data={"code": 0, "msg": "", "count": 0, "data": []})

    def get_object(self, pk):
        try:
            print(pk)
            return SystemRole.objects.get(id=pk)
        except SystemRole.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs):
        """
            更新被测系统角色信息
        """
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            # 编辑用户
            serializer = SystemRoleSerializers(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑被测系统角色信息成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "编辑被测系统角色信息失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)


    def check_identity_is_exist(self, role):
        '''
            检查被测系统中用户身份是否存在
        '''
        id = SystemRole.objects.filter(role=role)
        if id.count() > 0:
            return
        else:
            return True


    def post(self, request, *args, **kwargs):
        '''
            添加被测系统角色
        '''
        ret = {"code": 1000}
        try:
            # QueryDict
            data = request.data
            role = data["role"]
            res = self.check_identity_is_exist(role)
            if res == True:
                serializer = SystemRoleSerializers(data=data)
                if serializer.is_valid():
                    serializer.save()
                    ret["msg"] = "添加角色成功"
                    return Response(ret)
                ret["code"] = 1001
                ret["error"] = str(serializer.errors)
            else:
                ret["code"] = 1001
                ret["error"] = "该角色已存在"
            return Response(ret)
        except Exception as e:
            print(e)
            ret["code"] = 1001
            ret["error"] = "添加角色失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
            删除子角色
        """
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            snippet.delete()
            ret["msg"] = "删除角色成功"
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "删除角色失败"
        return Response(ret)


class SystemRoleToken(APIView):

    def get_token(self,pk):
        '''
            获取被测系统用户登录的令牌、用户的id
        '''
        try:
            obj = SystemRole.objects.get(id=pk)
            headers = {
                "Content-Type": "application/json"
            }
            params = {
                "loginName": obj.username,
                "password": obj.password
            }
            response = requests.post(url="{0}/adminapi/user/login".format(obj.ip), headers=headers, data=json.dumps(params))
            token = response.json()['accessToken']
            print("成功返回token：" + str(token))
            return token,obj
        except:
            return None,None

    def put(self, request, pk, *args, **kwargs):
        '''
            更新被测系统角色的token
        '''
        ret = {"code": 1000}
        try:
            token,obj = self.get_token(pk)
            if not token:
                ret["code"] = 1001
                ret["error"] = "被测系统Token更新失败"
                return Response(ret)
            data = {"token":token}
            serializer = TokenSerializers(obj,data=data)
            # 在获取反序列化的数据前，必须调用is_valid()方法进行验证，验证成功返回True，否则返回False
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "被测系统Token更新成功"
                return Response(ret, status=status.HTTP_201_CREATED)
            else:
                ret["code"] = 1001
                ret['error'] = str(serializer.errors)
                return Response(ret, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            ret["code"] = 1001
            ret["error"] = "被测系统Token更新失败"
            return Response(ret)

    def get(self, request, *args, **kwargs):
        '''
            获取角色列表
        '''
        system = request.GET.get("system")
        queryset = SystemRole.objects.filter(system=system)
        OrderedDict = RoleSerializers(queryset,many=True).data
        L = [i["role"] for i in OrderedDict]
        return Response(L)

