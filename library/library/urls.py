from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .swagger import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.books.urls")),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
