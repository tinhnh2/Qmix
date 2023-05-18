import glob
from random import randint
# import statistics
from scipy.stats import normaltest
fp_hssp4x = 6
fp_hssp4m = 1
fp_lg4x = 6
fp_lg4m = 1
fp_pfam = 1
fp_lg = 0
fp_lgR4 = 6
fp_lgG4 = 1
fp_c20 = 20
fp_c60 = 60
fp_ul3 = 3
fp_exeho = 6
fp_cf4 = 24
out_file = open("rell_test.out", "w")
def rell_test(in1, in2, dataset, fp1, fp2):
    print("RELL test for %s and %s for %s" % (in1, in2, dataset))
    outname = "rell_output/%s_%s.%s.out"%(in1,in2,dataset)
    out_for_each = open(outname,"w")
    out_file.writelines("RELL test for %s and %s with %s\n"%(in1,in2,dataset))
    sum_count1 = 0
    sum_count2 = 0
    file_path = ""
    if dataset == "hssp":
        file_path = "results/hssp_test/*.phy"
    else:
	file_path = "results/treebase_test/*.Phy"
    for f in glob.glob(r"%s"%file_path):
        f_name = f.split('/')[2]
        f_1 = open("results/%s_%s_results/sitelh/test_%s.sitelh"%(in1,dataset,f_name),"r")
        f_2 = open("results/%s_%s_results/sitelh/test_%s.sitelh"%(in2,dataset,f_name),"r")
        sites = int(f_1.readline().split()[1])
        f_2.readline()
        arr1 = f_1.readline().split()[1:]
        arr2 = f_2.readline().split()[1:]
        sample1 = [0.0]*sites
        sample2 = [0.0]*sites
        for i in range(sites):
            sample1[i] = float(arr1[i])
            sample2[i] = float(arr2[i])
        org_sum1 = sum(sample1)
        org_sum2 = sum(sample2)
        aic1 = 2*fp1 - 2*org_sum1
        aic2 = 2*fp2 - 2*org_sum2
        delta_aic = aic1 - aic2
        # print("delta_aic: ",delta_aic)
        statistic_array = [0.0]*10000
        # out_file = open("out.aic_v", "w")
        for m in range(10000):
            aic1 = 0.0
            aic2 = 0.0
            x = [randint(0, sites - 1) for p in range(0, sites)]
            sample_1 = [0.0] * sites
            sample_2 = [0.0] * sites
            for i in range(sites):
                sample_1[i] = float(arr1[x[i]])
                sample_2[i] = float(arr2[x[i]])
            aic1 = 2*fp1 - 2*sum(sample_1)
            aic2 = 2*fp2 - 2*sum(sample_2)
            statistic_array[m] = aic1 - aic2
            # out_file.write("%f\n"%(aic1-aic2))
        # out_file.close()
        # mean = statistics.mean(statistic_array)
        # print("Mean: ",mean)
        # print("2.57*mean = ",2.57*mean)
        z_score, pvalue = normaltest(statistic_array)
        # print("z_score: %f, pvalue: %f"%(z_score,pvalue))
        # stddev = statistics.stdev(statistic_array)
        # print("stddev: ",stddev)
        if pvalue < 0.01:
            if delta_aic < 0:
                sum_count1 += 1
		out_for_each.writelines("1\n")	
            else:
                sum_count2 += 1
		out_for_each.writelines("2\n")
	else:
	    out_for_each.writelines("x\n")
        f_1.close()
        f_2.close()
    print("Sum count 1: ",sum_count1)
    print("Sum count 2: ", sum_count2)
    out_file.writelines("Sum count 1: %d\n" % sum_count1)
    out_file.writelines("Sum count 2: %d\n" % sum_count2)
    out_for_each.close()


