from datetime import datetime as dt
from datetime import timedelta

from django.db.models import OuterRef, Subquery, Count
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from reports.models import Device, Datum


def index(request):
    return HttpResponse('Hi!')


def view1(request, year, month, day):
    date = dt.date(int(year), int(month), int(day))
    date_last_week = date - timedelta(days=7)
    top_ten = Device.objects.annotate(count=Count(Subquery(
            Datum.objects
            .filter(time__date=date)
            .filter(device=OuterRef('pk')).only('pk')
        ))).order_by('count')[:10]
    output = []
    for i in range(len(top_ten)):
        device = top_ten[i]
        count = Datum.objects.filter(time__date=date).filter(device=device).count()
        count_last_week = Datum.objects.filter(time__date=date_last_week).filter(device=device).count()
        device_stats = {
            'id': device.device_id,
            'count': count,
            'count_last_week': count_last_week,
            'change': None if count_last_week == 0 else float(count) / count_last_week - 1.0
        }
        output.append(device_stats)
    return JsonResponse(output)


def view2(request, device_id):
    return HttpResponse('View 2: %s' % device_id)
