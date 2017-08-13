from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hi!')


def view1(request, year, month, day):
    return HttpResponse('View 1: %s-%s-%s' % (year, month, day))


def view2(request, device_id):
    return HttpResponse('View 2: %s' % device_id)

