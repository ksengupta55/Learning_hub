from django.shortcuts import render

from video.forms import VideoForm
from .models import Video

# Create your views here.
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
