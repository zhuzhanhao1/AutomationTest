from rest_framework import status
from ApiTest.models import Link,Testurl
from ApiTest.serializers import LinkSerializers,TesturlSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
import json

class LinkList(APIView):

    def get(self, request, *args,**kwargs):
        '''
        友情链接列表
        '''
        link_list = Link.objects.all()
        serializer = LinkSerializers(link_list, many=True)
        pageindex = request.GET.get('page', 1)  # 页数
        pagesize = request.GET.get("limit", 10)  # 每页显示数量
        pageInator = Paginator(serializer.data, pagesize)
        # 分页
        contacts = pageInator.page(pageindex)
        res = []
        for contact in contacts:
            res.append(contact)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": res})


    def post(self,request,*args,**kwargs):
        '''
        添加友情链接
        '''
        ret = {"code":1000}
        try:
            body = json.loads(request.body)
            print(body)
            serializer = LinkSerializers(data=body)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "添加友情链接成功"
                return Response(ret)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            ret["code"] = 1001
            ret["error"] = "添加友情链接失败"
        return Response(ret)

    def put(self,request,*args,**kwargs):
        '''
        编辑友情链接
        '''
        ret = {"code":1000}
        try:
            pk = kwargs.get("pk")
            obj = Link.objects.filter(id=pk).first()
            serializer = LinkSerializers(instance=obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑友情链接成功"
                return Response(ret, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "编辑友情链接失败"
        return Response(ret)


class TesturlList(APIView):

    def get(self, request):
        '''
        日常所需测试网址列表
        '''
        testurl_list = Testurl.objects.all()
        serializer = TesturlSerializers(testurl_list, many=True)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": serializer.data})

