import base64
import datetime
import json
import os
import uuid

from PIL import ImageFile
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def uploadFile(request):
    # SET THE METHOD OF REQUEST(post)
    if request.method == "POST":
        # open id of the user
        open_id = request.POST.get('open_id')
        print("this is open id")
        print(open_id)
        # attachments (e.g. id front picture or back picture/avatar)
        image = request.FILES.get('image')
        print("this is image")
        print(image)
        if not image or len(image) < 1:
            raise ValueError('image is required!')

        # save the image in the "/media" directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        serial = get_urlsafe_uuid_base64()
        filename = '%s_%s' % (timestamp, serial)
        filepath = save_image(image, open_id, filename)
        print(filepath)
        res = {
            'url': request.build_absolute_uri(filepath)}
        print(json.dumps(res))
    return JsonResponse(res)


def get_urlsafe_uuid_base64():
    """
    随机UUID转Base64编码
    :return: 22位字符串
    """
    return str(base64.urlsafe_b64encode((uuid.uuid4()).bytes), encoding='ascii').rstrip('=\n')


def save_image(file_obj, open_id, filename):
    if not file_obj.content_type.startswith('image'):
        return None
    image_type = file_obj.content_type.split('/')[-1]
    if image_type not in ['png', 'jpeg', 'bmp', 'x-png', 'pjpeg']:
        return None
    filename = '%s.png' % filename

    root = '/home/django/server/media'
    print(root)
    print(open_id)

    # 判断在media下是否含有该用户的在media下创建文件夹
    # destination = os.path.join(root, open_id)
    destination = root + '/' + open_id

    print(destination)

    if not os.path.exists(destination):
        print("directory does not exist, create")
        os.mkdir(destination)
        print("directory created")
    else:
        print("directory exists")

    # filepath = os.path.join(destination, filename)
    filepath = destination + '/' + filename
    parser = ImageFile.Parser()
    for chunk in file_obj.chunks():
        parser.feed(chunk)
    image = parser.close()
    image.save(filepath)

    res = os.path.join(settings.UPLOAD_URL, open_id, filename)
    print(res)
    return res
