print("Please enter name and bid price for")

x = input("Bidder 1:").split()

winner = x
y=2
while x != 'END':
    x=input("Bidder "+str(y)+":").split()
    y=y+1
    if x[0] == 'END':
        break
    elif int(x[1]) > int(winner[1]):
        winner = x 

print("The fine watch is sold to "+winner[0]+" at"+" $"+winner[1])




