import numpy as np
import os
import sys
def pearson_corr(model1, model2):
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

def main(m1,m2):
    print("Start process...")
    corr1 = pearson_corr("%s.1"%m1,"%s.1"%m2)
    corr2 = pearson_corr("%s.2"%m1,"%s.2"%m2)
    corr3 = pearson_corr("%s.3"%m1,"%s.3"%m2)
    corr4 = pearson_corr("%s.4"%m1,"%s.4"%m2)
    print("corr1: %f, corr2: %f, corr3: %f, corr4: %f"%(corr1,corr2,corr3,corr4))

# call main function
if __name__ == '__main__':
    m1 = sys.argv[1]
    m2 = sys.argv[2]
    main(m1,m2)
