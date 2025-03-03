from rest_framework.routers import DefaultRouter

from .views import BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)

app_name = "books"

urlpatterns = router.urls
