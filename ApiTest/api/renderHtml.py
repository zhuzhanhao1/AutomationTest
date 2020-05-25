import json
from django.db.models import Q
from django.shortcuts import render, redirect
from ApiTest.models import SingleApi, ProcessApi, UserProfile, ChildMenu
from django.contrib import auth
import requests
from django.contrib.auth.models import User
import pypinyin
import random
from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from ApiTest.serializers import GetParamsSer


def login_views(request):
    '''
    访问登录首页
    '''
    return render(request, 'lgoindingding.html')


def dingding_login_views(request):
    '''
    钉钉扫码登录
    '''
    if request.method == "GET":
        code = request.GET.get('code', )
        appId = 'dingoa6if6q5jqpwb0sndx'
        appSecret = 'bpipZUwfOxppbNHfIJ8gmwmFClBfOmBnteUWPM4mmmXXNXxRTx_NznlxpC8M0F_1'

        token = requests.get(
            'https://oapi.dingtalk.com/sns/gettoken?appid={appId}&appsecret={appSecret}'.format(appId=appId,
                                                                                                appSecret=appSecret))
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
        unionid = user_info.get('unionid')
        openid = user_info.get('openid')
        user_obj = UserProfile.objects.filter(unionid=unionid).first()
        print(user_obj)
        if user_obj:
            print("当前登录用户已存在！")
        else:
            password = make_password("admin")
            user = User.objects.create(
                username=pypinyin.slug(user_info["nick"], separator="") + str(random.randint(0, 9999)),
                password=password, first_name=user_info["nick"])
            userprofile = UserProfile.objects.create(user=user, openId=openid, unionid=unionid)
            print(userprofile)
        user = UserProfile.objects.get(unionid=unionid)
        user = User.objects.get(id=user.user_id)
        request.session['username'] = user.username  # 登录成功后，用户登录信息存>放于session
        request.session.set_expiry(86400)  # 设置登录过期时间
        print(request.session)
        return redirect('/index/')
    else:
        return render(request, 'login.html')


def logout_views(request):
    # 这个相当于把这个requets里面的user给清除掉，清除掉session_id,注销掉用户
    auth.logout(request)
    # 删除Redis缓存的所有数据
    get_redis_connection("default").flushall()
    request.session.flush()
    # 将session的数据都删除,并且cookies也失效
    return redirect('/login/')


def index_views(request):
    '''
    首页html
    '''
    user_id = UserProfile.objects.filter().order_by("-user_id")[:1].first().user_id
    # 获取当前登录名
    name = User.objects.filter(id=user_id).first().first_name
    login_name = {
        "name": name
    }
    return render(request, 'index.html', login_name)


def home_views(request):
    '''
    首页内嵌ifame
    '''
    return render(request, 'search.html')


def singleapi_views(request):
    '''
    单一接口html
    crumbs:所属模块的键、英文名(用在了面包屑)
    belong:所属模块的值（中文名，用在了区分模块）
    system:所属系统
    '''
    belong = request.GET.get("belong", "")
    system = request.GET.get("system", "")
    #缓存Redis
    conn = get_redis_connection('default')
    dic = conn.get("single_params_dic")
    if dic:
        if belong:
            belong_value = json.loads(dic).get(belong, "")
            return render(request, "singleApi.html", {"crumbs": belong, "belong": belong_value, "system": system})
        else:
            return render(request, "singleApi.html", {"system": system})
    else:
        queryset = ChildMenu.objects.filter(Q(href__contains=system) & Q(area="single"))
        OrderedDict = GetParamsSer(queryset, many=True).data
        params_dic = {}
        for i in OrderedDict:
            params_dic[i["nav"]] = i["title"]
        print("访问MySQL拿取belong数据放入缓存")
        params_dic = json.dumps(params_dic)
        # 设置缓存时间一小时=3600
        conn.set("single_params_dic", params_dic)
        if belong:
            belong_value = dic.get(belong, "")
            return render(request, "singleApi.html", {"crumbs": belong, "belong": belong_value, "system": system})
        else:
            return render(request, "singleApi.html", {"system": system})




def processapi_views(request):
    '''
        流程接口html
        crumbs:所属模块的键、英文名(用在了面包屑)
        belong:所属模块的值（中文名，用在了区分模块）
        system:所属系统
    '''
    belong = request.GET.get("belong", "")
    system = request.GET.get("system", "")
    #缓存Redis
    conn = get_redis_connection('default')
    dic = conn.get("process_params_dic")
    if not dic:
        queryset = ChildMenu.objects.filter(Q(href__contains=system) & Q(area="process"))
        OrderedDict = GetParamsSer(queryset, many=True).data
        params_dic = {}
        for i in OrderedDict:
            params_dic[i["nav"]] = i["title"]
        print("访问MySQL拿取belong数据放入缓存")
        params_dic = json.dumps(params_dic)
        # 设置缓存时间一小时
        conn.set("process_params_dic", params_dic, 3600)
        if belong:
            belong_value = dic.get(belong, "")
            return render(request, "processApi.html", {"crumbs": belong, "belong": belong_value, "system": system})
        else:
            return render(request, "processApi.html", {"system": system})
    else:
        if belong:
            belong_value = json.loads(dic).get(belong, "")
            return render(request, "processApi.html", {"crumbs": belong, "belong": belong_value, "system": system})
        else:
            return render(request, "processApi.html", {"system": system})


def quicktest_views(request):
    '''
        内嵌ifame-快速测试页面
    '''
    return render(request, 'quickTest.html')


def apiDetail_views(request):
    '''
        接口详情页面
    '''
    singleid = request.GET.get("singleid", "")
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
        "body": id.body,
        "result": id.result,
        "head": id.head,
        "duration": id.duration
    }
    return render(request, "apiDetail.html", {"dic": dic})


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
        内容ifame-系统日志
    '''
    return render(request, 'systemlog.html')


def menu_management_views(request):
    '''
        内容ifame-菜单管理
    '''
    return render(request, 'menu.html')


def echart_report_views(request):
    '''
        内容ifame-报表
    '''
    return render(request, 'pyechartReport.html')

