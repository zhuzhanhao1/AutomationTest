from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from ApiTest.models import LeftMenu, ChildMenu
from ApiTest.serializers import LeftMenuSerializers, ChildMenuSerializers, ChildMenusSerializers, GetParamsSer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
import json


class MenuTree(APIView):
    '''
    树形菜单
    '''
    def get(self, request, *args, **kwargs):
        queryset = LeftMenu.objects.filter()
        area_list = list(set([x.area for x in queryset]))
        area_list.sort()
        print(area_list)
        l = []
        for i in range(len(area_list)):
            dic = {}
            dic["title"] = area_list[i]
            dic["id"] = i+1
            dic["children"] = []
            l.append(dic)

        queryset = LeftMenu.objects.filter(area="single")
        area_list = list(set([x.title for x in queryset]))
        for i in range(len(area_list)):
            dic = {}
            dic["title"] = area_list[i]
            dic["id"] = i+1
            dic["children"] = []
            l[1]["children"].append(dic)

        queryset = LeftMenu.objects.filter(area="process")
        area_list = list(set([x.title for x in queryset]))
        for i in range(len(area_list)):
            dic = {}
            dic["title"] = area_list[i]
            dic["id"] = i+1
            dic["children"] = []
            l[0]["children"].append(dic)


        queryset = LeftMenu.objects.filter(area="systemeSttings")
        area_list = list(set([x.title for x in queryset]))
        for i in range(len(area_list)):
            dic = {}
            dic["title"] = area_list[i]
            dic["id"] = i+1
            dic["children"] = []
            dic["href"]='http://127.0.0.1:8000/admin/'
            l[2]["children"].append(dic)
        return Response(l)


class MenuListManage(APIView):
    '''
    头部菜单加载左侧菜单
    '''
    def get(self, request, *args, **kwargs):
        dic = {}
        area = request.GET.get("area")
        conn = get_redis_connection('default')
        if area == "single":
            single_menu_list = conn.get("single_menu_list")
            if single_menu_list:
                single_menu_list = json.loads(single_menu_list)
                return Response(single_menu_list)
            else:
                parent_menu = LeftMenu.objects.filter(area="single")
                leftmenu_single_serializer = LeftMenuSerializers(parent_menu, many=True)
                # print(leftmenu_single_serializer.data)
                dic["single"] = leftmenu_single_serializer.data
                title_list = [i.title for i in parent_menu]
                # print(title_list)
                for i in range(1,len(title_list)):
                    ser = ChildMenuSerializers(ChildMenu.objects.filter(classification__title=title_list[i]), many=True).data
                    dic["single"][i]["children"] = ser
                print("访问MySQL拿去数据放入缓存")
                single_menu_list = json.dumps(dic)
                #设置缓存时间一小时
                conn.set("single_menu_list",single_menu_list,3600)

        elif area == "process":
            process_menu_list = conn.get("process_menu_list")
            if process_menu_list:
                process_menu_list = json.loads(process_menu_list)
                return Response(process_menu_list)
            else:
                parent_menu = LeftMenu.objects.filter(area="process")
                leftmenu_single_serializer = LeftMenuSerializers(parent_menu, many=True)
                # print(leftmenu_single_serializer.data)
                dic["process"] = leftmenu_single_serializer.data
                title_list = [i.title for i in parent_menu]
                # print(title_list)
                for i in range(0,len(title_list)):
                    ser = ChildMenuSerializers(ChildMenu.objects.filter(classification__title=title_list[i]), many=True).data
                    dic["process"][i]["children"] = ser
                print("访问MySQL拿去数据放入缓存")
                process_menu_list = json.dumps(dic)
                #设置缓存时间一小时
                conn.set("process_menu_list",process_menu_list,3600)

        elif area == "systemeSttings":
            systemeSttings_menu_list = conn.get("systemeSttings_menu_list")
            if systemeSttings_menu_list:
                systemeSttings_menu_list = json.loads(systemeSttings_menu_list)
                return Response(systemeSttings_menu_list)
            parent_menu = LeftMenu.objects.filter(area="systemeSttings")
            leftmenu_single_serializer = LeftMenuSerializers(parent_menu, many=True)
            # print(leftmenu_single_serializer.data)
            dic["systemeSttings"] = leftmenu_single_serializer.data
            print("访问MySQL拿去数据放入缓存")
            systemeSttings_menu_list = json.dumps(dic)
            # 设置缓存时间一小时
            conn.set("systemeSttings_menu_list", systemeSttings_menu_list, 3600)
        # print(dic)
        return Response(dic)


class MenuTableList(APIView):
    '''
    菜单表格
    根据左侧菜单标题查询子菜单
    '''
    def get(self, request, *args, **kwargs):
        '''
        菜单表格列表
        '''
        title = request.GET.get("title")
        #根据左侧菜单标题查询子菜单
        queryset = ChildMenu.objects.filter(classification__title=title)
        serializer = ChildMenusSerializers(queryset, many=True).data
        pageindex = request.GET.get('page', 1)  # 页数
        pagesize = request.GET.get("limit", 10)  # 每页显示数量
        pageInator = Paginator(serializer, pagesize)
        # 分页
        contacts = pageInator.page(pageindex)
        res = []
        for contact in contacts:
            res.append(contact)
        return Response(data={"code": 0, "msg": "", "count": len(serializer), "data": res})

    def post(self, request, *args, **kwargs):
        '''
        新建子菜单
        '''

        ret = {"code": 1000}
        data = request.data.copy()
        serializer = ChildMenusSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            ret["msg"] = "添加子菜单成功"
            return Response(ret)
        ret["code"] = 1001
        ret["error"] = str(serializer.errors)
        return Response(ret)

    def get_object(self, pk):
        try:
            print(pk)
            return ChildMenu.objects.get(id=pk)
        except ChildMenu.DoesNotExist:
            raise Http404

    def put(self, request, pk, *args, **kwargs):
        '''
        编辑子菜单
        '''
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            # 编辑用户
            serializer = ChildMenusSerializers(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                ret["msg"] = "编辑子菜单成功"
                return Response(ret)
            ret["code"] = 1001
            ret["error"] = str(serializer.errors)
        except:
            ret["code"] = 1001
            ret["error"] = "编辑子菜单失败"
        return Response(ret, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, *args, **kwargs):
        """
        删除子菜单
        """
        ret = {"code": 1000}
        try:
            snippet = self.get_object(pk)
            snippet.delete()
            ret["msg"] = "删除子菜单成功"
        except Exception as e:
            ret["code"] = 1001
            ret["error"] = "删除子菜单失败"
        return Response(ret)


class MenuBelongParams(APIView):
    '''
    获取belong的值
    '''
    def get(self, request, *args, **kwargs):
        system = request.GET.get("system")
        #查询菜单的href中包含所属系统的并且区域是single的
        queryset = ChildMenu.objects.filter(Q(href__contains=system) & Q(area="single"))
        OrderedDict = GetParamsSer(queryset,many=True).data
        dic = {}
        for i in OrderedDict:
            dic[i["nav"]] = i["title"]
        return Response(dic)

