from django.db import transaction
from django.db.models import Q
from ApiTest.common.dingDingNotice import send_singleapi_link, send_ding
from ApiTest.models import SingleApi, ProcessApi,Head
from ApiTest.serializers import Headser
from rest_framework.views import APIView
from rest_framework.response import Response
import json, xlrd
from pyecharts.globals import CurrentConfig
#设置src="../static/js/echarts.min.js"加载在本地路径
CurrentConfig.ONLINE_HOST  = "../static/js/"
from pyecharts import options as opts
from pyecharts.charts import Bar

class PublicApiSort(APIView):
    '''
        排序
    '''
    def post(self, request, *args, **kwargs):
        '''
        :param request: 【排序后id的顺序】、属于什么模块、属于什么系统、是单一接口的还是流程接口的
        :return: 将排序号按照id的顺序重新生成
        '''
        ret = {"code": 1000}
        data = request.data
        caseids = json.loads(data.get("caseids", ""))
        belong = data.get("belong", "")
        system = data.get("system", "")
        type = data.get("type", "")
        flag = 0
        try:
            if type == "single":
                if belong:
                    all = SingleApi.objects.filter(Q(belong=belong) & Q(system=system))
                else:
                    all = SingleApi.objects.filter(system=system)
                l = []
                for i in all:
                    l.append(i.sortid)
                l.sort()  # 有序排序，从小到大
                for d in caseids:
                    SingleApi.objects.filter(caseid=d).update(sortid=l[flag])
                    flag += 1
            elif type == "process":
                if belong:
                    all = ProcessApi.objects.filter(Q(belong=belong) & Q(system=system))
                else:
                    all = ProcessApi.objects.filter(system=system)
                l = []
                for i in all:
                    l.append(i.sortid)
                l.sort()
                for d in caseids:
                    ProcessApi.objects.filter(caseid=d).update(sortid=l[flag])
                    flag += 1

            ret["msg"] = "排序成功"
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "排序失败"
        return Response(ret)

class PublicApiDingDingNotice(APIView):
    '''
        钉钉通知
    '''
    def update_date(self):
        pass

    def get_phone_by_user(self,head):
        obj = Head.objects.get(user=head)
        return obj.phone

    def get(self, request, *args, **kwargs):
        '''
        发送钉钉消息
        '''
        ret = {"code": 1000}
        try:
            ids = request.GET.get("caseid", "").split(",")[:-1]
            isporcess = request.GET.get("isprocess", "")
            for id in ids:
                if isporcess == "no":
                    data = SingleApi.objects.get(caseid=id)
                    phone = self.get_phone_by_user(data.head)
                    send_singleapi_link("singleid", id, data.casename + "-详情-->")
                elif isporcess == "yes":
                    data = ProcessApi.objects.get(caseid=id)
                    phone = self.get_phone_by_user(data.head)
                    send_singleapi_link("processid", id, data.casename + "-详情-->")
                send_ding(phone + "-看消息", phone)
            ret["msg"] = 1000
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "发送钉钉信息失败"
        return Response(ret)

class PublicApiImport(APIView):
    '''
        导入单一接口数据
    '''
    def post(self, request, *args, **kwargs):
        '''
        :param request:
        :return: 导入数据
        '''
        ret = {"code": 1000}
        f = request.FILES.get('file')  # sheet名
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
                        SingleApi.objects.create(caseid=rowVlaues[0], identity=rowVlaues[1],
                                                 casename=rowVlaues[2], url=rowVlaues[3],
                                                 belong=rowVlaues[4], method=rowVlaues[5],
                                                 head=rowVlaues[6], system=rowVlaues[7],
                                                 sortid=rowVlaues[8])
                        ret["msg"] = 1000
            except:
                ret["code"] = 1001
                ret["error"] = "解析excel文件或者数据插入错误"
            return Response(ret)
        else:
            ret["code"] = 1001
            ret["error"] = "所选文件必须是xlsx、xls格式"
            return Response(ret)

class EchartExport(APIView):
    '''
        echar图表
    '''
    def post(self, request, *args, **kwargs):
        '''
        导出Echart报表
        '''
        ret = {"code": 1000}
        datas = request.data
        content = json.loads(datas.get("request", ""))
        url_list = []
        duration_list = []
        for i in content:
            url_list.append(i["url"].split("/")[-1])
            duration_list.append(i["duration"])
        print(url_list)
        duration_list = [0 if i==None else i for i in duration_list]
        print(duration_list)
        try:
            # 纵向柱状图
            c = (
                Bar()
                    .add_xaxis(url_list)
                    .add_yaxis("Duration", duration_list)
                    .set_global_opts(
                    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
                    title_opts=opts.TitleOpts(title="接口响应时长分布图", subtitle="右上角图标可切换折线图哦！"),
                    toolbox_opts=opts.ToolboxOpts(),
                    legend_opts=opts.LegendOpts(is_show=False),
                    datazoom_opts=opts.DataZoomOpts(),

                )
                .render("./ApiTest/templates/pyechartReport.html")
            )
            ret["msg"] = "生成报表成功"
        except Exception as e:
            print(e)
            ret["code"] = 1001
            ret["error"] = "生成报表异常"
        return Response(ret)

class HeadList(APIView):
    '''
        责任者
    '''
    def get(self, request, *args, **kwargs):
        query_set = Head.objects.filter()
        ser = Headser(query_set,many=True).data
        # dic = {}
        # for i in ser:
        #     dic[i["user"]] = i["phone"]
        # print(dic)
        head_list = [i["user"] for i in ser]
        return Response(head_list)
