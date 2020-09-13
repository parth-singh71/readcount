from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone, timesince
import datetime
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import StoryViewSerializer
from .models import Story, StoryView


# Create your views here.


@login_required
def story_home(request):
    if request.method == 'GET':
        stories = Story.objects.all()
        context = {
            'stories': stories,
            'title': "Home"
        }
    return render(request, 'stories/home.html', context=context)


def check_if_storyview_exists(user, story):
    try:
        storyView = StoryView.objects.get(user=user, story=story)
    except StoryView.DoesNotExist:
        storyView = None
    if storyView is not None:
        return True
    else:
        return False


def get_all_storyviewers(story):
    return StoryView.objects.filter(story=story)


def get_current_story_viewers(story):
    time = timezone.now() - datetime.timedelta(seconds=30)
    return StoryView.objects.filter(story=story, last_seen__gte=time)


def update_last_seen(user, story):
    storyview = StoryView.objects.get(user=user, story=story)
    storyview.last_seen = timezone.now()
    storyview.save()


@login_required
def single_story(request, id):
    if request.method == 'GET':
        story = Story.objects.get(id=id)
        if request.user.is_authenticated:
            user = request.user
            if not check_if_storyview_exists(user, story):
                storyview = StoryView(user=user, story=story)
                storyview.save()
        update_last_seen(request.user, story)
        current_story_viewers = get_current_story_viewers(story)
        all_viewers = get_all_storyviewers(story)
        title = f"Story - {story.title}"
        context = {
            'story': story,
            'title': title,
            'current_viewers': current_story_viewers,
            'all_viewers': all_viewers,
        }
    return render(request, 'stories/single_story.html', context=context)


class CurrentStoryViewersView(APIView):

    def get(self, request, id=None):
        if id:
            story = Story.objects.get(id=id)
            update_last_seen(request.user, story)
            current_story_viewers = get_current_story_viewers(story)
            serializer = StoryViewSerializer(
                current_story_viewers, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)


class TotalStoryViewersView(APIView):

    def get(self, request, id=None):
        if id:
            story = Story.objects.get(id=id)
            all_viewers = get_all_storyviewers(story)
            serializer = StoryViewSerializer(
                all_viewers, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
