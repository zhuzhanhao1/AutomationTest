from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect
from ApiTest.models import SingleApi, ProcessApi
from django.contrib import auth
import requests

role = {"ast":"单位档案员","sysadmin":"系统管理员","admin":"单位管理员","tdradmin": "数据管理员"}
erms_role = {"ast":"单位档案员","sysadmin":"系统管理员","admin":"单位管理员"}
tdr_role = {"tdradmin": "数据管理员"}

ermsapi = {
    "unit": "单位接口",
    "dept": "部门管理接口",
    "user": "用户管理接口",
    "record": "Record接口",
    "policy": "保留处置策略接口",
    "navigation": "导航管理接口",
    "data_form/year_check_form": "年检表单特有功能管理接口",
    "data_form": "数据表单管理接口",
    "data_form_config": "数据表单配置管理接口",
    "file_plan": "文件计划管理接口",
    "document": "文档管理接口",
    "attribute_mapping_scheme": "映射规则接口",
    "volume": "案卷管理接口",
    "archives": "档案管理接口",
    "class": "类目模块接口",
    "report": "统计表报模块接口",
    "deposit_form": "续存记录接口",
    "view": "视图自定义接口",
    "acl": "访问控制策略管理",
    "resource": "资源管理接口",
    "common_folder": "通用文件夹管理接口",
    "category": "门类模块接口",
    "admin": "admin平台接口",
    "metadata": "元数据平台接口",
    "transfer_form":"移交表单管理接口"
}

tdrapi = {
    "user":"用户管理接口",
    "unit":"单位接口",
    "common":"公共操作相关接口",
    "metadata":"元数据平台接口",
    "category":"门类模块接口",
    "appraisal_record":"鉴定记录接口",
    "appraisal_task":"鉴定任务接口",
    "resource": "资源管理接口",
    "retrieval_archives": "调卷单内档案详情",
    "view": "视图自定义接口",
    "report": "统计报表模块接口",
    "archives": "档案管理接口",
    "using": "档案利用接口",
    "volume": "案卷管理接口",
    "attribute_mapping_scheme": "映射规则接口",
    "document": "文档管理接口",
    "common_folder": "文件夹接口",
    "data_form_config": "数据表单配置管理接口",
    "data_form": "数据表单管理接口",
    "warehouse": "库房接口",
    "warehouseLayer": "库房层接口",
    "warehouse_address": "库房存址接口",
    "workflow": "工作流引擎接口",
    "navigation": "导航管理接口",
    "file_retrieval": "实体调卷管理接口",
    "usage_archives": "利用档案接口",
    "borrowing_apply": "借阅申请接口",
    "borrowing_apply_archives": "借阅档案申请接口",
    "subject_relation": "专题档案接口",
    "record": "Record接口",
    "admin":"admin平台接口",
    "subject":"专题接口",
    "department":"部门管理接口"
}

erms_process_api = {
    "login": "登录流程",
    "data_form_config": "数据表单配置流程",
    "report": "统计报表配置流程",
    "policy": "保留处置策略流程",
    "category": "类目保管期限流程",
    "acl": "访问控制策略流程",
    "view": "视图自定义流程",
    "document_collection":"文件收集流程",
    "filing": "文件整理流程"

}

tdr_process_api = {
    "login":"登录过程接口"
}


# 用户登录
def login_views(request):
    # if request.POST:
    #     username = request.POST.get('username',"")
    #     password = request.POST.get('password',"")
    #     print(username,password)
    #     user = auth.authenticate(username=username,password=password)  #认证给出的用户名和密码
    #     if user is not None and user.is_active:    #判断用户名和密码是否有效
    #         auth.login(request, user)
    #         request.session['user'] = username  #跨请求的保持user参数
    #         print(request.session)
    #         response = HttpResponseRedirect('/index/')
    #         return response
    #     else:
    #         return HttpResponse("账户或者密码错误，请检查")
    return render(request, 'lgoindingding.html')


