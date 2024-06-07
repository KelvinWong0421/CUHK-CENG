def is_astonishing(x):
    a = str(x)
    for i in range(1,len(str(x))):
        b = a[:i]
        c = a[i:]

        sum = 0
        #print(int(b),int(c))
        
        if int(b) > int(c):
            for j in range(int(c), int(b)+1):
                sum += j
            if sum == x:
                return True, int(c), int(b)
        else:
            for j in range(int(b), int(c)+1):
                sum += j
            if sum == x:
                return True, int(b), int(c)
                

    return False, 0, 0 
        
        




x = int(input("Enter an integer: "))
y = is_astonishing(x)
if y[0]:
    print(str(x)+" is astonishing "+str(x)+" = sum from ("+str(y[1])+" to "+str(y[2]) +").")
else:
    print(str(x)+" is not astonishing.")

