from django.http import HttpResponse
from django.shortcuts import render

def save_twits(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def user_register(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def all_twits(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def save_pic(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def logout(request):
    return HttpResponse("Hello, world. You're at the polls index.")