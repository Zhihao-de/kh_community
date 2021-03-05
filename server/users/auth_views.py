import json

import requests
from django.conf import settings
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users import response_code
from users.models import UserModel

'''
获取openid
'''


def get_openid_by_code(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'
    get_url = url.format(settings.WEIXIN_APPID, settings.WEIXIN_SECRET, code)
    r = requests.get(get_url)
    return r.json()


@csrf_exempt
def wechat_login(request):
    json_data = json.loads(request.body)
    code = json_data['code']
    userInfo = json_data['userInfo']
    try:
        nickname = userInfo['nickName']
        avatar = userInfo['avatarUrl']
        sex = userInfo['gender']

        print(userInfo)

        json_data_wx = get_openid_by_code(code)
        print("发出了请求微信openiD")
        if 'errcode' in json_data_wx:
            res = {
                'errno': response_code.AUTH_ERROR,
                'statusCode': 200,
                'errMsg': '出错了:' + json_data_wx['errmsg']
            }
            print("获取微信open id 的时候出错")
            return JsonResponse(res)
        weixin_openid = json_data_wx['openid']

        print("获取到微信的open id正准备用户的数据库操作")
        print(weixin_openid)
        print("在UserModel中进行查询")
        role = -1
        # 在usermodel中查找该微信openID
        try:
            customerObj = UserModel.objects.get(wx_open_id=weixin_openid)
            print(customerObj)

            user_details = model_to_dict(customerObj)
            flags = user_details["flags"]
            print(user_details)
            # 当flags=2时表示是开皇用户
            if flags == 2:
                res = {
                    'errno': response_code.IS_SUCCESS,
                    'statusCode': 200,
                    'errMsg': '登录成功',
                    'userInfo': userInfo,
                    "openId": weixin_openid,
                    "userDetail": user_details,
                    "role": 2
                }
            # flags==1时候表示是加盟用户
         
            else:
                res = {
                    'errno': response_code.IS_SUCCESS,
                    'statusCode': 200,
                    'errMsg': '登录成功',
                    'userInfo': userInfo,
                    "openId": weixin_openid,
                    "userDetail": user_details,
                    "role": flags
                }
            return JsonResponse(res)
        except:
            # 表示是普通用户 而且还未申请
            role = 4
            print("普通用户")
            # 将这个用户的信息加入用户中
            newUser = UserModel()

            # 表示还未申请
            newUser.flags = 4
            newUser.wx_open_id = weixin_openid
            newUser.wx_union_id = weixin_openid
            newUser.gender = sex
            newUser.address_id = 0
            newUser.wx_avatar_url = avatar
            newUser.wx_name = nickname
            newUser.save()
            res = {
                'errno': response_code.IS_SUCCESS,
                'statusCode': 200,
                'errMsg': '登录成功',
                "openId": weixin_openid,
                "userDetail": user_details,
                "role": flags
            }
            return JsonResponse(res)


    except:
        res = {
            'errno': response_code.AUTH_ERROR,
            'statusCode': 200,
            'errMsg': '登录出错了'
        }
        print("最后出错了")
        return JsonResponse(res)
