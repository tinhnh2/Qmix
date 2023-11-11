#!/usr/bin/env python3.8
import argparse
import os
import sys
import numpy as np
import time
import glob

CURR_DIR = os.getcwd()
print("Current dir: %s" % CURR_DIR)
time_model = "GTR20"
site_rate_type = "4X"
data_path = ""
corr_thres = 0.95
number_thread = 8
start_matrix = "LG"


def normalize(input_file):
    in_file = open(input_file, 'r')
    out_file = open("%s.normalized" % input_file, 'w')
    R = [[0.0] * 20] * 20
    Q = [[0.0] * 20] * 20
    Pi = [0.0] * 20
    for i in range(1, 20):
        line = in_file.readline()
        line = line.split()
        A = [0.0] * 20
        for j in range(0, i):
            A[j] = float(line[j])
        R[i] = A
    line = in_file.readline()
    line = line.split()
    for ii in range(20):
        Pi[ii] = float(line[ii])
    for i in range(20):
        for j in range(20):
            if j > i:
                R[i][j] = R[j][i]
    for i in range(20):
        A = [0.0] * 20
        for j in range(20):
            A[j] = Pi[j] * R[i][j]
        Q[i] = A
    for i in range(20):
        temp = 0.0
        for j in range(20):
            if i != j:
                temp += Q[i][j]
        Q[i][i] = -temp
    miu = 0
    for x in range(20):
        miu = miu - Pi[x] * Q[x][x]
    for i in range(20):
        for j in range(20):
            if j < i:
                R[i][j] = R[i][j] / miu
    for i in range(20):
        for j in range(20):
            if i > j:
                out_file.writelines("%f " % R[i][j])
        if i > 0:
            out_file.writelines("\n")

    for i in range(20):
        out_file.writelines("%f " % Pi[i])
    in_file.close()
    out_file.close()


def run_step2(folder, loop_id):
    # Run Modelfinder on training set
    if loop_id == 1:
        cmd = 'cp initial_models/%s %s/Q.step2.4x.1' % (start_matrix, folder)
        os.system(cmd)
        cmd = 'cp initial_models/%s %s/Q.step2.4x.2' % (start_matrix, folder)
        os.system(cmd)
        cmd = 'cp initial_models/%s %s/Q.step2.4x.3' % (start_matrix, folder)
        os.system(cmd)
        cmd = 'cp initial_models/%s %s/Q.step2.4x.4' % (start_matrix, folder)
        os.system(cmd)
    os.chdir("%s/loop%d/step2" % (CURR_DIR, loop_id))
    if site_rate_type == "4X" or site_rate_type == "4x":
        for aln_file in glob.glob(r"data/*.phyml"):
            aln_name = aln_file.split('/')[1]
            cmd = "iqtree2 -seed 1 -T %d -s %s --prefix %s -m \"MIX{Q.step2.4x.1,Q.step2.4x.2,Q.step2.4x.3,Q.step2.4x.4}*R4\" --no-seq-comp -wslmr" % (
                number_thread, aln_file, aln_name)
            os.system(cmd)
    else:
        for aln_file in glob.glob(r"data/*.phyml"):
            aln_name = aln_file.split('/')[1]
            cmd = "iqtree2 -seed 1 -T %d -s %s --prefix %s -m \"MIX{Q.step2.4x.1,Q.step2.4x.2,Q.step2.4x.3,Q.step2.4x.4}*G4\" --no-seq-comp -wslmr" % (
                number_thread, aln_file, aln_name)
            os.system(cmd)
    cmd = "touch step2.iqtree"
    os.system(cmd)


def pearon_corr(model1, model2):
    print(model1)
    print(model2)
    file1 = open(model1, "r")
    file2 = open(model2, "r")
    len_ = 190
    if time_model != "GTR20":
        len_ = 400
    list1 = [0]*len_
    list2 = [0]*len_
    line1 = file1.read().split()
    line2 = file2.read().split()
    line1 = line1[:-20]
    line2 = line2[:-20]
    for i in range(len(line1)):
        list1[i] = float(line1[i])
        list2[i] = float(line2[i])
    matrix = np.corrcoef(list1, list2)
    corr = matrix[0][1]
    return corr


