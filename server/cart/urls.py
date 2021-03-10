from rest_framework import routers

from cart import views

# ModelViewSet的请求路由注册
router = routers.DefaultRouter()
router.register(r'cart', views.CartViewSet, basename='cart')

urlpatterns = []
urlpatterns += router.urls
