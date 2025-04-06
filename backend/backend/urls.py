from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import JsonResponse

def ping(request):
    return JsonResponse({"message": "pong"})



urlpatterns = [
    #admin urls
    path('svt-admin/', admin.site.urls),
    #for auth
    path('api/', include('authentication.urls')),
    #for posts in blog
    path('api/', include('posts.urls')),
    #project urls
    path('api/', include('project.urls')),
    #love urks
    path('api/', include('love.urls')),
    #for github action
    path("ping/", ping),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
