from apps.accounts.views import DecoratedTokenObtainPairView, UserViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

app_name = "accounts"

urlpatterns = (
    path("token/", DecoratedTokenObtainPairView.as_view(), name="token_create"),
    path("", include(router.urls)),
)
