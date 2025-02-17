from apps.accounts.serializers import TokenObtainPairResponseSerializer, UserSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        security=[],
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(security=[])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
            return [permission() for permission in permission_classes]
        return super().get_permissions()