def dingding_login_views(request):
    """登录验证"""

    if request.method == "GET":
        ##########二维码认证登录#############
        code = request.GET.get('code', )
        appId = 'dingoa6if6q5jqpwb0sndx'
        appSecret = 'bpipZUwfOxppbNHfIJ8gmwmFClBfOmBnteUWPM4mmmXXNXxRTx_NznlxpC8M0F_1'

        token = requests.get(
            'https://oapi.dingtalk.com/sns/gettoken?appid={appId}&appsecret={appSecret}'.format(appId=appId,appSecret=appSecret))
        access_token = token.json()["access_token"]

        tmp_auth_code = requests.post(
            "https://oapi.dingtalk.com/sns/get_persistent_code?access_token={access_token}".format(
                access_token=access_token),
            json={
                "tmp_auth_code": code
            })
        tmp_code = tmp_auth_code.json()
        print(tmp_code)

        openid = tmp_code['openid']
        persistent_code = tmp_code['persistent_code']
        sns_token_request = requests.post(
            "https://oapi.dingtalk.com/sns/get_sns_token?access_token={access_token}".format(access_token=access_token),
            json={
                "openid": openid,
                "persistent_code": persistent_code
            })

        sns_token = sns_token_request.json()['sns_token']
        print(sns_token)

        user_info_request = requests.get(
            'https://oapi.dingtalk.com/sns/getuserinfo?sns_token={sns_token}'.format(sns_token=sns_token))

        user_info = user_info_request.json()['user_info']
        print(user_info)

        user = auth.authenticate(username=user_info["nick"],password=user_info["unionid"])  #认证给出的用户名和密码
        print(user)
        if user is not None and user.is_active:    #判断用户名和密码是否有效
            auth.login(request, user)
            request.session['username'] = user_info["nick"]  #跨请求的保持user参数
            request.session.set_expiry(86400)  # 设置登录过期时间
            print(request.session)
        return redirect('/index/')
        # unionid = user_info.get('unionid')
        # print(unionid)
        # return HttpResponse("ok")
        # user_obj = UserInfo.objects.filter(unionid=unionid).first()
        # request.session['username'] = user_obj.username  # 登录成功后，用户登录信息存>放于session
        # request.session.set_expiry(86400)  # 设置登录过期时间
        # content = {'code': 0,
        #            'msg': 'success',
        #            'user_info': {
        #                'user_id': user_obj.id,
        #                'username': user_obj.username,
        #                'user_iphone': user_obj.phone,
        #                'user_email': user_obj.email,
        #                'user': user_obj.user,
        #                'D_user': user_obj.D_user
        #            }
        #            }
        # ####################################
        # content = {'code': 0, 'msg':'success',}
        # return JsonResponse(data=content,status=status.HTTP_200_OK)
    else:
        return render(request, 'login.html')

def logout_views(request):
    auth.logout(request)
    return render(request, 'login.html')


def index_views(request):
    '''
    首页html
    '''
    return render(request, 'index.html')


def home_views(request):
    '''
    首页内嵌ifame
    '''
    global role
    return render(request, 'search.html',{"role":role})


def singleapi_views(request):
    '''
    单一接口html
    '''
    global erms_role,tdrapi,tdr_role,ermsapi
    belong = request.GET.get("belong", "")
    system = request.GET.get("system", "")

    if system == "erms":
        '''
            belong_key:所属模块的键、英文名
            belong:所属模块的值、中文名
            system:所属系统
            role:角色对象
            apinav:新建、编辑所属模块的select值
        '''
        #如果belong存在,只返回belong的值
        for i in ermsapi:
            if belong == i:
                L = []
                belong_value = ermsapi.get(i,"")
                L.append(belong_value)
                return render(request, "singleApi.html",{"belong_key":belong,"belong": belong_value, "system": system,"role":erms_role,"apinav":L})
        #如果belong不存在，返回导航的总列表
        l = []
        for a in ermsapi:
            l.append(ermsapi.get(a))
        return render(request, "singleApi.html",{"system": system,"role":erms_role,"apinav":l})

    elif system == "tdr":
        # 如果belong存在,只返回belong的值
        for i in tdrapi:
            if belong == i:
                L = []
                belong_value = tdrapi.get(i,"")
                L.append(belong_value)
                return render(request, "singleApi.html",{"belong_key":belong,"belong": belong_value, "system": system,"role":tdr_role,"apinav":L})
        # 如果belong不存在，返回导航的总列表
        l  = []
        for a in tdrapi:
            l.append(tdrapi.get(a))
        return render(request, "singleApi.html",{"system": system,"role":tdr_role,"apinav":l})


