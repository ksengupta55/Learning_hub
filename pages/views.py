from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.core.mail import send_mail, get_connection
from django.conf import settings

from pages.models import Page
from . models import Page
from . forms import ContactForm

# Create your views here.
#def index(request):
    #return HttpResponse("<h1> The LMS Homepage</h1>")

def index(request):
    #pg = get_object_or_404(Page, permalink=pagename)
    pg = Page.objects.get(permalink='/')
    #return HttpResponse("<h1> The LMS Homepage</h1>")
    context ={
        'title': pg.title,
        'content': pg.body_text,
        'last_updated': pg.update_date,
        'page_list': Page.objects.all(),
    }
    # assert False
    return render(request, "pages/page.html", context)

def about(request):
    #pg = get_object_or_404(Page, permalink=pagename)
    pg = Page.objects.get(permalink='/about')
    context ={
        'title': pg.title,
        'content': pg.body_text,
        'last_updated': pg.update_date,
        'page_list': Page.objects.all(),
    }
    # assert False
    return render(request, "pages/page.html", context)


def services(request):
    #pg = get_object_or_404(Page, permalink=pagename)
    pg = Page.objects.get(permalink='/services')
    context = {
        'title': pg.title,
        'content': pg.body_text,
        'last_updated': pg.update_date,
        'page_list': Page.objects.all(),
    }
    # assert False
    return render(request, "pages/page.html", context)

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print("Email host: ", settings.EMAIL_HOST)
            print("Email port: ", settings.EMAIL_PORT)
            print("Host user: ", settings.EMAIL_HOST_USER)
            print("Host password: ", settings.EMAIL_HOST_PASSWORD)
            print("Security: ", settings.EMAIL_USE_TLS)
            cd = form.cleaned_data
            #user = authenticate(username='admin',
                                 #password='r0h1n1')
            '''if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')'''
            
            '''con = get_connection(settings.EMAIL_BACKEND)
            print("Connection: ", con)'''
            
            with get_connection(
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS  
            ) as connection:
                send_mail(
                cd['subject'], 
                cd['message'], 
                cd.get('email', 'ksengupta55@gmail.com'),
                [settings.EMAIL_HOST_USER])
            return HttpResponseRedirect('/contact?submitted=True')

    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True
            
    return render(request, 'pages/contact.html', {'form': form, 'page_list': Page.objects.all(), 'submitted': submitted}) 



