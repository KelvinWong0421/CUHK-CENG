
a, b = map(int, input("Enter two integers: ").split())
 

if a > b:
    a, b = b, a 

sum = 0  
for i in range(a,b+1):
    sum += i 

print("Sum from " +str(a)+" to "+str(b)+": "+str(sum))