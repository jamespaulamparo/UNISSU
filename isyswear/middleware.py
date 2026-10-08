from django.shortcuts import redirect
from django.urls import reverse

# Legacy middleware deactivated: View-level decorators (@login_required, @admin_required)
# now handle all permission gating cleanly and robustly.

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
