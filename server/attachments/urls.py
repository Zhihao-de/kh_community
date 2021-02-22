from django.conf.urls import url
from rest_framework import routers

from attachments import views

router = routers.DefaultRouter()
router.register(r'internal/attachments', views.AttachmentsViewSet, basename='attachments')

urlpatterns = []
urlpatterns += router.urls
