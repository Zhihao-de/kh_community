from rest_framework import routers
from users import backend_views

# 后端视图
router = routers.DefaultRouter()
router.register(r'internal/users', backend_views.UsersViewSet)
router.register(r'internal/users/(?P<user_id>[^/.]+)/applications',
                backend_views.UserApplicationsViewSet, basename='user_applications')
router.register(r'internal/users/(?P<user_id>[^/.]+)/locations',
                backend_views.UserLocationViewSet, basename='user_locations')
router.register(r'internal/users/(?P<user_id>[^/.]+)/docs',
                backend_views.UserDocsViewSet, basename='user_docs')

urlpatterns = []
urlpatterns += router.urls
