from django.conf.urls import url
from rest_framework import routers

from products import views

router = routers.DefaultRouter()
# 前端视图
router.register(r'products/categories', views.ProductCategoryReadonlyViewSet)
router.register(r'products', views.ProductsReadonlyViewSet)
router.register(r'products/(?P<product_id>[^/.]+)/units', views.ProductUnitViewSet)
# 后端视图
router.register(r'internal/products/categories', views.ProductCategoryViewSet)
router.register(r'internal/products', views.ProductsViewSet, basename='product')
router.register(r'internal/products/(?P<product_id>[^/.]+)/units', views.ProductUnitViewSet, basename='unit')

urlpatterns = [
    url(r'internal/products/categories/tree',
        views.ProductCategoryViewSet.as_view({'get': 'list_tree'}))
]
urlpatterns += router.urls
