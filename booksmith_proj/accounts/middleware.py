from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessRestrictionMiddleware:
    """
    Middleware to restrict access to the admin page for non-superusers.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the path starts with 'admin/' and the user is not a superuser, restrict access.
        if request.path.startswith(reverse('admin:index')) and not (request.user.is_authenticated and request.user.is_superuser):
            return redirect('/')  # Redirect to the homepage or any other page.
        return self.get_response(request)
