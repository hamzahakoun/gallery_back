from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/images',include('images.api.urls'),name = 'images-api'),
    url(r'^api/events',include('events.api.urls'),name = 'events-api'),
    url(r'^api/comments',include('comments.api.urls'),name = 'comments-api'),
    url(r'^api/users',include('users.api.urls'),name = 'users-api'),
    url(r'^api/api-token-auth/', obtain_jwt_token),
    url(r'^api/verify-token/', verify_jwt_token),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
