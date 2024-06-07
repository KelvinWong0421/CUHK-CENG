def checkerboard(x, y, z):
    m = []
    lst = [y, z]
    rlst = [z, y]
    for i in range(x):
        temp = []
        if i % 2 == 0:
            for j in range(x):
                j = j%2
                temp.append(lst[j])
            m.append(temp)
        else:
            for j in range(x):
                j = j%2
                temp.append(rlst[j])
            m.append(temp)
    return m

def print_board(m):
    for i in m :
        print(" ".join(i))



x, y, z= input().split()
x = int(x)

print_board(checkerboard(x,y,z))
