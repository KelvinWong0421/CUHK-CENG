h = int(input("Enter h: "))

while h<=0 or h>30:
    h = int(input("Enter h: "))




for k in range(0, h):

    for i in range(k, h-1):
            print(end=" ")
    
    print("/", end="")

    for i in range(k):
            if k == h-1:
               print("__",end="") 
            else:
                print(end="  ")
        


    print("\\")
    
    




    