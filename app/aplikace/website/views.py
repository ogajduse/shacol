from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collision
#import sqlite3
#from graphos.sources.model import ModelDataSource
#from graphos.renderers import flot
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

# Create your views here.
def colls(request):
    collisions = Collision.objects.all()
    return render(request, 'website/collision.html', {'collisions': collisions})

def graphs(request):
    data =  [
        ['Total time', 'Bits'],
        [2004, 1000],
        [2005, 1170],
        [2006, 660],
        [2007, 1030]
    ]
    # DataSource object
    data_source = SimpleDataSource(data=data)
    # Chart object
    chart = LineChart(data_source)
    context = {'chart': chart}
    return render(request, 'website/graphs.html', context)
    """collisions = Collision.objects.all()
    data = ModelDataSource(collisions, fields=['bits', 'total_time'])
    chart = flot.LineChart(data)
    return render(request, 'website/graphs.html', {'chart: chart})"""

def delete(request):
    colls = Collision.objects.all()
    colls.delete()
    return redirect('/')

def filtering(request):
    if 'method' in request.POST:
        colls = Collision.objects.all()
        query = dict(
            method=""
        )

        if request.POST['method'] == "str":
            colls = colls.filter(test_method__contains='String')
            query['method']= request.POST['method']
            #query['method']= request.POST['method']

        elif request.POST['method'] == "int":
            colls = colls.filter(test_method__contains='Int')
            query['method']= request.POST['method']

        elif request.POST['method'] == "db":
            colls = colls.filter(test_method__contains="db")
            query['method']= request.POST['method']

        return render(request, 'website/collision.html', {'colls':colls, 'query':query})

    else:
        return redirect('/')


#    return render(request, 'website/base.html')
