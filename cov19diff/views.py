from django.shortcuts import render
from django.http import HttpResponse
from cov19diff.restype import ResultType
from cov19diff.restype import DaylyStatus
from cov19diff.jhudata import readDaily, dayCSVFormat

from cov19diff.models import DailyCsv
from rest_framework import viewsets
from rest_framework import permissions
from cov19diff.serializers import DailyCsvSerializer

from cov19diff.forms import DailyStatusForm

import glob
import os

from datetime import date
from datetime import timedelta

# Create your views here.

def filelist():
    files = glob.glob("../snap/*.txt")
    files = list(map(lambda x: os.path.basename(x.replace('.txt','')), files))
    files.sort(reverse=True)
    return files

def index(request):
    files = filelist()
    return render(request, 'cov19diff/index.html',{'files': files})

def dodiff(request):
    tgt = []
    for file in filelist():
        if file in request.POST:
            tgt.append(file)
    return difflist(request,tgt[1],tgt[0])

def getItems(line):
    flds = line.rstrip().split('\t')
    num = flds[0].replace(',','')
    if num.isnumeric():
        return [flds[1],int(num)]
    else:
        return None

def difflist(request, old, new):
    oldfilen = '../snap/'+old+'.txt'
    newfilen = '../snap/'+new+'.txt'
    oldstat = open(oldfilen)
    newstat = open(newfilen)

    tbl = dict()
    for line in oldstat:
        items = getItems(line)
        if items:
            tbl[items[0]] = items[1]
        else:
            if 'Updated' in line:
                oldtime = line

    results = []
    for line in newstat:
        items = getItems(line)
        if items:
            if items[0] in tbl:
                results.append(ResultType(items[0],tbl[items[0]],items[1]))
        else:
            if 'Updated' in line:
                newtime = line

    return render(request, 'cov19diff/list.html',
                {'results': results, 'oldtime': oldtime, 'newtime': newtime})

def daylyStat(request,day,ord,form):
    datas = readDaily(day)
    daylys = []
    for data in datas:
        daylys.append(DaylyStatus(data,
                                  datas[data]['Confirmed'],
                                  datas[data]['Deaths'],
                                  datas[data]['Recovered']))
    if ord == 'C':
        daylys.sort(key=lambda d: d.confirmed, reverse=True)
    elif ord == 'A':
        daylys.sort(key=lambda d: d.active(), reverse=True)
    elif ord == 'D':
        daylys.sort(key=lambda d: d.deaths, reverse=True)
    elif ord == 'R':
        daylys.sort(key=lambda d: d.recover, reverse=True)
    elif ord == 'DR':
        daylys.sort(key=lambda d: float(d.deathRatio()), reverse=True)
    elif ord == 'RR':
        daylys.sort(key=lambda d: float(d.recoverRatio()), reverse=True)
    elif ord == 'AR':
        daylys.sort(key=lambda d: float(d.activeRatio()), reverse=True)
    elif ord == 'CN':
        daylys.sort(key=lambda d: d.cname)

    return render(request, 'cov19diff/dayly.html',
                {'daylys': daylys, 'day': day, 'form': form})

def doDayly(request):
    if request.method == 'GET':
        form = DailyStatusForm()
    else:
        form = DailyStatusForm(request.POST)
        if form.is_valid():
            day = dayCSVFormat(form.cleaned_data['day'])
            ord = form.cleaned_data['order']
            return daylyStat(request, day, ord, form)
    return render(request, 'cov19diff/dayly.html',
                {'daylys': [], 'day': None, 'form': form})

def doTS(request,cname):
    today = date.today()
    targetday = today - timedelta(days=30)
    pv = None
    days = dict()
    while targetday < today:
        tday = targetday.strftime('%m-%d-%Y')
        datas = readDaily(tday)
        if len(datas) > 0 and cname in datas:
            if pv:
                nv = DaylyStatus(cname,
                                      datas[cname]['Confirmed'],
                                      datas[cname]['Deaths'],
                                      datas[cname]['Recovered'])
                days[tday] = nv.setdiff(pv)
                pv = nv
            else:
                pv = DaylyStatus(cname,
                                      datas[cname]['Confirmed'],
                                      datas[cname]['Deaths'],
                                      datas[cname]['Recovered'])
        targetday = targetday + timedelta(days=1)
    #days = reversed(days)
    return render(request, 'cov19diff/ts.html',
                {'cname': cname, 'days': days})

class DailyCsvViewSet(viewsets.ModelViewSet):
    queryset = DailyCsv.objects.all()
    serializer_class = DailyCsvSerializer
    permission_classes = [permissions.IsAuthenticated]
