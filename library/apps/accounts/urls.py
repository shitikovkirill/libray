from apps.accounts.views import UserViewSet
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

app_name = "accounts"

urlpatterns = (
    path("token/", TokenObtainPairView.as_view(), name="token_create"),
    path("", include(router.urls)),
)
