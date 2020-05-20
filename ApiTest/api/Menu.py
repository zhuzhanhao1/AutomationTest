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
            print(menu_list)
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
                print(conn.get("menu"))

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

