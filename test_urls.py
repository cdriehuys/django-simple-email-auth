from django.urls import include, path

urlpatterns = [path("rest/", include("email_auth.interfaces.rest.urls"))]
