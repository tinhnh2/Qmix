import sys
def normalize(input_file):
    in_file = open(input_file, 'r')
    out_file = open("%s.normalized"%input_file,'w')
    R = [[0.0] * 20] * 20
    Q = [[0.0] * 20] * 20
    Pi = [0.0] * 20
    for i in range (1,20):
        line = in_file.readline()
        line = line.split()
        A = [0.0] * 20
        for j in range(0,i):
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
                out_file.writelines("%f "%R[i][j])
        if i > 0:
            out_file.writelines("\n")

    for i in range(20):
        out_file.writelines("%f "%Pi[i])
    in_file.close()
    out_file.close()

if __name__ == '__main__':
    input_file = sys.argv[1]
    normalize(input_file)