def do_step2(loop_id):
    print("This is step 3")
    if loop_id == 1:
        if str(os.path.exists("loop%d" % loop_id)) == "True":
            cmd = "rm -rf loop%d" % loop_id
            os.system(cmd)
        cmd = "mkdir -p loop%d/step2" % (loop_id)
        os.system(cmd)
        cmd = "cp -rf %s loop%d/step2/data" % (data_path, loop_id)
        os.system(cmd)
    path = "loop%d/step2/" % loop_id
    run_step2(path, loop_id)


list_zero = {}
count_zero = 0


def write_to_out(dataset, in_aln_name, list_out, id_out, count, list_zero):
    print("Open aln file: %s, id: %d, count: %d" %
          (in_aln_name, id_out, count))
    global count_zero
    if count < 10:
        print("Detect count = 0 with name: %s, id: %d" % (in_aln_name, id_out))
        list_zero[count_zero] = [in_aln_name, id_out]
        count_zero = count_zero + 1
        return
    in_aln = open("%s/%s" % (dataset, in_aln_name), "r")
    out_aln = open("step2_out%d/%s" % (id_out, in_aln_name), "w")
    first_line = in_aln.readline()
    number_clade = int(first_line.split()[0])
    out_aln.write("%d %d\n" % (number_clade, count))
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
            list_aln_out[id_aln_out] = list_aln_out[id_aln_out] + \
                input_line[site-1]
            id_aln_out = id_aln_out + 1

    for id in range(number_clade):
        str_out = list_clade_out[id] + "  " + list_aln_out[id]
        out_aln.write("%s\n" % str_out)
    in_aln.close()
    out_aln.close()


def step2(dataset):
    for f in glob.glob(r"%s/*.*" % dataset):
        print("process file %s" % f)
        aln = f.split('/')[1]
        if str(os.path.exists("%s.sitelh" % (aln))) == "False":
            print("Remove file %s/%s" % (dataset, aln))
            cmd = "rm %s/%s" % (dataset, aln)
            os.system(cmd)
            continue
        sitelh_file = open("%s.sitelh" % aln, "r")
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
    outFile = open("%s/out%d/%s.treefile" % (path, group_id, name), "w")
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
                        output = output + str("%.10f" % new_number)
                        break
            else:
                output = output + tree[i]
            i = i + count
        i = i + 1
    outFile.writelines(output)


def step3(dataset):
    for f in glob.glob(r"%s/*.*" % dataset):
        print("step3 %s" % f)
        aln = f.split('/')[1]
        treefiles = open("%s.treefile" % aln, "r")
        tree = treefiles.readline()
        cmd = "grep -A 4 \"Category  Relative_rate  Proportion\" %s.iqtree | tail -n4 > tmp_%s.iqtree" % (aln, aln)
        os.system(cmd)
        iqtree_file = open("tmp_%s.iqtree" % aln, "r")
        rate = {}
        rate[0] = iqtree_file.readline().split()[1]
        rate[1] = iqtree_file.readline().split()[1]
        rate[2] = iqtree_file.readline().split()[1]
        rate[3] = iqtree_file.readline().split()[1]
        iqtree_file.close()
        treefiles.close()
        for j in range(4):
            print("Rate is %s" % rate[j])
            rescale_tree(tree, float(rate[j]), j+1, aln, "trees")
    for i in range(count_zero):
        cmd = ("rm trees/out%d/%s.treefile" % (list_zero[i][1], list_zero[i][0]))
        os.system(cmd)


def main_step3(dataset):
    print("Start process...")
    step2(dataset)
    step3(dataset)


def do_step3(loop_id):
    cmd = "mkdir -p loop%d/step3" % (loop_id)
    os.system(cmd)
    os.chdir("%s/loop%d/step3" % (CURR_DIR, loop_id))
    os.system(cmd)
    cmd = "mkdir step2_out1; mkdir step2_out2; mkdir step2_out3; mkdir step2_out4; mkdir -p trees/out1; mkdir -p trees/out2; mkdir -p trees/out3; mkdir -p trees/out4"
    os.system(cmd)
    cmd = "cp -rf ../step2/* ."
    os.system(cmd)
    main_step3("data")


