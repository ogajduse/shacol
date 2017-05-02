bits = Collision.objects.values_list("bits").distinct()
data = [['Bits']]
name_tt = "String method - total time/bits"
name_ho = "String method - count of cycles/total bits"
#data_tt = []
#data_ho = []
""""
colls_ho= Collision.objects.values_list("bits", "hash_order").filter(test_method__icontains="String")
"""
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
    print("selected_in_hash: " + str(selected_in_hash))
    bitlist = list()
    bitlist_select = Collision.objects.values_list("bits").filter(test_method__icontains="Str", input_hash=selected_in_hash)
    for i in bitlist_select:
        bitlist.append(i[0])
    print("printing bitlist")
    print(bitlist)
    for bits in bitlist:
        print("actual bits: " + str(bits))
        print("POINT1 data_tt before insert " + str(data))
        time = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="Str", input_hash=selected_in_hash, bits=bits)
        print(time.values)
        cycles = Collision.objects.values_list("bits", "cycles").filter(test_method__icontains="Str", input_hash=selected_in_hash, bits=bits)
        print(cycles.values)
        print("first arg time: " + str(datadict.get(time[0][0])))
        print("first arg cycles: " + str(datadict.get(cycles[0][0])))
        print("data_tt before insert " + str(data_tt))
        data_tt[datadict.get(time[0][0])].insert(inp_hsh, time[0][1])
        print("data_tt after insert " + str(data_tt))
        print("data_ho before insert " + str(data_ho))
        data_ho[datadict.get(cycles[0][0])].insert(inp_hsh, cycles[0][1])
        print("data_ho after insert " + str(data_ho))

