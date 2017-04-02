from django.shortcuts import render
from django.http import HttpResponse
from .models import Collision
import sqlite3
# Create your views here.
def colls(request):
    collisions = Collision.objects.all()
    return render(request, 'website/base.html', {'collisions': collisions})


def filtering(request):
    if request:
        colls = Collision.objects.all()
        query = dict(
            method = ""
        )

        if 'method' in request.POST:
            if request.POST['method'] == "str":
                colls = colls.filter(test_method='String method')
                query['method']= request.POST['method']
                #query['method']= request.POST['method']

            elif request.POST['method'] == "int":
                colls = colls.filter(test_method__contains='Int')
                #query['method']= request.POST['method']

            elif request.POST['method'] == "with DB set":
                colls = colls.filter(test_method="db")
                query['method']= request.POST['method']

        return render(request, 'website/base.html', {'colls':colls, 'query':query})

    else:
        return redirect('/')


    return render(request, 'website/base.html')