def do_step4(loop_id):
    print("This is step 5")
    os.chdir("%s"%CURR_DIR)
    cmd = "mkdir -p loop%d/step4" % (loop_id)
    os.system(cmd)
    os.chdir("%s/loop%d/step4" % (CURR_DIR, loop_id))
    cmd = "rm step4*"
    os.system(cmd)
    cmd = "cat ../step3/trees/out1/* > tree1.treefile;cat ../step3/trees/out2/* > tree2.treefile;cat ../step3/trees/out3/* > tree3.treefile;cat ../step3/trees/out4/* > tree4.treefile"
    os.system(cmd)
    cmd = "mkdir out1;mkdir out2;mkdir out3;mkdir out4"
    os.system(cmd)
    cmd = "cp ../step3/step2_out1/* out1/"
    os.system(cmd)
    cmd = "cp ../step3/step2_out2/* out2/"
    os.system(cmd)
    cmd = "cp ../step3/step2_out3/* out3/"
    os.system(cmd)
    cmd = "cp ../step3/step2_out4/* out4/"
    os.system(cmd)

    cmd = "cp ../step2/Q.step2.4x* ."
    os.system(cmd)
    cmd = "iqtree2 -seed 1 -st AA -T %d -S out1  -te tree1.treefile --model-joint GTR20+FO --init-model Q.step2.4x.1  --prefix step4.1 " % (
        number_thread)
    os.system(cmd)
    cmd = "grep -A 22 \"can be used as input for IQ-TREE\" step4.1.iqtree | tail -n21 > Q.step4.4x.1"
    os.system(cmd)
    cmd = "iqtree2 -seed 1 -st AA -T %d -S out2  -te tree2.treefile --model-joint GTR20+FO --init-model Q.step2.4x.2  --prefix step4.2 " % (
        number_thread)
    os.system(cmd)
    cmd = "grep -A 22 \"can be used as input for IQ-TREE\" step4.2.iqtree | tail -n21 > Q.step4.4x.2"
    os.system(cmd)
    cmd = "iqtree2 -seed 1 -st AA -T %d -S out3  -te tree3.treefile --model-joint GTR20+FO --init-model Q.step2.4x.3  --prefix step4.3 " % (
        number_thread)
    os.system(cmd)
    cmd = "grep -A 22 \"can be used as input for IQ-TREE\" step4.3.iqtree | tail -n21 > Q.step4.4x.3"
    os.system(cmd)
    cmd = "iqtree2 -seed 1 -st AA -T %d -S out4  -te tree4.treefile --model-joint GTR20+FO --init-model Q.step2.4x.4  --prefix step4.4 " % (
        number_thread)
    os.system(cmd)
    cmd = "grep -A 22 \"can be used as input for IQ-TREE\" step4.4.iqtree | tail -n21 > Q.step4.4x.4"
    os.system(cmd)


def loop(loop_id):
    print("Continue loop %d" % loop_id)
    do_step2(loop_id)
    os.chdir("%s" % CURR_DIR)
    while 1:
        check = 0
        if str(os.path.exists("loop%d/step2/step2.iqtree" % (loop_id))) == "True":
            break
        else:
            time.sleep(10)
    print("Finish step2, continue to step3_5")
    do_step3(loop_id)
    do_step4(loop_id)
    os.chdir("%s"%CURR_DIR)
    while 1:
        check = 0
        for i in range(1, 5):
            if str(os.path.exists("loop%d/step4/Q.step4.4x.%d" % (loop_id, i))) == "True":
                check = check + 1
        if check < 4:
            time.sleep(10)
        else:
            break
    print("Finish loop %d" % loop_id)


