
from django.conf.urls import (include, url)
from django.contrib import admin
from django.views.decorators.cache import cache_page

from days.views import IndexView

CACHE_DURATION = 60  # In seconds, I think

urlpatterns = [
    url(r'^$', cache_page(CACHE_DURATION)(IndexView.as_view())),
    url(r'^stabstabstab/', admin.site.urls),
]
