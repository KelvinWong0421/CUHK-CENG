try:
    with open("scores.txt") as f:

        f1 = f.readlines()              #read file scores.txt in to list
        fp = []             
        for i in range(len(f1)):        #extract the scores only
            fp.append( int(f1[i][7:]))  

        table = sorted(fp, reverse = True)   
        rank =[ ]

        for score in fp:
            rank.append(fp.index(score) + 1)   #create a table to rank relationship
        
        #print(table)
        #print(rank)
        
        for i in range(len(f1)):
            f1[i] = f1[i].strip()       #delete \n
        
        
        w = open("ranks.txt", "w")      #create file
        for i in range(len(f1)):
            w.write(str(f1[i])+" "+str(rank[table.index(fp[i])])+"\n") #output 
        w.close


        #print(f1)


except IOError as e:
    print("Unable to access file")