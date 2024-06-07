


a = int(input("Enter a: "))
b = int(input("Enter b: "))

while a<0 or b<0:
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))

a, b=str(a), str(b)

asum = int(0) 
bsum = int(0)

for x in a:
    asum += int(x)

for x in b:
    bsum += int(x)


print("a X b:",asum*bsum) 

