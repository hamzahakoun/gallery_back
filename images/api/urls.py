from django.conf.urls import url
from .views import ImageModelViewSet,TagModelViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('',ImageModelViewSet,base_name = 'image')

urlpatterns = [
    url('tags',TagModelViewSet.as_view({"get" : 'list'}))
]

urlpatterns += router.urls
