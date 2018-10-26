from rest_framework.routers import SimpleRouter
from .views import EventModelViewSet
from django.conf.urls import url

router = SimpleRouter()
router.register('',EventModelViewSet,base_name = 'events')
urlpatterns = router.urls
