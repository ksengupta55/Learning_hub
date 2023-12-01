from pathlib import Path
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from lh_project import settings

from video.forms import VideoForm
from .models import Video
from learning_hub.models import Lesson

# Create your views here.
@login_required
def video_list(request):
    video = Video.objects.all()
    return render(request, "video_list.html", {"video": video})

def new_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
           
            form.save()
             
            
            #return HttpResponseRedirect("/new_lesson/?submitted=true")
            return render(request, 'new_video.html', {'form': form, 'submitted': 'sumbitted'})
    else:
        form = VideoForm()
    return render(request, 'new_video.html', {'form': form})

@login_required
def video_delete(request, id = None):
    instance = get_object_or_404(Video, id=id)
    
    videoDir = str(instance.video) # Question dir path (relative) from database

    videopath = str(settings.MEDIA_ROOT) + "/" + videoDir # Question dir full path 

    video_path = Path(videopath)
    print("Video path and name: ", video_path)
    video_path.unlink() # Delete Question file

    instance.delete() # Delete database records
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))