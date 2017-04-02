from django.shortcuts import render
from django.http import HttpResponse
from .models import Collision
import sqlite3
# Create your views here.
def colls(request):
    collisions = Collision.objects.all()
    return render(request, 'website/base.html', {'collisions': collisions})


def method(request):
    return render(request, 'website/base.html')
