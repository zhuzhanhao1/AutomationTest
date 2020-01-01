# Create your views here.
import json
from django.db.models import Q
from ApiTest.models import SingleApi,ProcessApi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PublicApiSort(APIView):
    def post(self, request, format=None):
        '''
        :param request: 【排序后id的顺序】、属于什么模块、属于什么系统、是单一接口的还是流出接口的
        :param format:
        :return: 将排序号按照id的顺序重新生成
        '''
        data = request.data
        caseids = json.loads(data["caseids"])
        belong = data["belong"]
        system = data["system"]
        type = data["type"]
        if type == "single":
            if belong:
                all = SingleApi.objects.filter(Q(belong=belong) & Q(system=system))
            else:
                all = SingleApi.objects.filter(system=system)
            l = []
            for i in all:
                l.append(i.sortid)
            l.sort() #有序排序，从小到大
            flag = 0
            for d in caseids:
                SingleApi.objects.filter(caseid=d).update(sortid=l[flag])
                flag += 1
            return Response({"code": "200", "msg": "操作成功"},status=status.HTTP_200_OK)
        else:
            if belong:
                all = ProcessApi.objects.filter(Q(belong=belong) & Q(system=system))
            else:
                all = ProcessApi.objects.filter(system=system)
            l = []
            for i in all:
                l.append(i.sortid)
            l.sort()
            flag = 0
            for d in caseids:
                ProcessApi.objects.filter(caseid=d).update(sortid=l[flag])
                flag += 1
            return Response({"code": "200", "msg": "操作成功"},status=status.HTTP_200_OK)