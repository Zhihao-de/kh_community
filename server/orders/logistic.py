import urllib.request as req

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.utils import json


@csrf_exempt
def get_route(request):
    # 使用用友API
    host = "https://api.yonyoucloud.com/apis/dst/delivery/queryDelivery?"
    apicode = "2e1192ad67ad4c468a7600d9d23e677d"
    number = request.GET['number']
    type_para = request.GET['type']
    path = "number=" + number + "&type=" + type_para
    url = host + path

    print('----------------------------------')
    print(url)

    header = {
        "authoration": "apicode",
        "apicode": apicode}
    my_request = req.Request(url, headers=header)
    response = req.urlopen(my_request)
    content = response.read().decode('utf-8')
    res_dict = json.loads(content)
    print(res_dict)

    if content:
        return JsonResponse(res_dict, safe=False)
    else:
        return JsonResponse({"status": "error"})
