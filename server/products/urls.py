from django.conf.urls import url
from rest_framework import routers

from products import views

router = routers.DefaultRouter()
# 前端视图
router.register(r'products/categories', views.ProductCategoryReadonlyViewSet)
router.register(r'products', views.ProductsReadonlyViewSet)

# 后端视图
router.register(r'internal/products/categories', views.ProductCategoryViewSet)
router.register(r'internal/products', views.ProductsViewSet, basename='product')

urlpatterns = [
    url(r'internal/products/categories/tree',
        views.ProductCategoryViewSet.as_view({'get': 'list_tree'}))
]
urlpatterns += router.urls
