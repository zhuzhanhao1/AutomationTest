import json
import requests
from ApiTest.models import SystemRole
from ApiTest.serializers import SystemRoleSerializers,TokenSerializers,SystemRoleUpdateInfoSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class SystemRoleList(APIView):

    def get(self, request, *args, **kwargs):
        '''
        获取被测系统用户角色列表
        '''
        system_role_info = SystemRole.objects.all()
        serializer = SystemRoleSerializers(system_role_info, many=True)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": serializer.data})

class GetTokenByRole(APIView):

    def get_token(self,role,ip):
        '''
        获取被测系统用户登录的令牌、用户的id
        '''
        try:
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
            print("token：" + str(res))
            return res,id
        except:
            return None,None

    def put(self, request, *args, **kwargs):
        '''
        更新被测系统角色的token
        '''
        ret = {"code": 1000}
        try:
            datas = request.data
            role = json.loads(datas.get("role",""))
            ip = datas.get("ip","")
            for i in role:
                token,id = self.get_token(i,ip)
                data = {"token":token,"ip":ip}
                serializer = TokenSerializers(id,data=data)
                # 在获取反序列化的数据前，必须调用is_valid()方法进行验证，验证成功返回True，否则返回False
                if serializer.is_valid():
                    serializer.save()
                else:
                    ret["code"] = 1001
                    ret['error'] = str(serializer.errors)
                    return Response(ret, status=status.HTTP_400_BAD_REQUEST)
            ret["msg"] = "被测系统Token更新成功"
            return Response(ret, status=status.HTTP_201_CREATED)
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "被测系统Token更新失败"
            return Response(ret)


class UpdateSystemRole(APIView):
    """
    更新被测系统角色信息
    """
    def get_object(self, pk):
        try:
            print(pk)
            return SystemRole.objects.get(identity=pk)
        except SystemRole.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs):
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            # 编辑用户
            serializer = SystemRoleUpdateInfoSerializers(snippet, data=request.data)
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


class AddSystemRole(APIView):

    def get_role_by_identity(self,identity):
        '''
        更具被测系统角色身份获取角色名
        '''
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
        '''
        检查被测系统中用户身份是否存在
        '''
        id = SystemRole.objects.filter(identity=identity)
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
                    serializer.save()
                    ret["msg"] = "添加被测系统角色成功"
                    return Response(ret)
                ret["code"] = 1001
                ret["error"] = str(serializer.errors)
            else:
                ret["code"] = 1001
                ret["error"] = "该身份下已存在用户，请您创建其他身份的用户"
                return Response(ret)
        except:
            ret["code"] = 1001
            ret["error"] = "添加被测系统角色失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)