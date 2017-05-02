from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Collision
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart
from django.db.models import Max, Min
from graphos.sources.model import ModelDataSource
import copy

def colls(request):
    colls = Collision.objects.all()
    return render(request, 'website/collision.html', {'colls': colls})

def graphs(request):
    if 'graphmethod' in request.POST:
        if request.POST['graphmethod'] == "str":
            bits = Collision.objects.values_list("bits").filter(test_method__icontains="str").distinct()
            data = [['Bits']]
            name_tt = "String method - total time/bits"
            name_ho = "String method - count of cycles/total bits"
            # generate values (bits) for the first column
            for b in bits:
                data.append([b[0]])

            input_hashes = Collision.objects.values_list("input_hash").filter(test_method__icontains="String").distinct()
            for ih in input_hashes:
                data[0].append(ih[0])

            data_tt = copy.deepcopy(data)
            data_ho = copy.deepcopy(data)

            datadict = dict()
            for i in range(1, len(data)):
                datadict[data[i][0]] = i

            for inp_hsh in range(1, len(data[0]), 1):
                selected_in_hash = data[0][inp_hsh]
                #print("selected_in_hash: " + str(selected_in_hash))
                bitlist = list()
                bitlist_select = Collision.objects.values_list("bits").filter(test_method__icontains="Str", input_hash=selected_in_hash)
                for i in bitlist_select:
                    bitlist.append(i[0])
                #print("printing bitlist")
                #print(bitlist)
                for bits in bitlist:
                    #print("actual bits: " + str(bits))
                    time = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="Str", input_hash=selected_in_hash, bits=bits)
                    #print(time.values)
                    cycles = Collision.objects.values_list("bits", "cycles").filter(test_method__icontains="Str", input_hash=selected_in_hash, bits=bits)
                    #print(cycles.values)
                    #print("first arg time: " + str(datadict.get(time[0][0])))
                    #print("data_tt before insert " + str(data_tt))
                    data_tt[datadict.get(time[0][0])].insert(inp_hsh, time[0][1])
                    #print("data_tt after insert " + str(data_tt))
                    #print("data_ho before insert " + str(data_ho))
                    data_ho[datadict.get(cycles[0][0])].insert(inp_hsh, cycles[0][1])
                    #print("data_ho after insert " + str(data_ho))

        elif request.POST['graphmethod'] == "int":
            bits = Collision.objects.values_list("bits").filter(test_method__icontains="int").distinct()
            data = [['Bits']]
            name_tt = "Int method - total time/bits"
            name_ho = "Int method - count of cycles/total bits"
            for b in bits:
                data.append([b[0]])

            input_hashes = Collision.objects.values_list("input_hash").filter(test_method__icontains="Int").distinct()
            for ih in input_hashes:
                data[0].append(ih[0])

            data_tt = copy.deepcopy(data)
            data_ho = copy.deepcopy(data)

            datadict = dict()
            for i in range(1, len(data)):
                datadict[data[i][0]] = i

            for inp_hsh in range(1, len(data[0]), 1):
                selected_in_hash = data[0][inp_hsh]
                bitlist = list()
                bitlist_select = Collision.objects.values_list("bits").filter(test_method__icontains="Int", input_hash=selected_in_hash)
                for i in bitlist_select:
                    bitlist.append(i[0])
                for bits in bitlist:
                    time = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="Int", input_hash=selected_in_hash, bits=bits)
                    cycles = Collision.objects.values_list("bits", "cycles").filter(test_method__icontains="Int", input_hash=selected_in_hash, bits=bits)
                    data_tt[datadict.get(time[0][0])].insert(inp_hsh, time[0][1])
                    data_ho[datadict.get(cycles[0][0])].insert(inp_hsh, cycles[0][1])

        elif request.POST['graphmethod'] == "db":
            #max_bits_db = (Collision.objects.filter(test_method__icontains="db").aggregate(Max('bits'))['bits__max']) + 1
            bits = Collision.objects.values_list("bits").filter(test_method__icontains="db").distinct()
            data = [['Bits']]
            name_tt = "DB Set method - total time/bits"
            name_ho = "DB Set method - count of cycles/total bits"
            for b in bits:
                data.append([b[0]])

            input_hashes = Collision.objects.values_list("input_hash").filter(test_method__icontains="db").distinct()
            for ih in input_hashes:
                data[0].append(ih[0])

            data_tt = copy.deepcopy(data)
            data_ho = copy.deepcopy(data)

            datadict = dict()
            for i in range(1, len(data)):
                datadict[data[i][0]] = i

            for inp_hsh in range(1, len(data[0]), 1):
                selected_in_hash = data[0][inp_hsh]
                bitlist = list()
                bitlist_select = Collision.objects.values_list("bits").filter(test_method__icontains="db", input_hash=selected_in_hash)
                for i in bitlist_select:
                    bitlist.append(i[0])
                for bits in bitlist:
                    time = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="db", input_hash=selected_in_hash, bits=bits)
                    cycles = Collision.objects.values_list("bits", "cycles").filter(test_method__icontains="db", input_hash=selected_in_hash, bits=bits)
                    data_tt[datadict.get(time[0][0])].insert(inp_hsh, time[0][1])
                    data_ho[datadict.get(cycles[0][0])].insert(inp_hsh, cycles[0][1])

        elif request.POST['graphmethod'] == "all":
            pass

        data_source_tt = SimpleDataSource(data=data_tt)
        chart_tt = LineChart(data_source_tt, options={'title': name_tt})

        data_source_ho = SimpleDataSource(data=data_ho)
        chart_ho = LineChart(data_source_ho, options={'title': name_ho})

        return render(request, 'website/graphs.html', {'chart': chart_tt, 'chart2': chart_ho})
    return render(request, 'website/graphs.html')
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
