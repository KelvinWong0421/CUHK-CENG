def pie_chart(d):
    sum=0
    for i in list(d.values()):
        sum = sum+int(i)
    length=360/sum
    
    for i in range(len(d)):
        if(list(d.values())[i]*length)%1==0 :   #Round final values to the nearest tenth 
            x = None
        else :
            x =1

        d[list(d.keys())[i]]=round(list(d.values())[i]*length, x)
    
    return d
    

print(pie_chart({"a":1, "b":2 }))
print(pie_chart({ "a":30, "b":15, "c":55 }))
print(pie_chart({ "a":8, "b":21, "c":12, "d":5, "e":4 }))


