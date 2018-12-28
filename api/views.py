from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import TwitterUser, Twit, SavedRequests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session

NN=10000
HH=2

def process_request(func):

    def wrapper(request):
        darius_auth=True
        #print(list_of_login_needing_funcs,func.__name__,func.__name__ in list_of_login_needing_funcs)
        if func.__name__ in list_of_login_needing_funcs and not request.user.is_authenticated:
            darius_auth=False
        now=SavedRequests.objects.create(explorer=request.META['HTTP_USER_AGENT'],ip=request.META['REMOTE_ADDR'],auth=darius_auth)
        now.save()

        #first and second part
        res=list(reversed(list(SavedRequests.objects.order_by('time'))))
        unautho_reqs = 0
        for i in range(len(res)):

            if res[i].ip == request.META['REMOTE_ADDR']:
                unautho_reqs +=1

            j=i+1
            reqs_sent=0
            while(j<len(res) and res[j].time.second-res[i].time.second<HH):
                #print(res[j].time.second - res[i].time.second)
                if res[j].ip==request.META['REMOTE_ADDR']:
                    reqs_sent+=1
                j+=1
            if reqs_sent>=NN or unautho_reqs>NN:
                return HttpResponse(status=404)


        return func(request)
    return wrapper
@process_request
@login_required
def save_twits(request):
    twit = Twit.objects.create(owner=TwitterUser.objects.get(user=request.user), title=request.POST['twit_title'],
                               body=request.POST['twit_body'], date=timezone.now())
    twit.save()
    return redirect("/api")

@process_request
def user_register(request):
    user = User.objects.create_user(username=request.POST["user_name"],
                                    email=request.POST["user_mail"],
                                    password=request.POST["user_password"],
                                    )
    user.first_name = request.POST["visible_name"]
    user.save()
    t = TwitterUser.objects.create(user=user)
    t.save()
    return redirect("/api/login_page")

@process_request
@login_required
def all_twits(request):
    twits = reversed(list(Twit.objects.order_by('date')))
    context = {'twits': twits}
    return render(request, 'api/all_twits.html', context)

@process_request
@login_required
def save_pic(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        owner = TwitterUser.objects.get(user=request.user)
        owner.avatar = request.FILES["avatar_pic"]
        owner.save()
        # MemoryFileUploadHandler(request.FILES["avatar_pic"])

    return redirect("/api")

@process_request
def darius_login(request):
    user = authenticate(request, username=request.POST["luser_name"], password=request.POST["luser_password"])
    if user is not None:

        login(request, user)
        return redirect("/api")
    else:
        return redirect("/api/login_page")

@process_request
@login_required
def index(request):
    twits = reversed(list(Twit.objects.filter(owner=TwitterUser.objects.get(user=request.user)).order_by('date')))
    context = {'twits': twits, "user": request.user, "TwitterUser": TwitterUser.objects.get(user=request.user)}
    return render(request, 'api/index.html', context)

@process_request
@login_required
def darius_logout(request):
    logout(request)
    return redirect("/api/login_page")

@process_request
def login_page(request):
    context = {}
    return render(request, 'api/login_page.html', context)

@process_request
def login_fix(request, next_page):
    return redirect("/api/login_page")


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def token_twits(request):
    user = request.user
    twit_user = TwitterUser.objects.get(user=user)
    Twit.objects.create(owner=twit_user, title=request.POST['twit_title'],
                        body=request.POST['twit_body'], date=timezone.now())
    return HttpResponse('response saved')


@login_required()
def token_generate(request):
    Token.objects.get(user=request.user).delete()
    token = Token.objects.create(user=request.user).key
    data = dict()
    data['token'] = str(token)
    return JsonResponse(data)

global list_of_login_needing_funcs
list_of_login_needing_funcs=['darius_logout','index','darius_login','save_pic','all_twits','save_twits']