ls=[]

try:
    with open("scores.txt") as f:
        f1 = f.readlines()
        sum = 0
        sum2 = 0
        for i in range(len(f1)):
            f1[i]=int(f1[i][7:])
            sum += f1[i]
        mean = round(float(sum/len(f1)),2)

        for j in range(len(f1)):
            sum2 += (f1[j]-mean)**2
        var = round(float(sum2/len(f1)),2) 
        print("Mean:",mean)
        print("Variance:",var)
        

except IOError as e:
    print("Unable to access file")
