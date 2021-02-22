from orders import frontend_urls, backend_urls

urlpatterns = []
urlpatterns += frontend_urls.urlpatterns
urlpatterns += backend_urls.urlpatterns

