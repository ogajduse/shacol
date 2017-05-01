bits = Collision.objects.values_list("bits").distinct()
data_tt = [['Bits']]
count_ih = 1
name_tt = "String method - total time/bits"
# generate values (bits) for the first column
for b in bits:
    data_tt.append([b[0]])

input_hashes = Collision.objects.values_list("input_hash").filter(test_method__icontains="String").distinct()
for ih in input_hashes:
    data_tt[0].append(ih[0])

datadict = dict()
for i in range(1, len(data_tt)):
    datadict[data_tt[i][0]] = i

for inp_hsh in range(1, len(data_tt[0]), 1):
    selected_in_hash = data_tt[0][inp_hsh]
    print("selected_in_hash: " + str(selected_in_hash))
    bitlist = list()
    bitlist_select = Collision.objects.values_list("bits").filter(test_method__icontains="Str", input_hash=selected_in_hash)
    for i in bitlist_select:
        bitlist.append(i[0])
    print("printing bitlist")
    print(bitlist)
    for bits in bitlist:
        print("actual bits: " + str(bits))
        time = Collision.objects.values_list("bits", "total_time").filter(test_method__icontains="Str", input_hash=selected_in_hash, bits=bits)
        print(time.values)
        #data_tt[datadict.get(time[0][0])][inp_hsh] = time[0][1]
        data_tt[datadict.get(time[0][0])].insert(inp_hsh, time[0][1])