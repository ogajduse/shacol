from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collision
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from django.db.models import Max, Min

# Create your views here.
def colls(request):
    collisions = Collision.objects.all()
    return render(request, 'website/collision.html', {'collisions': collisions})

def graphs(request):
    max_bits = (Collision.objects.all().aggregate(Max('bits'))['bits__max']) + 1
    min_bits = (Collision.objects.all().aggregate(Min('bits'))['bits__min'])
    data = [['Bits', 't-int', 't-string']]

    for b in range(min_bits, max_bits , 4):
        colls_int = Collision.objects.values_list("total_time").filter(test_method__contains="Int", bits=b)
        colls_str = Collision.objects.values_list("total_time").filter(test_method__contains="String", bits=b)
        tmp = [b, colls_int, colls_str]
        data.append(tmp)

    data_source = SimpleDataSource(data=data)
    chart = LineChart(data_source)
    context = {'chart': chart}
    return render(request, 'website/graphs.html', context)

def graphfilter(request):
    if 'graphmethod' in request.POST:
        data = [['Total time', 'Bits']]
        if request.POST['graphmethod'] == "str":
            colls = Collision.objects.values_list("total_time", "bits").filter(test_method__contains="String")
            for time, bits in colls:
                data.append([time, bits])

        elif request.POST['graphmethod'] == "int":
            colls = Collision.objects.values_list("total_time", "bits").filter(test_method__contains="Int")
            for time, bits in colls:
                data.append([time, bits])

        elif request.POST['graphmethod'] == "db":
            colls = Collision.objects.values_list("total_time", "bits").filter(test_method__contains="db")
            for time, bits in colls:
                data.append([time, bits])

        elif request.POST['graphmethod'] == "all":
            max_bits = (Collision.objects.all().aggregate(Max('bits'))['bits__max']) + 1
            min_bits = (Collision.objects.all().aggregate(Min('bits'))['bits__min'])
            data = [['Bits', 't-int', 't-string']]
            for b in range(min_bits, max_bits , 4):
                colls_int = Collision.objects.values_list("total_time").filter(test_method__contains="Int", bits=b)
                colls_str = Collision.objects.values_list("total_time").filter(test_method__contains="String", bits=b)
                tmp = [b, colls_int, colls_str]
                data.append(tmp)

    data_source = SimpleDataSource(data=data)
    chart = LineChart(data_source)
    context = {'chart': chart}
    return render(request, 'website/graphs.html', context)

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
