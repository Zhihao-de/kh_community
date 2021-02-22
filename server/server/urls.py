"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
# from django.contrib.staticfiles.views import serve
from django.views.static import serve
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from attachments import urls as attachments_urls
from intentions import urls as intentions_urls
from orders import urls as orders_urls
from products import urls as products_urls
from server import settings
from users import urls as users_urls

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        re_path(r'^cms/', include(wagtailadmin_urls)),
        re_path(r'^docs/', include(wagtaildocs_urls)),
        re_path(r'^pages/', include(wagtail_urls)),
        path('', TemplateView.as_view(template_name='index.html')),
        url(r'^v1/', include(attachments_urls)),
        url(r'^v1/', include(products_urls)),
        url(r'^v1/', include(users_urls)),
        url(r'^v1/', include(orders_urls)),
        url(r'^v1/', include(intentions_urls)),
        url(r'media/files/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT})

    ] \
    # + static('/media/files/', document_root=settings.MEDIA_ROOT)
