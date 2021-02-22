from rest_framework import serializers

from attachments.models import AttachmentModel


class AttachmentsSerializer(serializers.ModelSerializer):
    """
    附件表序列化器
    """

    class Meta:
        model = AttachmentModel
        fields = '__all__'