def processapi_views(request):
    '''
    单一接口html
    '''
    global erms_role,tdr_role,erms_process_api
    belong = request.GET.get("belong", "")
    system = request.GET.get("system", "")
    # sortid = AddProcessApi().parameter_check(system)
    if system == "erms":
        #如果belong存在,只返回belong的值
        for i in erms_process_api:
            if belong == i:
                L = []
                belong_value = erms_process_api.get(i,"")
                L.append(belong_value)
                return render(request, "processApi.html",
                              {"belong_key":belong,"belong": belong_value,
                                "system": system,"role":erms_role,"apinav":L})
        #如果belong不存在，返回导航的总列表
        l = []
        for a in erms_process_api:
            l.append(erms_process_api.get(a))
        return render(request, "processApi.html",
                      {"system": system,"role":erms_role,"apinav":l})

    elif system == "tdr":
        #如果belong存在,只返回belong的值
        for i in tdr_process_api:
            if belong == i:
                L = []
                belong_value = tdr_process_api.get(i,"")
                L.append(belong_value)
                return render(request, "processApi.html",
                              {"belong_key":belong,"belong": belong_value,
                                "system": system,"role":tdr_role,"apinav":L})
        #如果belong不存在，返回导航的总列表
        l = []
        for a in tdr_process_api:
            l.append(tdr_process_api.get(a))
        return render(request, "processApi.html",
                      {"system": system,"role":tdr_role,"apinav":l})


def quicktest_views(request):
    '''
    内嵌ifame-快速测试页面
    '''
    return render(request, 'quickTest.html')


def apiDetail_views(request):
    '''
    详情页面
    '''
    singleid = request.GET.get("singleid","")
    processid = request.GET.get("processid", "")
    if singleid:
        id = SingleApi.objects.get(caseid=singleid)
    elif processid:
        id = ProcessApi.objects.get(caseid=processid)
    identity = id.identity
    url = "/".join(id.url.split("/")[-2:])
    dic = {
        "identity": identity,
        "belong": id.belong,
        "casename": id.casename,
        "url": url,
        "method": id.method,
        "params": id.params,
        "body" : id.body,
        "result" : id.result,
        "head" : id.head,
        "duration":id.duration
    }
    return render(request, "apiDetail.html", {"dic":dic})


def link_views(request):
    '''
    内嵌ifame-友情链接
    '''
    return render(request, 'link.html')


def testurl_views(request):
    '''
    内嵌ifame-测试网址
    '''
    return render(request, 'testUrl.html')


def systemlog_views(request):
    '''
    :内容ifame-系统日志
    '''
    return render(request, 'systemlog.html')


def menu_management_views(request):
    '''
    :内容ifame-菜单管理
    '''
    return render(request, 'menu.html')

def echart_report_views(request):
    '''
    :内容ifame-菜单管理
    '''
    return render(request, 'pyechartReport.html')


def test(request):
    all = ProcessApi.objects.filter()
    for i in all:
        url = i.url.split("/")
        a = 0
        w = ""
        e = ""
        for ii in url:
            if a >= 3:
                e = "/"+ii
            w += e
            a += 1
        ProcessApi.objects.filter(caseid=i.caseid).update(url=w)
    return HttpResponse("完成咯")


