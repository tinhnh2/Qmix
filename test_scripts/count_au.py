import glob
import sys

folder = sys.argv[1]
au_1 = 0.0
au_2 = 0.0
count_Q = 0
count_Q1 = 0
for f in glob.glob(r"%s/*_250.pv"%folder):
    f1 = open(f,"r")
#    print("File %d, name: %s" % (file_id, f))
    idx = 0
    item = 3
    au = 0.0
    for line in f1:
        idx += 1
        if idx == 4:
            data = list(line.split())
            au = float(data[4])
            item = int(data[2])
#            print("ITEM: %d, AU: %f"%(item,au))
            if au > 0.95:
                if item == 1:
                    count_Q += 1
                else:
                    count_Q1 += 1

    f1.close()
print("HSSP4X/4M COUNT: ", count_Q)
print("LG4X/4M COUNT: ", count_Q1)

