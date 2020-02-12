import json
from django.db.models import Q
from ApiTest.models import SingleApi
from ApiTest.serializers import SingleApiSerializers,SingleApiParamsSerializers,SingleApiBodySerializers,SingleApiHeadSerializers
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SingleApiDetail(APIView):
    """
    获取单一接口详情
    """
    def get_object(self, pk):
        try:
            return SingleApi.objects.get(caseid=pk)
        except SingleApi.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        snippet = self.get_object(pk)
        serializer = SingleApiSerializers(snippet)
        return Response(serializer.data)


class SingleApiList(APIView):
    """
    单一接口列表
    """
    def get(self, request, *args ,**kwargs):

        casename = request.GET.get("casename", "")          #搜索名字
        belong = request.GET.get("belong", "")              #所属模块
        system = request.GET.get("system", "")              #所属系统

        if casename:
            if belong:
                apilists = SingleApi.objects.filter(Q(casename__contains=casename) & Q(belong__contains=belong) & Q(system=system))
                if apilists.count() == 0:
                    apilists = SingleApi.objects.filter(Q(result__contains="error") & Q(result__contains="message") & Q(system=system))
            else:
                apilists = SingleApi.objects.filter(Q(casename__contains=casename) & Q(system=system))
                if  apilists.count() == 0:
                    apilists = SingleApi.objects.filter(Q(result__contains="error") & Q(result__contains="message") & Q(system=system))

        elif system:
            if belong:
                apilists = SingleApi.objects.filter(Q(belong__contains=belong) & Q(system=system)).order_by("sortid")
            else:
                apilists = SingleApi.objects.filter(system=system).order_by("sortid")

        serializer = SingleApiSerializers(apilists, many=True)
        pageindex = request.GET.get('page', 1)      # 页数
        pagesize = request.GET.get("limit", 30)     # 每页显示数量
        pageInator = Paginator(serializer.data, pagesize)
        # 分页
        contacts = pageInator.page(pageindex)
        res = []
        for contact in contacts:
            res.append(contact)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": res})


class AddSingleApi(APIView):

    def parameter_check(self,system):
        """
        验证参数
        """
        L = []
        sortid_queryset = SingleApi.objects.filter(system=system).values("sortid") #[{"caseid":0},{}]
        for i in sortid_queryset:
            L.append(i.get("sortid"))
        Newsordid = max(L) + 1
        print("最大的排序号为：" + str(Newsordid))
        return Newsordid

    def post(self, request, *args, **kwargs):
        '''
        创建单一接口
        '''
        ret = {"code": 1000}
        try:
            data = request.data
            system = data.get("system","")
            sortid = self.parameter_check(system)

            serializer = SingleApiSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                SingleApi.objects.filter(sortid=None).update(sortid=sortid)
                ret["msg"] = "新建单一接口成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "新建单一接口失败"
        return Response(ret)


class UpdateSingleApi(APIView):
    """
    更新单一接口
    """
    def get_object(self, pk):
        try:
            return SingleApi.objects.get(caseid=pk)
        except SingleApi.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs):
        '''
        更新单一接口
        '''
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            serializer = SingleApiSerializers(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑单一接口成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "编辑单一接口失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        '''
        编辑责任者
        '''
        ret = {"code": 1000}
        try:
            head = request.GET.get("head","")
            snippet = self.get_object(pk)
            serializer = SingleApiHeadSerializers(snippet, data={"head":head})
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑责任者成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "编辑责任者失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, pk, *args, **kwargs):
        '''
        如果是params则修改parmas的值，否则修改body的值
        '''
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            try:
                serializer = SingleApiParamsSerializers(snippet, data=request.data)
            except:
                serializer = SingleApiBodySerializers(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑params/body成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "编辑params/body失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)

class DelSingleApi(APIView):

    def get_object(self, pk):
        try:
            return SingleApi.objects.get(caseid=pk)
        except SingleApi.DoesNotExist:
            raise Http404

    def delete(self, request, pk, *args, **kwargs):
        """
        删除单一接口，批量删除单一接口
        根据PK来区分
        """
        ret = {"code": 1000}
        try:
            if pk == '0':
                for i in json.loads(request.data['ids']):
                    self.get_object(i).delete()
                ret["msg"] = "批量删除成功"
            else:
                snippet = self.get_object(pk)
                snippet.delete()
                ret["msg"] = "单个删除成功"
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "删除失败"
        return Response(ret)


class SearchSingleApi(APIView):

    def get(self, request, *args, **kwargs):
        '''
        检索包含的名称、路径、负责人的列表字典
        '''
        ret = {"code": 1000}
        try:
            data = request.GET.get("key", "")
            if data:
                apilist = SingleApi.objects.filter(Q(casename__contains=data)| Q(belong__contains=data) | Q(url__contains=data) | Q(head__contains=data))
            else:
                apilist = SingleApi.objects.filter()
            serializer = SingleApiSerializers(apilist, many=True)
            pageindex = request.GET.get('page', 1)  # 页数
            pagesize = request.GET.get("limit", 10)  # 每页显示数量
            pageInator = Paginator(serializer.data, pagesize)
            contacts = pageInator.page(pageindex)
            res = []
            for contact in contacts:
                res.append(contact)
            return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": res})
        except Exception as e:
            ret["code"] = 1001
            ret["msg"] = "检索列表返回失败"
        return Response(ret)


