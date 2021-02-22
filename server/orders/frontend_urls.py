from django.urls import re_path
from rest_framework import routers

from orders import frontend_views, wxpay, logistic

router = routers.DefaultRouter()

router.register(r'orders', frontend_views.OrdersViewSet, basename="order")

router.register(r'orders/(?P<order_id>[^/.]+)/details', frontend_views.OrderDetailsViewSet, basename='order_details')

router.register(r'orders/(?P<order_id>[^/.]+)/transactions', frontend_views.OrderTransactionsViewSet,
                basename='order_transactions')

router.register(r'orders/(?P<order_id>[^/.]+)/routes', frontend_views.OrderRoutesViewSet, basename='order_routes')

# router.register(r'orders/(?P<order_id>[^/.]+)/pay', wxpay.payOrder, basename='wxpay')

urlpatterns = [
    # 微信支付
    re_path(r'orders/wxpay/', wxpay.payOrder, name="wxpay"),
    # 查看物流
    re_path(r'orders/logistic/$', logistic.get_route, name='route'),
    # 微信支付回调
    re_path(r'orders/wxpayback/', wxpay.wxpayback, name='wxpayback')
]
urlpatterns += router.urls