def main_run():
    print("Start process...: ")
    print("Data path: %s" % data_path)
    loop_id = 1
    exit_loop = 0
    while exit_loop == 0:
	global count_zero
	count_zero = 0
        loop(loop_id)
        os.chdir("%s" % CURR_DIR)
        corr1 = pearon_corr("loop%d/step4/Q.step2.4x.1" %
                            loop_id, "loop%d/step4/Q.step4.4x.1" % loop_id)
        corr2 = pearon_corr("loop%d/step4/Q.step2.4x.2" %
                            loop_id, "loop%d/step4/Q.step4.4x.2" % loop_id)
        corr3 = pearon_corr("loop%d/step4/Q.step2.4x.3" %
                            loop_id, "loop%d/step4/Q.step4.4x.3" % loop_id)
        corr4 = pearon_corr("loop%d/step4/Q.step2.4x.4" %
                            loop_id, "loop%d/step4/Q.step4.4x.4" % loop_id)
        print("Pearson correllation: %.8f, %.8f, %.8f, %.8f" %
              (corr1, corr2, corr3, corr4))
        if corr1 < float(corr_thres) or corr2 < float(corr_thres) or corr3 < float(corr_thres) or corr4 < float(corr_thres):
            cmd = "cp -rf loop%d loop%d" % (loop_id, loop_id+1)
            os.system(cmd)
	    cmd = "cp -rf loop%d/step2/data loop%d/step4/"%(loop_id + 1, loop_id + 1)
	    os.system(cmd)
	    cmd = "rm loop%d/step2/*"%(loop_id + 1)
	    os.system(cmd)
	    cmd = "cp -rf loop%d/step4/data loop%d/step2/"%(loop_id + 1, loop_id + 1)
	    os.system(cmd)
	    cmd = "cp loop%d/step4/Q.step4.4x.1 loop%d/step2/Q.step2.4x.1"%(loop_id + 1, loop_id + 1)
	    os.system(cmd)
	    cmd = "cp loop%d/step4/Q.step4.4x.2 loop%d/step2/Q.step2.4x.2"%(loop_id + 1, loop_id + 1)
	    os.system(cmd)
	    cmd = "cp loop%d/step4/Q.step4.4x.3 loop%d/step2/Q.step2.4x.3"%(loop_id + 1, loop_id + 1)
	    os.system(cmd)
	    cmd = "cp loop%d/step4/Q.step4.4x.4 loop%d/step2/Q.step2.4x.4"%(loop_id + 1, loop_id + 1)
	    os.system(cmd)
	    cmd = "rm -rf loop%d/step3/*"%(loop_id + 1)
	    os.system(cmd)
	    cmd = "rm -rf loop%d/step4/*"%(loop_id + 1)
	    os.system(cmd)
            loop_id = loop_id + 1
        else:
            exit_loop = 1
            normalize("loop%d/step4/Q.step4.4x.1" % loop_id)
            normalize("loop%d/step4/Q.step4.4x.2" % loop_id)
            normalize("loop%d/step4/Q.step4.4x.3" % loop_id)
            normalize("loop%d/step4/Q.step4.4x.4" % loop_id)
            cmd = "cp loop%d/step4/Q.step4.4x.1.normalized Q.1" % loop_id
            os.system(cmd)
            cmd = "cp loop%d/step4/Q.step4.4x.2.normalized Q.2" % loop_id
            os.system(cmd)
            cmd = "cp loop%d/step4/Q.step4.4x.3.normalized Q.3" % loop_id
            os.system(cmd)
            cmd = "cp loop%d/step4/Q.step4.4x.4.normalized Q.4" % loop_id
            os.system(cmd)
            print("Finish process")


def run(args):
    global site_rate_type
    site_rate_type = args.model
    global corr_thres
    corr_thres = args.cor
    global number_thread
    number_thread = int(args.threads)
    global start_matrix
    start_matrix = args.initial
    global data_path
    data_path = args.data
    print("mode; %s, cor: %s, theads: %d, initia: %s, dat_path: %s" %
          (site_rate_type, corr_thres, number_thread, start_matrix, data_path))
    main_run()


# call main function
if __name__ == '__main__':
    print("STARTING QMIX...")
    parser = argparse.ArgumentParser(description='QMix')
    parser.add_argument('-model',
                        type=str,
                        default='4M',
                        choices=['4M', '4X'])

    parser.add_argument('-cor',
                        type=str,
                        default="0.99",
                        help='the correlation threshold')

    parser.add_argument('-threads',
                        type=str,
                        default="18",
                        help='The number of computing threads')

    parser.add_argument('-initial',
                        type=str,
                        default='LG',
                        help='The initial matrix')
    parser.add_argument('-data',
                        type=str,
                        default='',
                        help='The full path of training alignment dataset')

    args = parser.parse_args(sys.argv[1:])

    run(args)
