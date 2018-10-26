from rest_framework.routers import SimpleRouter
from .views import CommentModelViewSet

router = SimpleRouter()
router.register('',CommentModelViewSet,base_name = 'comments')
urlpatterns = router.urls
