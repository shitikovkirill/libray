from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version="v1",
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[],
)
