while True:
    try:
        b = float(input("Enter the bill amount: ")) 
        if b < 0 :
            raise ValueError
        else:
            while True:
                try:
                    n = int(input("Enter number of people: "))
                    if n < 0:
                        raise ValueError
                    p ="{:.2f}".format(b/n,3)
                    print("Everyone should pay $",p)
                    break
                
                except ValueError:
                    print("Retry with a positive integer for no. of people!")
                except ZeroDivisionError:
                    print("Division by zero error!")   
            
            break
    except ValueError as e:
        print("Retry with a non-negative value for the bill!")    

