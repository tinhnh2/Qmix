import os
import glob
import sys
list_zero = {}
count_zero = 0
def write_to_out(dataset, in_aln_name, list_out, id_out, count, list_zero):
    print("Open aln file: %s, id: %d, count: %d"%(in_aln_name,id_out,count))
    global count_zero
    if count < 10:
        print("Detect count = 0 with name: %s, id: %d"%(in_aln_name,id_out))
        list_zero[count_zero] = [in_aln_name,id_out]
        count_zero = count_zero + 1
        return
    in_aln = open("%s/%s" % (dataset,in_aln_name), "r")
    out_aln = open("step3_out%d/%s" % (id_out,in_aln_name), "w")
    first_line = in_aln.readline()
    number_clade = int(first_line.split()[0])
    out_aln.write("%d %d\n"%(number_clade, count))
    list_clade_out = {}
    list_aln_out = {}
    for i in range(number_clade):
        list_aln_out[i] = ""
    input_aln = {}
    input_aln_id = 0
    for line in in_aln:
        if not line.strip():
            continue
        str_line = line.split()
        list_clade_out[input_aln_id] = str_line[0]
        input_aln[input_aln_id] = str_line[1]
        input_aln_id = input_aln_id + 1
    for id in range(count):
        site = int(list_out[id])
        id_aln_out = 0
        for i in range(number_clade):
            input_line = input_aln[i]
            list_aln_out[id_aln_out] = list_aln_out[id_aln_out] + input_line[site-1]
            id_aln_out = id_aln_out + 1

    for id in range(number_clade):
        str_out = list_clade_out[id] + "  " + list_aln_out[id]
        out_aln.write("%s\n"%str_out)
    in_aln.close()
    out_aln.close()

def estimate_model():
    print("This procedure is to estimate new models")
def step3(dataset):
    for f in glob.glob(r"%s/*.phyml"%dataset):
	print("process file %s"%f)
	aln = f.split('/')[1]
        sitelh_file = open("%s.sitelh"%aln, "r")
        for i in range(11):
            sitelh_file.readline()
        list1 = {}
        list2 = {}
        list3 = {}
        list4 = {}
        id_out1 = 0
        id_out2 = 0
        id_out3 = 0
        id_out4 = 0
        for line in sitelh_file:
            list = line.split()
            site = int(list[0])
   	    lnLH = float(list[1])
	    max = float(list[2])
            id = 0
            if max < float(list[3]):
                max = float(list[3])
                id = 1
            if max < float(list[4]):
                max = float(list[4])
                id = 2
            if max < float(list[5]):
                max = float(list[5])
                id = 3
            if id == 0:
	        list1[id_out1] = site
                id_out1 = id_out1 + 1
	    if id == 1:
	        list2[id_out2] = site
                id_out2 = id_out2 + 1
	    if id == 2:
	        list3[id_out3] = site
                id_out3 = id_out3 + 1
   	    if id == 3:
	        list4[id_out4] = site
                id_out4 = id_out4 + 1
        write_to_out(dataset, aln, list1, 1, id_out1, list_zero)
        write_to_out(dataset, aln, list2, 2, id_out2, list_zero)
        write_to_out(dataset, aln, list3, 3, id_out3, list_zero)
        write_to_out(dataset, aln, list4, 4, id_out4, list_zero)
def rescale_tree(tree, rate, group_id, name, path):
    output = ""
    scale = rate
    length = len(tree)
    i = 0
    outFile = open("%s/out%d/%s.treefile"%(path,group_id,name),"w")
    while i < length:
        if tree[i] != ':' and tree[i] != ',' and tree[i] != ')' and tree[i] != ';':
            output = output + tree[i]
        else:
            count = 0
            if tree[i] == ':':
                number = ""
                output = output + ":"
                new_number = 0.0
                for j in range(i+1, length):
                    if tree[j] != ',' and tree[j] != ')' and tree[j] != ';':
                        number = number + tree[j]
                        count = count + 1
                    else:
                        new_number = scale * float(number)
                        output = output + str("%.10f"%new_number)
			#output = output + str(new_number)
                        break
            else:
                output = output + tree[i]
            i = i + count
        i = i + 1
    #print("Input  str: %s"%tree)
    #print("Output str: %s"%output)
    outFile.writelines(output)

def step4(dataset):
    for f in glob.glob(r"%s/*.phyml"%dataset):
	print("step4 %s"%f)
	aln = f.split('/')[1]
	treefiles = open("%s.treefile"%aln, "r")
	tree = treefiles.readline()
        cmd = "grep -A 4 \"Category  Relative_rate  Proportion\" %s.iqtree | tail -n4 > tmp_%s.iqtree"%(aln,aln)
        os.system(cmd)
        iqtree_file = open("tmp_%s.iqtree"%aln, "r")
	rate = {}
	rate[0] = iqtree_file.readline().split()[1]
	rate[1] = iqtree_file.readline().split()[1]
	rate[2] = iqtree_file.readline().split()[1]
	rate[3] = iqtree_file.readline().split()[1]
	iqtree_file.close()
	treefiles.close()
        for j in range(4):
	    print("Rate is %s"%rate[j])
            rescale_tree(tree, float(rate[j]), j+1, aln, "trees")
    for i in range(count_zero):
        cmd = ("rm trees/out%d/%s.treefile"%(list_zero[i][1],list_zero[i][0]))
        os.system(cmd)

def main(dataset):
    print("Start process...")
    step3(dataset)
    step4(dataset)

# call main function
if __name__ == '__main__':
    dataset = sys.argv[1]
    main(dataset)
