from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.story_home, name='storyhome'),
    path('story/<int:id>', views.single_story, name='single-story'),
    path('story/api/currentviewers/<int:id>', views.CurrentStoryViewersView.as_view()),
    path('story/api/totalviewers/<int:id>', views.TotalStoryViewersView.as_view()),
]