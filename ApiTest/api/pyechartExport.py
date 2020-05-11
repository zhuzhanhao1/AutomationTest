from rest_framework.views import APIView
from rest_framework.response import Response
import json
from pyecharts import options as opts
from pyecharts.charts import Bar


class EchartExport(APIView):

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
        except:
            ret["code"] = 1001
            ret["error"] = "生成报表异常"
        return Response(ret)