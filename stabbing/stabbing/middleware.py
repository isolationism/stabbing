
from pprint import pprint

from days import models


class ModelObjectMiddleware(object):
    """Determines an appropriate (if any) model object based on access URL"""

    def __init__(self, get_response):
        """Initialize the middleware (runs once)"""
        self.get_response = get_response

    def __call__(self, request):
        """Called on each request"""
        # Try to determine an appropriate model object based on access URL
        hostname = request.META['HTTP_HOST']
        if hostname.count('stabbing'):
            request.model_object = models.LastStabbing
        elif hostname.count('shooting'):
            request.model_object = models.LastShooting
        else:
            request.model_object = None

        # Get a response from our view.
        response = self.get_response(request)

        # No post-view processing required.
        return response
