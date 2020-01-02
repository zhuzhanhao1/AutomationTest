# Create your views here.
import json

import xlrd
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render

from ApiTest.common.dingDingNotice import send_singleapi_link, send_ding
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


class PublicApiDingDingNotice(APIView):

    def get(self, request, format=None):
        '''
        :param request: id
        :return: 钉钉消息
        '''
        ids = request.GET.get("caseid","").split(",")[:-1]
        isporcess = request.GET.get("isprocess","")
        for id in ids:
            if isporcess == "no":
                data = SingleApi.objects.get(caseid=id)
                send_singleapi_link("singleid",id, data.casename + "-详情-->")
            elif isporcess == "yes":
                data = ProcessApi.objects.get(caseid=id)
                send_singleapi_link("processid",id, data.casename + "-详情-->")
            send_ding(data.head+"-看消息",data.head)
        return Response({"code": "200", "msg": "操作成功"},status=status.HTTP_200_OK)


class PublicApiImport(APIView):

    def post(self, request, format=None):
        '''
        :param request:
        :return: 导入数据
        '''
        f = request.FILES.get('file')   #sheet名
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            try:
                with transaction.atomic():  # 控制数据库事务交易
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        print(rowVlaues)
                        SingleApi.objects.create(caseid=rowVlaues[0],identity=rowVlaues[1],casename=rowVlaues[2],url=rowVlaues[3],
                                            belong=rowVlaues[4],method=rowVlaues[5],head=rowVlaues[6],system=rowVlaues[7],sortid=rowVlaues[8])
            except:
                return Response({"status": 400, "message": "解析excel文件或者数据插入错误"})
            return Response({"code": "200", "msg": "操作成功"},status=status.HTTP_200_OK)
        else:
            return Response({"status": 400, "message": "上传文件类型错误"})
