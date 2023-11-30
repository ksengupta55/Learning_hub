from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('video_list/', views.video_list, name='video_list'),
    path('new_video/', views.new_video, name='new_video'),

]
#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
