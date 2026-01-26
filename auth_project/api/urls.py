from rest_framework.routers import DefaultRouter

from .views import BookAuthorViewSet, BookViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register(r"books-author", BookAuthorViewSet, basename="bookauthor")


urlpatterns = router.urls
