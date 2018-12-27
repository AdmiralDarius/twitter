from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import TwitterUser, Twit
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


@login_required
def save_twits(request):
    twit = Twit.objects.create(owner=TwitterUser.objects.get(user=request.user), title=request.POST['twit_title'],
                               body=request.POST['twit_body'], date=timezone.now())
    twit.save()
    return redirect("/api")


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


@login_required
def all_twits(request):
    twits = reversed(list(Twit.objects.order_by('date')))
    context = {'twits': twits}
    return render(request, 'api/all_twits.html', context)


@login_required
def save_pic(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        owner = TwitterUser.objects.get(user=request.user)
        owner.avatar = request.FILES["avatar_pic"]
        owner.save()
        # MemoryFileUploadHandler(request.FILES["avatar_pic"])

    return redirect("/api")


def darius_login(request):
    user = authenticate(request, username=request.POST["luser_name"], password=request.POST["luser_password"])
    if user is not None:
        login(request, user)
        return redirect("/api")
    else:
        return redirect("/api/login_page")


@login_required
def index(request):
    twits = reversed(list(Twit.objects.filter(owner=TwitterUser.objects.get(user=request.user)).order_by('date')))
    context = {'twits': twits, "user": request.user, "TwitterUser": TwitterUser.objects.get(user=request.user)}
    return render(request, 'api/index.html', context)


@login_required
def darius_logout(request):
    logout(request)
    return redirect("/api/login_page")


def login_page(request):
    context = {}
    return render(request, 'api/login_page.html', context)


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
