import json
from django.db.models import Q
from ApiTest.models import ProcessApi
from ApiTest.serializers import ProcessApiListSerializers,AddProcessApiSerializers,\
                                ProcessApiBodySerializers,ProcessApiParamsSerializers,ProcessApiHeadSerializers,\
                                ProcessApiDependKeySerializers,ProcessApiDependIdSerializers,\
                                ProcessApiReplaceKeySerializers,ProcessApiReplacePositionSerializers
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


class ProcessApiList(APIView):
    """
    单一接口列表
    """
    def get(self, request, *args, **kwargs):
        casename = request.GET.get("casename", "")     #搜索名字
        belong = request.GET.get("belong", "")              #所属模块
        system = request.GET.get("system", "")              #所属系统
        if casename:
            if belong:
                apilists = ProcessApi.objects.filter(Q(casename__contains=casename) & Q(belong=belong) & Q(system=system))
                if apilists.count() == 0:
                    apilists = ProcessApi.objects.filter(Q(result__contains="error") & Q(result__contains="message") & Q(system=system))
            else:
                apilists = ProcessApi.objects.filter(Q(casename__contains=casename) & Q(system=system))
                if  apilists.count() == 0:
                    apilists = ProcessApi.objects.filter(Q(result__contains="error") & Q(result__contains="message") & Q(system=system))

        elif system:
            if belong:
                apilists = ProcessApi.objects.filter(Q(belong=belong) & Q(system=system)).order_by("sortid")
            else:
                apilists = ProcessApi.objects.filter(system=system).order_by("sortid")

        serializer = ProcessApiListSerializers(apilists, many=True)
        pageindex = request.GET.get('page', 1)  # 页数
        pagesize = request.GET.get("limit", 30)  # 每页显示数量
        pageInator = Paginator(serializer.data, pagesize)
        # 分页
        contacts = pageInator.page(pageindex)
        res = []
        for contact in contacts:
            res.append(contact)
        return Response(data={"code": 0, "msg": "", "count": len(serializer.data), "data": res})


class AddProcessApi(APIView):
    '''
    创建流程接口
    '''
    def parameter_check(self,system):
        """
        验证参数
        """
        L = []
        sortid_queryset = ProcessApi.objects.filter(system=system).values("sortid") #[{"sortid":0},{}]
        for i in sortid_queryset:
            L.append(i.get("sortid"))
        print(L)
        Newsordid = max(L) + 1
        print("最大的排序号为：" + str(Newsordid))
        return Newsordid

    def post(self, request, *args, **kwargs):
        ret = {"code": 1000}
        try:
            data = request.data
            system = data.get("system", "")
            sortid = self.parameter_check(system)
            print(sortid)
            serializer = AddProcessApiSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                ProcessApi.objects.filter(sortid=None).update(sortid=sortid)
                ret["msg"] = "新建流程接口成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "新建流程接口失败"
        return Response(ret)


class UpdateProcessApi(APIView):
    """
    更新单一接口
    """
    def get_object(self, pk):
        try:
            print(pk)
            return ProcessApi.objects.get(caseid=pk)
        except ProcessApi.DoesNotExist:
            raise Http404


    def put(self, request, pk, *args, **kwargs):
        '''
        更新流程接口
        '''
        ret = {"code":1000}
        try:
            snippet = self.get_object(pk)
            serializer = AddProcessApiSerializers(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "编辑失败"
        return Response(ret)

    def get(self, request, pk, *args, **kwargs):
        '''
        编辑责任者
        '''
        ret = {"code":1000}
        try:
            head = request.GET.get("head","")
            depend_key = request.GET.get("depend_key","")
            depend_id = request.GET.get("depend_id","")
            replace_key = request.GET.get("replace_key","")
            replace_position = request.GET.get("replace_position","")
            snippet = self.get_object(pk)
            if head:
                data = {"head":head}
                serializer = ProcessApiHeadSerializers(snippet, data=data)
                ret["msg"] = "编辑责任者成功"
            elif depend_id:
                data = {"depend_id":depend_id}
                serializer = ProcessApiDependIdSerializers(snippet, data=data)
                ret["msg"] = "编辑依赖id成功"
            elif depend_key:
                data = {"depend_key":depend_key}
                serializer = ProcessApiDependKeySerializers(snippet, data=data)
                ret["msg"] = "编辑依赖的key成功"
            elif replace_key:
                data = {"replace_key": replace_key}
                serializer = ProcessApiReplaceKeySerializers(snippet, data=data)
                ret["msg"] = "编辑替换体成功"
            elif replace_position:
                if replace_position == '["params"]':
                    replace_position = 0
                elif replace_position == '["body"]':
                    replace_position = 1
                elif replace_position == '["params","body"]':
                    replace_position = 2
                data = {"replace_position": replace_position}
                serializer = ProcessApiReplacePositionSerializers(snippet, data=data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "编辑失败"
        return Response(ret)



    def post(self, request, pk, *args, **kwargs):
        '''
        如果是params则修改parmas的值，否则修改body的值
        '''
        ret = {"code":1000}
        try:
            snippet = self.get_object(pk)
            try:
                a = request.data["params"]
                serializer = ProcessApiParamsSerializers(snippet, data=request.data)
            except:
                serializer = ProcessApiBodySerializers(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑params/body成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "编辑params/body失败"
        return Response(ret)

class DelProcessApi(APIView):
    """
    删除单一接口
    """
    def get_object(self, pk):
        try:
            return ProcessApi.objects.get(caseid=pk)
        except ProcessApi.DoesNotExist:
            raise Http404

    def delete(self, request, pk, *args, **kwargs):
        #批量删除
        ret = {"code": 1000}
        try:
            if pk == '0':
                for i in json.loads(request.data.get("ids")):
                    print(i)
                    self.get_object(i.get("caseid2")).delete()
                ret["msg"] = "批量删除成功"
            #单个删除
            else:
                snippet = self.get_object(pk)
                snippet.delete()
                ret["msg"] = "单个删除成功"
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "删除失败"
        return Response(ret)