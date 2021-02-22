from django.db import models

# Create your models here.


class AttachmentModel(models.Model):
    """
    附件表
    """
    url = models.CharField(max_length=1024, verbose_name='相对路径')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kh_attachments'
