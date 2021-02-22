from django.urls import path
from rest_framework import routers

from users import auth_views, frontend_views, file_uploader

# 前端视图
router = routers.DefaultRouter()
router.register(r'users', frontend_views.UsersViewSet)
router.register(r'users/(?P<user_id>[^/.]+)/applications', frontend_views.UserApplicationsViewSet,
                basename='user_applications')
router.register(r'users/(?P<user_id>[^/.]+)/locations', frontend_views.UserLocationViewSet, basename='user_locations')
router.register(r'locations', frontend_views.UserLocationViewSet, basename='user_locations')
router.register(r'users/(?P<user_id>[^/.]+)/docs', frontend_views.UserDocsViewSet, basename='user_docs')
router.register(r'users/(?P<user_id>[^/.]+)/addresses', frontend_views.UserAddressViewSet, basename='user_address')
router.register(r'users/(?P<user_id>[^/.]+)/accounts', frontend_views.UserAccountViewSet, basename='user_accounts')

urlpatterns = [
    path('wechat_login', auth_views.wechat_login, name='wechat_login'),
    path('upload', file_uploader.uploadFile, name="upload")
]
urlpatterns += router.urls
