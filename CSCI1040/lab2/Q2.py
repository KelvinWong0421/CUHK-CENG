x = (input("Enter numbers: ").split())

output =[]
for x in x:
    if x.isdigit() == True and x not in output : 
        if int(x)%2 == 1 :
            output.append(x)


print("output:",*output, sep=' ')