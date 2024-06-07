

exchange_rate={"USD": 0.13, "EUR": 0.11, "CNY":0.81, "GBP":0.095}

curreny = input("Enter a currency: ")
amount = float(input("Enter the amount: "))

v=0

for x in exchange_rate:
    if curreny == x:
        camount = amount/exchange_rate[x]
        print("Converted amount: HKD","%.2f" % camount)
        v=1;
        break
    
if v==0:
    print("Unknown currency!")




   
    

