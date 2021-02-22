from django.urls import re_path
from rest_framework import routers

from orders import backend_views, wxpay

# 后端视图
router = routers.DefaultRouter()
router.register(r'internal/orders', backend_views.OrdersViewSet)
# 订单交易
router.register(r'internal/orders/(?P<order_id>[^/.]+)/transactions',
                backend_views.OrderTransactionsViewSet, basename='order_transactions')
# 商品清单
router.register(r'internal/orders/(?P<order_id>[^/.]+)/details',
                backend_views.OrderDetailsViewSet, basename='order_details')
# 订单物流
router.register(r'internal/orders/(?P<order_id>[^/.]+)/routes',
                backend_views.OrderRoutesViewSet, basename='order_routes')
# 订单历史
router.register(r'internal/orders/(?P<order_id>[^/.]+)/history',
                backend_views.OrderHistoryViewSet, basename='order_history')

urlpatterns = [
    # 微信退款
    re_path(r'internal/orders/refund/', wxpay.wxpayrefund, name="refund"),

    # 微信退款回调
    re_path(r'internal/orders/refundback/', wxpay.refundback, name='refundback')
]

urlpatterns += router.urls
