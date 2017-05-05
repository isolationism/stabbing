from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from django.conf import settings

from . import models


class IndexView(TemplateView, ContextMixin):
    """The only page that matters."""
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Gets the most recent article date"""
        context = super().get_context_data(**kwargs)

        # Add some data to our context object
        context['site'] = self.request.site
        try:
            context['stabbing'] = models.LastStabbing.on_site\
                .latest('date_stabbed')
        except models.LastStabbing.DoesNotExist:
            context['stabbing'] = None

        return context
