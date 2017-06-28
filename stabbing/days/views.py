from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from django.conf import settings

from days import models


class IndexView(TemplateView, ContextMixin):
    """The only page that matters."""
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        """Gets the most recent article date"""
        context = super().get_context_data(**kwargs)

        model_obj = self.request.model_object

        # Add some data to our context object
        context['site'] = self.request.site

        # Is there a model object associated with the request?
        if model_obj:
            try:
                context['event'] = model_obj.on_site.latest('date_event')

            # No event was found, so provide some strings to display.
            except model_obj.DoesNotExist:
                print(model_obj)

                if issubclass(model_obj, models.LastStabbing):
                    context['event'] = {'noun': 'Stabbing'}
                elif issubclass(model_obj, models.LastShooting):
                    context['event'] = {'noun': 'Shooting'}
                else:
                    context['event'] = {'noun': 'Event'}

        # I can't tell what kind of event it was, so say 'None'.
        else:
            context['event'] = {'noun': 'Event'}

        return context
