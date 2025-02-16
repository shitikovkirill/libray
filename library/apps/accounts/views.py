from apps.accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
            return [permission() for permission in permission_classes]
        return super().get_permissions()
