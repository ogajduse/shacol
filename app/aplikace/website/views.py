from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collision
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from django.db.models import Max, Min
from graphos.sources.model import ModelDataSource

def colls(request):
    colls = Collision.objects.all()
    return render(request, 'website/collision.html', {'colls': colls})

def graphs(request):
    max_bits_str = (Collision.objects.filter(test_method__icontains="Str").aggregate(Max('bits'))['bits__max']) + 1
    max_bits_int = (Collision.objects.filter(test_method__icontains="Int").aggregate(Max('bits'))['bits__max']) + 1
    max_bits_db = (Collision.objects.filter(test_method__icontains="db").aggregate(Max('bits'))['bits__max']) + 1
    max_bit_list = [max_bits_str, max_bits_int, max_bits_db]
    max_bits = min(max_bit_list)
    min_bits_str = Collision.objects.filter(test_method__icontains="Str").aggregate(Min('bits'))['bits__min']
    min_bits_int = Collision.objects.filter(test_method__icontains="Int").aggregate(Min('bits'))['bits__min']
    min_bits_db = Collision.objects.filter(test_method__icontains="db").aggregate(Min('bits'))['bits__min']
    min_bit_list = [min_bits_str, min_bits_int, min_bits_db]
    min_bits = max(min_bit_list)

    data_tt = [['Bits', 'Int method', 'String method', 'DB Set method']]
    name_tt = "All methods - total time/bits"
    for b in range(min_bits, max_bits , 4):
        colls_int = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="Int", bits=b)
        colls_str = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="String", bits=b)
        colls_db = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="db", bits=b)
        for bits, time in colls_int:
            tmp = [bits, time]
        for bits, time in colls_str:
            tmp.append(time)
        for bits, time in colls_db:
            tmp.append(time)
        data_tt.append(tmp)

    data_ho = [['Bits', 'Int method', 'String method', 'DB Set method']]
    name_ho = "All - index of collison hash/total bits"
    for b in range(min_bits, max_bits , 4):
        colls_int = Collision.objects.values_list("bits", "hash_order").filter(test_method__icontains="Int", bits=b)
        colls_str = Collision.objects.values_list("bits", "hash_order").filter(test_method__icontains="String", bits=b)
        colls_db = Collision.objects.values_list("bits", "hash_order").filter(test_method__icontains="db", bits=b)
        for bits, ho in colls_int:
            tmp = [bits, ho]
        for bits, ho in colls_str:
            tmp.append(ho)
        for bits, ho in colls_db:
            tmp.append(ho)
        data_ho.append(tmp)

    data_tm = [['Bits', 'Int method', 'String method', 'DB Set method']]
    name_tm = "All - index of collison hash/total bits"
    for b in range(min_bits, max_bits , 4):
        colls_int = Collision.objects.values_list("bits", "total_memory").filter(test_method__icontains="Int", bits=b)
        colls_str = Collision.objects.values_list("bits", "total_memory").filter(test_method__icontains="String", bits=b)
        colls_db = Collision.objects.values_list("bits", "total_memory").filter(test_method__icontains="db", bits=b)
        for bits, tm in colls_int:
            tmp = [bits, tm]
        for bits, tm in colls_str:
            tmp.append(tm)
        for bits, tm in colls_db:
            tmp.append(tm)
        data_tm.append(tmp)


    if 'graphmethod' in request.POST:
        if request.POST['graphmethod'] == "str":
            data_tt = [['Bits', 'Total time [s]']]
            colls = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="String")
            name_tt = "String method - total time/bits"
            for bits, time in colls:
                data_tt.append([bits, time])

            data_ho = [['Bits', 'Hashes']]
            colls_ho= Collision.objects.values_list("bits", "hash_order").filter(test_method__icontains="String")
            name_ho = "String method - count of cycles/total bits"
            for bits, hashes in colls_ho:
                data_ho.append([bits, hashes])

            data_tm = [['Bits', 'Total memory [MB]']]
            colls_tm = Collision.objects.values_list("bits", "total_memory").filter(test_method__icontains="String")
            name_tm = "String method - bits/total memory"
            for bits, memory in colls_tm:
                data_tm.append([bits, memory])


        elif request.POST['graphmethod'] == "int":
            data_tt = [['Bits', 'Total time [s]']]
            colls = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="Int")
            name_tt = "Int method - total time/bits"
            for bits, time in colls:
                data_tt.append([bits, time])

            data_ho = [['Bits', 'Hashes']]
            colls_ho= Collision.objects.values_list("bits", "hash_order").filter(test_method__icontains="Int")
            name_ho = "Int method - count of cycles/total bits"
            for bits, hashes in colls_ho:
                data_ho.append([bits, hashes])

            data_tm = [['Bits', 'Total memory [MB]']]
            colls_tm = Collision.objects.values_list("bits", "total_memory").filter(test_method__icontains="Int")
            name_tm = "Int method - bits/total memory"
            for bits, memory in colls_tm:
                data_tm.append([bits, memory])

        elif request.POST['graphmethod'] == "db":
            data_tt = [['Bits', 'Total time [s]']]
            colls = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="DB")
            name_tt = "DB Set method - total time/bits"
            for bits, time in colls:
                data_tt.append([bits, time])

            data_ho = [['Bits', 'Hashes']]
            colls_ho= Collision.objects.values_list("bits", "hash_order").filter(test_method__icontains="db")
            name_ho = "DB Set method - count of cycles/total bits"
            for bits, hashes in colls_ho:
                data_ho.append([bits, hashes])

        elif request.POST['graphmethod'] == "all":
            pass

    data_source_tt = SimpleDataSource(data=data_tt)
    chart_tt = LineChart(data_source_tt, options={'title': name_tt})

    data_source_ho = SimpleDataSource(data=data_ho)
    chart_ho = LineChart(data_source_ho, options={'title': name_ho})

    data_source_tm = SimpleDataSource(data=data_tm)
    chart_tm = LineChart(data_source_tm, options={'title': name_tm})
    return render(request, 'website/graphs.html', {'chart': chart_tt, 'chart2': chart_ho, 'chart3': chart_tm})
    #return redirect('/')

def delete(request):
    colls = Collision.objects.all()
    colls.delete()
    return redirect('/')

def filtering(request):
    if 'method' in request.POST:
        colls = Collision.objects.all()
        if request.POST['method'] == "str":
            colls = colls.filter(test_method__icontains='String')

        elif request.POST['method'] == "int":
            colls = colls.filter(test_method__icontains='Int')

        elif request.POST['method'] == "db":
            colls = colls.filter(test_method__icontains="DB")

        elif request.POST['method'] == "all":
            pass

    return render(request, 'website/collision.html', {'colls':colls})
