
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^/', include('days.urls', namespace='days')),
    url(r'^admin/', admin.site.urls),
]
