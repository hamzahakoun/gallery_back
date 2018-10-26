from django.conf.urls import url
from .views import UserModelViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('',UserModelViewSet)
urlpatterns = router.urls
