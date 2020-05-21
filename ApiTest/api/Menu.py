from django.core.paginator import Paginator
from django.db.models import Q

from ApiTest.models import LeftMenu, ChildMenu
from ApiTest.serializers import LeftMenuSerializers, ChildMenuSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
import json


ret = {"code":1000}

class MenuList(APIView):
    '''
    左侧二级菜单
    '''
    def get_level_one_menu(self):
        '''
        头部导航菜单-dict格式-一级菜单
        '''
        left = {}
        leftmenu_single = LeftMenu.objects.filter(area="single")
        leftmenu_single_serializer = LeftMenuSerializers(leftmenu_single, many=True)

        leftmenu_process = LeftMenu.objects.filter(area="process")
        leftmenu_process_serializer = LeftMenuSerializers(leftmenu_process, many=True)

        leftmenu_systemeSttings = LeftMenu.objects.filter(area="systemeSttings")
        leftmenu_systemeSttings_serializer = LeftMenuSerializers(leftmenu_systemeSttings, many=True)

        #从点击头部导航显示左侧导航
        left["single"] = leftmenu_single_serializer.data
        left['process'] = leftmenu_process_serializer.data
        left["systemeSttings"] = leftmenu_systemeSttings_serializer.data
        print(left)
        return left

    def get(self, request, *args, **kwargs):
        '''
        二级菜单参数，评级一级菜单
        '''

        conn = get_redis_connection('default')
        menu_list = conn.get("menu")
        if menu_list:
            print("从缓存拿数据")
            menu_list = json.loads(menu_list)
            return Response(menu_list)
        else:
            print("访问MySQL拿去数据放入缓存")
            try:
                left = self.get_level_one_menu()

                ermsapi = ChildMenu.objects.filter(classification__title="ERMS接口测试")
                ermsapi_erializer = ChildMenuSerializers(ermsapi, many=True)

                tdrapi = ChildMenu.objects.filter(classification__title="TDR接口测试")
                tdrapi_erializer = ChildMenuSerializers(tdrapi, many=True)

                ermsprocess = ChildMenu.objects.filter(classification__title="ERMS接口流程测试")
                ermsprocess_erializer = ChildMenuSerializers(ermsprocess, many=True)

                tdrprocess = ChildMenu.objects.filter(classification__title="TDR接口流程测试")
                tdrprocess_erializer = ChildMenuSerializers(tdrprocess, many=True)

                #拼接二级菜单到主菜单
                left["single"][1]['children'] = ermsapi_erializer.data
                left["single"][2]['children'] = tdrapi_erializer.data
                left['process'][0]['children'] = ermsprocess_erializer.data
                left['process'][1]['children'] = tdrprocess_erializer.data

                menu_list = json.dumps(left)
                #设置缓存时间一小时
                conn.set("menu",menu_list,3600)

                return Response(left)
            except Exception as e:
                ret["code"] = 1001
                ret["error"] = "请检查后台代码"
                return ret

    def post(self, request, *args, **kwargs):
        '''
        新建二级菜单，暂时通过admin创建，暂放
        '''
        serializer = ChildMenuSerializers(data=request.data)
        if serializer.is_valid():
            # .save()是调用SnippetSerializer中的create()方法
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                print("从缓存拿数据")
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
                print("从缓存拿数据")
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
                print("从缓存拿数据")
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



class MenuTable(APIView):
    '''
    菜单表格
    根据左侧菜单标题查询子菜单
    '''
    def get(self, request, *args, **kwargs):
        title = request.GET.get("title")
        #根据左侧菜单标题查询子菜单
        queryset = ChildMenu.objects.filter(classification__title=title)
        serializer = ChildMenuSerializers(queryset, many=True).data
        pageindex = request.GET.get('page', 1)  # 页数
        pagesize = request.GET.get("limit", 10)  # 每页显示数量
        pageInator = Paginator(serializer, pagesize)
        # 分页
        contacts = pageInator.page(pageindex)
        res = []
        for contact in contacts:
            res.append(contact)
        return Response(data={"code": 0, "msg": "", "count": len(serializer), "data": res})


class ChildMenuList(APIView):
    '''
    zhi
    '''
    def post(self, request, *args, **kwargs):
        ret = {"code": 1000}
        data = request.data
        serializer = ChildMenuSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            ret["msg"] = "添加友情链接成功"
            return Response(ret)
        ret["code"] = 1001
        ret["error"] = str(serializer.errors)
        return Response(ret)

