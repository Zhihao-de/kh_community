from intentions import frontend_urls
from intentions import backend_urls

urlpatterns = []
urlpatterns += frontend_urls.urlpatterns
urlpatterns += backend_urls.urlpatterns

