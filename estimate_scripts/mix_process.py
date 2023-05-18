import numpy as np
import os
import time
import sys
import glob
os.environ["CURR_DIR"] = os.getcwd()
site_rate_type = "4x"
def create_bjob_file(folder, loop_id):
    # Run Modelfinder on training set
    if site_rate_type == "4x":
        cmd = "cp run_step3_4x.sh %s/"%(folder)
    else:
	cmd = "cp run_step3_4m.sh %s/"%(folder)
    os.system(cmd)
    if loop_id == 1:
        cmd = 'cp Q.LG %s/Q.step3.4x.1'%(folder)
        os.system(cmd)
        cmd = 'cp Q.LG %s/Q.step3.4x.2'%(folder)
        os.system(cmd)
        cmd = 'cp Q.LG %s/Q.step3.4x.3'%(folder) 
        os.system(cmd)
        cmd = 'cp Q.LG %s/Q.step3.4x.4'%(folder)
        os.system(cmd)
    if site_rate_type == "4x":
        cmd = 'sh run.sh %d run_step3_4x.sh'%loop_id
    else:
        cmd = 'sh run.sh %d run_step3_4m.sh'%loop_id
    os.system(cmd)
    print(cmd)

def pearon_corr(model1, model2):
    print(model1)
    print(model2)
    file1 = open(model1,"r")
    file2 = open(model2,"r")
    list1 = [0]*190
    list2 = [0]*190
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
def do_step3(loop_id):
    print("This is step 3")
    number_core = 4
    cmd = "mkdir -p loop%d/step3"%(loop_id)
    os.system(cmd)
    cmd = "cp -rf data loop%d/step3/"%(loop_id)
    os.system(cmd)
    path="loop%d/step3/"%loop_id
    create_bjob_file(path,loop_id)
    
def do_step4(loop_id):
    cmd = 'sh step4.sh %d'%(loop_id)
    os.system(cmd)
    
def do_step5(loop_id):
    print("This is step 5")
    cmd = "sh step5.sh %d"%(loop_id)
    os.system(cmd)

def loop(loop_id):
    print("Continue loop %d"%loop_id)
    do_step3(loop_id)
    
    while 1:
	check = 0
	if str(os.path.exists("loop%d/step3/step3.iqtree"%(loop_id))) == "True":
	    break;
	else:
	    time.sleep(10)
    print("Finish step3, continue to step4_5")
    do_step4(loop_id)
    do_step5(loop_id)
    while 1:
        check = 0
        for i in range(1,5):
            if str(os.path.exists("loop%d/step5/Q.step5.4x.%d"%(loop_id,i))) == "True":
                check = check + 1
        if check < 4:
            time.sleep(10)
        else:
            break
    print("Finish loop %d"%loop_id)

def main(corr_thres,loop_undo):
    print("Start process...: ")
    loop_id = 1
    exit_loop = 0
    while exit_loop == 0:
        if str(os.path.exists("un.do")) != "True":
	    loop(loop_id)
	else:
	    loop_id = int(loop_undo)
	    cmd = "rm un.do"
	    os.system(cmd)
	cmd = "sh normalized.sh %d"%loop_id
	os.system(cmd)
        corr1 = pearon_corr("loop%d/step5/Q.step3.4x.1"%loop_id,"loop%d/step5/Q.step5.4x.1.normalized"%loop_id)
        corr2 = pearon_corr("loop%d/step5/Q.step3.4x.2"%loop_id,"loop%d/step5/Q.step5.4x.2.normalized"%loop_id)
        corr3 = pearon_corr("loop%d/step5/Q.step3.4x.3"%loop_id,"loop%d/step5/Q.step5.4x.3.normalized"%loop_id)
        corr4 = pearon_corr("loop%d/step5/Q.step3.4x.4"%loop_id,"loop%d/step5/Q.step5.4x.4.normalized"%loop_id)
        print("Pearson correllation: %.8f, %.8f, %.8f, %.8f"%(corr1,corr2,corr3,corr4))
        if corr1 < float(corr_thres) or corr2 < float(corr_thres) or corr3 < float(corr_thres) or corr4 < float(corr_thres):
            cmd = "cp -rf loop%d loop%d"%(loop_id,loop_id+1)
            os.system(cmd)
	    cmd = "sh reset_models.sh %d"%(loop_id+1)
	    os.system(cmd)
	    loop_id = loop_id + 1
        else:
	    exit_loop = 1
            print("Finish process")

# call main function
# python mix_process.py 4x 29 51 1 0.999. This is for 4x type, 51 group, 29 aln each group, undo loop with id = 1 and corr thres is 0.999
if __name__ == '__main__':
    site_rate_type = sys.argv[1]
    loop_undo = sys.argv[2]
    corr_thres = sys.argv[3]
    main(corr_thres,loop_undo)
