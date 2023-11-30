from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'learning_hub'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    path('new_lesson/', views.new_lesson, name='new_lesson'), 
    path('filtered_lesson/', views.filtered_lesson, name='filtered_lesson'),
    path('filtered_lesson/lesson_delete/<int:id>', views.lesson_delete, name="lesson_delete"),
    path('filtered_lesson/lesson_detail/<int:pk>', views.lesson_detail , name='lesson-detail'), 
    path('search/', views.search, name="search"),
    path('result/', views.search, name="result"),    
    path('search/lesson_detail/<int:pk>', views.lesson_detail , name='lesson-detail'),
    #path('lessons/<int:pk>', views.lessons , name='lessons'),
    path('tokenizer/<int:id>/', views.tokenizer, name='tokenizer'),
    path('similarity/', views.similarity, name='similarity'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += static('/filtered_lesson/learning_hub/media/', document_root=settings.STATIC_ROOT)
#urlpatterns += static('/search/lms_app/static/', document_root=settings.STATIC_ROOT)
