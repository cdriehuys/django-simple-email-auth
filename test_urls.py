from django.contrib import admin
from django.urls import include, path

try:
    import rest_framework  # noqa

    REST_FRAMEWORK_AVAILABLE = True
except ImportError:
    REST_FRAMEWORK_AVAILABLE = False

# Include the admin URL so 'manage.py check' actually does something.
urlpatterns = [path("admin/", admin.site.urls)]

# If DRF is installed, include the REST endpoints.
if REST_FRAMEWORK_AVAILABLE:
    urlpatterns.append(
        path("rest/", include("email_auth.interfaces.rest.urls"))
    )
