import glob
def merge_lh(folder1, folder2, out):
    print("Process %s and %s"%(folder1,folder2))
    for f in glob.glob(r"%s/*.sitelh"%folder1):
        name = f.split('/')[1]
        out_name = "%s/%s"%(out,name)
        f_out = open("%s"%out_name,'w')
        fin1 = open(f,'r')
        fin2 = open("%s/%s"%(folder2,name),'r')
        line1 = fin1.readline()
	sites = line1.split()[1]
        f_out.writelines("2 %s\n"%sites)
	line2 = fin1.readline()
	f_out.writelines("%s"%line2)
        fin2.readline()
        line2 = fin2.readline()
        f_out.writelines("%s"%line2)
        f_out.close()
        fin1.close()
        fin2.close()
merge_lh("hssp4m","lg4m","hssp4m_lg4m")
merge_lh("hssp4m","lgG4","hssp4m_lgG4")
merge_lh("hssp4m","pfam","hssp4m_pfam")
merge_lh("hssp4m","c20","hssp4m_c20")
merge_lh("hssp4m","c60","hssp4m_c60")