rell_test("hssp4x","lg4x","hssp",fp_hssp4x,fp_lg4x)
rell_test("hssp4m","lg4m","hssp",fp_hssp4m,fp_lg4m)
rell_test("hssp4x","lg","hssp",fp_hssp4x,fp_lg)
rell_test("hssp4m","lg","hssp",fp_hssp4m,fp_lg)
rell_test("hssp4x","lgR4","hssp",fp_hssp4x,fp_lgR4)
rell_test("hssp4m","lgG4","hssp",fp_hssp4m,fp_lgG4)
rell_test("hssp4x","pfam","hssp",fp_hssp4x,fp_pfam)
rell_test("hssp4m","pfam","hssp",fp_hssp4m,fp_pfam)
rell_test("hssp4x","c20","hssp",fp_hssp4x,fp_c20)
rell_test("hssp4m","c20","hssp",fp_hssp4m,fp_c20)
rell_test("hssp4x","c60","hssp",fp_hssp4x,fp_c60)
rell_test("hssp4m","c60","hssp",fp_hssp4m,fp_c60)
rell_test("hssp4x","ul3","hssp",fp_hssp4x,fp_ul3)
rell_test("hssp4m","ul3","hssp",fp_hssp4m,fp_ul3)
rell_test("hssp4x","exeho","hssp",fp_hssp4x,fp_exeho)
rell_test("hssp4m","exeho","hssp",fp_hssp4m,fp_exeho)
rell_test("hssp4x","cf4","hssp",fp_hssp4x,fp_cf4)
rell_test("hssp4m","cf4","hssp",fp_hssp4m,fp_cf4)
rell_test("lg4x","ul3","hssp",fp_lg4x,fp_ul3)
rell_test("lg4m","ul3","hssp",fp_lg4m,fp_ul3)
rell_test("lg4x","exeho","hssp",fp_lg4x,fp_exeho)
rell_test("lg4m","exeho","hssp",fp_lg4m,fp_exeho)
rell_test("lg4x","cf4","hssp",fp_lg4x,fp_cf4)
rell_test("lg4m","cf4","hssp",fp_lg4m,fp_cf4)

rell_test("hssp4x","lg4x","tb",fp_hssp4x,fp_lg4x)
rell_test("hssp4m","lg4m","tb",fp_hssp4m,fp_lg4m)
rell_test("hssp4x","lg","tb",fp_hssp4x,fp_lg)
rell_test("hssp4m","lg","tb",fp_hssp4m,fp_lg)
rell_test("hssp4x","lgR4","tb",fp_hssp4x,fp_lgR4)
rell_test("hssp4m","lgG4","tb",fp_hssp4m,fp_lgG4)
rell_test("hssp4x","pfam","tb",fp_hssp4x,fp_pfam)
rell_test("hssp4m","pfam","tb",fp_hssp4m,fp_pfam)
rell_test("hssp4x","c20","tb",fp_hssp4x,fp_c20)
rell_test("hssp4m","c20","tb",fp_hssp4m,fp_c20)
rell_test("hssp4x","c60","tb",fp_hssp4x,fp_c60)
rell_test("hssp4m","c60","tb",fp_hssp4m,fp_c60)
rell_test("hssp4x","ul3","tb",fp_hssp4x,fp_ul3)
rell_test("hssp4m","ul3","tb",fp_hssp4m,fp_ul3)
rell_test("hssp4x","exeho","tb",fp_hssp4x,fp_exeho)
rell_test("hssp4m","exeho","tb",fp_hssp4m,fp_exeho)
rell_test("hssp4x","cf4","tb",fp_hssp4x,fp_cf4)
rell_test("hssp4m","cf4","tb",fp_hssp4m,fp_cf4)
rell_test("lg4x","ul3","tb",fp_lg4x,fp_ul3)
rell_test("lg4m","ul3","tb",fp_lg4m,fp_ul3)
rell_test("lg4x","exeho","tb",fp_lg4x,fp_exeho)
rell_test("lg4m","exeho","tb",fp_lg4m,fp_exeho)
rell_test("lg4x","cf4","tb",fp_lg4x,fp_cf4)
rell_test("lg4m","cf4","tb",fp_lg4m,fp_cf4)
rell_test("lg4x","lg","hssp",fp_lg4x,fp_lg)
rell_test("lg4m","lg","hssp",fp_lg4x,fp_lg)
rell_test("pfam","lg","hssp",fp_pfam,fp_lg)
rell_test("c20","lg","hssp",fp_c20,fp_lg)
rell_test("c60","lg","hssp",fp_c60,fp_lg)
rell_test("ul3","lg","hssp",fp_ul3,fp_lg)
rell_test("cf4","lg","hssp",fp_cf4,fp_lg)
rell_test("exeho","lg","hssp",fp_exeho,fp_lg)
rell_test("lg4m","lgG4","hssp",fp_lg4m,fp_lgG4)
rell_test("lg4m","lgG4","tb",fp_lg4m,fp_lgG4)

out_file.close()
