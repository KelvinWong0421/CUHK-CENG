profit = int(input("Enter the profit (HKD): "))
if profit <= 1000000:
    bonus = profit * 0.1
else: 
    bonus = (1000000 * 0.1) + (profit-1000000)*0.05

print("The bonus amount (HKD):",int(bonus))