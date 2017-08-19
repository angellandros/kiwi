from datetime import datetime as dt
from datetime import timedelta

from django.db.models import OuterRef, Subquery, Count, Sum, IntegerField
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from reports.models import Device, Datum


def index(request):
    return HttpResponse('Hi!')


def view1(request, year, month, day):
    date = dt(int(year), int(month), int(day))
    date_last_week = date - timedelta(days=7)
    top_ten = Device.objects.annotate(count=Subquery(
            Datum.objects
            .filter(time__date=date, device=OuterRef('pk'))
            .order_by()
            .values('device')
            .annotate(c=Count('*'))
            .values('c'),
    output_field=IntegerField())).order_by('-count')[:10]
    output = {}
    for i in range(len(top_ten)):
        device = top_ten[i]
        count = Datum.objects.filter(time__date=date).filter(device=device).count()
        count_last_week = Datum.objects.filter(time__date=date_last_week).filter(device=device).count()
        device_stats = {
            'id': device.device_id,
            'count': device.count,
            'count_last_week': count_last_week,
            'change': None if count_last_week == 0 else round(float(count) * 100.0 / count_last_week - 100.0, 2)
        }
        output[i] = device_stats
    return output


def view1_json(request, year, month, day):
    return JsonResponse(view1(request, year, month, day))


def view1_html(request, year, month, day):
    devices = view1(request, year, month, day)
    context = {
        'devices': devices,
    }
    return render(request, 'reports/view1.html', context)


def view2_html(request, type, status):
    dated = (
        Datum.objects
        .filter(
            type=1 if type == 'sensor' else 2,
            status=1 if status == 'offline' else 2
        )
        .annotate(date=TruncDate('time'))
        .values('date')
        .annotate(count=Count('*'))
    )
    last_day = dated.latest('date')['date']
    queryset = dated.filter(date__gte=last_day - timedelta(days=30))
    numbers = {}
    for i in range(30):
        result = queryset.filter(date=last_day - timedelta(days=i))
        if result.count() != 0:
            numbers[i] = result[0]
    context = {
        'numbers': numbers,
        'type': type,
        'status': status,
    }
    return render(request, 'reports/view2.html', context)


def index(request):
    first = Datum.objects.order_by('time')[0].time.date().isoformat()
    latest = Datum.objects.latest('time').time.date().isoformat()
    context = {
        'first': first,
        'latest': latest,
    }
    return render(request, 'reports/index.html', context)
