from rest_framework import routers

from intentions import frontend_views

# ModelViewSet的请求路由注册
router = routers.DefaultRouter()
router.register(r'intentions', frontend_views.IntentionsViewSet, basename='intentions')
router.register(r'intention_assignment', frontend_views.IntentionAssignmentsViewSet, basename='intention_assignment')
router.register(r'intentions/(?P<intention_id>[^/.]+)/details', frontend_views.IntentionDetailsViewSet,
                basename='intention_details')
router.register(r'intention_history', frontend_views.IntentionHistoryViewSet, basename='intention_history')

urlpatterns = []
urlpatterns += router.urls
