from django.conf.urls import url
from rest_framework import routers

from intentions import backend_views

# ModelViewSet的请求路由注册
router = routers.DefaultRouter()
router.register(r'internal/intentions', backend_views.IntentionsViewSet, basename='intentions')
router.register(r'internal/intention_history', backend_views.IntentionHistoryViewSet, basename='intention_history')
router.register(r'internal/intentions/(?P<intention_id>[^/.]+)/details',
                backend_views.IntentionDetailsViewSet, basename='intention_details')
router.register(r'internal/intentions/(?P<intention_id>[^/.]+)/assignments',
                backend_views.IntentionAssignmentsViewSet, basename='intention_assignments')
router.register(r'internal/intentions/assignments',
                backend_views.IntentionAssignmentsDropViewSet, basename='assignment_drop')
router.register(r'internal/intentions/(?P<intention_id>[^/.]+)/history',
                backend_views.IntentionHistoryViewSet, basename='intention_history')

# APIVIEW请求路径的注册
'''
urlpatterns = [
    url(r'internal/intentions/(?P<intention_id>[^/.]+)/assignments/create',
        backend_views.IntentionAssignmentsViewSet.as_view({'post': 'batch_create'})),
    url(r'internal/intentions/(?P<intention_id>[^/.]+)/assignments/drop',
        backend_views.IntentionAssignmentsViewSet.as_view({'patch': 'batch_update'}))
]
'''

#urlpatterns += router.urls
urlpatterns = []
urlpatterns += router.urls