from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """The only page that matters."""
    template_name = "about.html"

    def get_extra_data(self):
        """Gets the most recent article date"""
        context = super().get_extra_data()
        # Do some stuff here
        return context
