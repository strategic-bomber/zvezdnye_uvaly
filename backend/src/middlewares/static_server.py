# redirect_middleware.py
import os

from django.conf import settings
from django.http import HttpResponseRedirect, FileResponse


class RedirectJSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path starts with 'js/'
        if request.path.startswith('/js/') or request.path.startswith('/img/') or request.path.startswith("/css/") \
                or request.path.startswith('/favicon.ico'):

            # Redirect to a different route
            rp = request.path.lstrip('/') # FIXME апач блокировал сервер, в проде так не надо делать!!!
            file = open(f"../frontend/dist/{rp}", "rb")

            return FileResponse(file)

        response = self.get_response(request)
        return response