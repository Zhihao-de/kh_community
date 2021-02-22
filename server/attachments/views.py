import base64
import datetime
import os
import uuid
from urllib.parse import urlparse

from PIL import ImageFile
from rest_framework import viewsets

from attachments.serializers import *
from server import settings


class AttachmentsViewSet(viewsets.ModelViewSet):
    """
    附件视图集
    """
    queryset = AttachmentModel.objects.all()
    serializer_class = AttachmentsSerializer

    def create(self, request, *args, **kwargs):
        """
        上传附件
        :param request: 请求
        :return:
        """
        file = request.FILES.getlist('file', None)
        if not file or len(file) < 1:
            raise ValueError('file is required')
        file_obj = file[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        serial = self._get_urlsafe_uuid_base64()
        filename = '%s_%s' % (timestamp, serial)
        if file_obj.content_type.startswith('image'):
            filepath = AttachmentsViewSet._save_image(file_obj, filename)
        elif file_obj.content_type.startswith('application'):
            filepath = AttachmentsViewSet._save_doc(file_obj, filename)
        else:
            raise ValueError('file is not supported')
        request.data['url'] = request.build_absolute_uri(filepath)
        return super().create(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            raise ValueError('pk is required')
        url = request.data.get('url', None)
        if not url:
            raise ValueError('url is required')
        filepath = settings.BASE_DIR + urlparse(url).path
        if os.path.exists(filepath) and not os.path.isdir(filepath):
            ext = os.path.splitext(filepath)[-1].lower()
            if ext in ['.png', '.pdf', '.doc', '.docx', '.wps']:
                os.remove(filepath)
        return super().destroy(request, args, kwargs)

    @staticmethod
    def _save_image(file_obj, filename):
        if not file_obj.content_type.startswith('image'):
            return None
        image_type = file_obj.content_type.split('/')[-1]
        if image_type not in ['png', 'jpeg', 'bmp', 'x-png', 'pjpeg']:
            return None
        filename = '%s.png' % filename
        filepath = os.path.join(settings.UPLOAD_ROOT, filename)
        parser = ImageFile.Parser()
        for chunk in file_obj.chunks():
            parser.feed(chunk)
        image = parser.close()
        image.save(filepath)
        print(filepath)
        return os.path.join(settings.UPLOAD_URL, filename)

    @staticmethod
    def _save_doc(file_obj, filename):
        """
        存储 Content-Type 为 application/pdf, application/msword, application/vnd.ms-works 类型的文件
        :param file_obj:
        :param filename:
        :return:
        """
        if not file_obj.content_type.startswith('application'):
            return None
        image_type = file_obj.content_type.split('/')[-1]
        if image_type not in ['pdf', 'msword', 'vnd.ms-works']:
            return None
        ext = os.path.splitext(file_obj.name)[-1]
        filepath = os.path.join(settings.UPLOAD_ROOT, filename + ext)
        with open(filepath, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        print(os.path.join(settings.UPLOAD_URL, filename))
        return os.path.join(settings.UPLOAD_URL, filename)

    @staticmethod
    def _get_urlsafe_uuid_base64():
        """
        随机UUID转Base64编码
        :return: 22位字符串
        """
        return str(base64.urlsafe_b64encode((uuid.uuid4()).bytes), encoding='ascii').rstrip('=\n')


class AttachmentsFrontViewSet(viewsets.ModelViewSet):
    """
    附件视图集
    """

    # queryset = AttachmentModel.objects.all()
    # serializer_class = AttachmentsSerializer

    def create(self, request, *args, **kwargs):
        """
        上传附件
        :param request: 请求
        需要文件和用户的Id来作为参数
        参数是用来存放文件夹的
        :return:
        """
        # 获取文件
        file = request.FILES.getlist('file', None)
        # 获取前端传来的open id
        open_id = request.POST.get('open_id')
        print("open_id:" + open_id)
        if not file or len(file) < 1:
            raise ValueError('file is required')
        file_obj = file[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        serial = self._get_urlsafe_uuid_base64()
        filename = '%s_%s' % (timestamp, serial)
        if file_obj.content_type.startswith('image'):
            filepath = AttachmentsFrontViewSet._save_image(file_obj, open_id, filename)
        else:
            raise ValueError('file is not supported')
        request.data['url'] = request.build_absolute_uri(filepath)
        return super().create(request, args, kwargs)

    @staticmethod
    def _save_image(file_obj, open_id, filename):
        if not file_obj.content_type.startswith('image'):
            return None
        image_type = file_obj.content_type.split('/')[-1]
        if image_type not in ['png', 'jpeg', 'bmp', 'x-png', 'pjpeg']:
            return None
        # 文件的名字
        filename = '%s.png' % filename
        # 判断在media下是否含有该用户的在media下创建文件夹
        destination = settings.UPLOAD_ROOT + '/' + open_id
        print(destination)
        if not os.path.exists(destination):
            print("directory does not exist, create")
            os.mkdir(destination)
        else:
            print("directory exists")

        # filepath = os.path.join(settings.UPLOAD_ROOT, filename)
        filepath = os.path.join(destination, filename)
        parser = ImageFile.Parser()
        for chunk in file_obj.chunks():
            parser.feed(chunk)
        image = parser.close()
        image.save(filepath)
        print(filepath)
        return os.path.join(settings.UPLOAD_URL, filename)

    @staticmethod
    def _get_urlsafe_uuid_base64():
        """
        随机UUID转Base64编码
        :return: 22位字符串
        """
        return str(base64.urlsafe_b64encode((uuid.uuid4()).bytes), encoding='ascii').rstrip('=\n')
