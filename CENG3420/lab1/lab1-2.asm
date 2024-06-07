.globl _start

.data
array1: .word -1 22 8 35 5 4 11 2 1 78

.text
_start:

    la a0, array1
    li a1, 0    	#start  lo/j
    li a2, 9    	#end    hi	
    
    
    #swap 8 and 78 > set 8 to be pivot
    lw t0, 8(a0)
    lw t1, 36(a0)
    sw t0, 36(a0)	#t0 = 8
    sw t1, 8(a0)	
    
    addi t1,a1,-1            #i
    li t2,8		#hi-1
    
    j loop
    
loop:
    bgt a1, t2, end	#end conitdtion

    
    slli t6,a1,2
    add  t6,a0,t6
    lw t3, 0(t6)	   #get -1   t6= adress of j
    
    jal ra, check	 
    addi a1,a1,1          #j++
    j loop
    
check:
    ble t3,t0,lessthaneq
    jalr zero, 0(ra)
    
lessthaneq:
    addi t1,t1,1        #i++        
    slli t4,t1,2
    add t4, t4, a0
    
    lw t5, 0(t4)	#a[i]
    sw t3, 0(t4)        #swap value
    sw t5, 0(t6)	
      
    jalr zero, 0(ra)
    
end:
   addi t1,t1,1        #i++        
   slli t4,t1,2
   add t4, t4, a0
   lw t5, 0(t4)	       #a[i+1] 
   sw t0, 0(t4)
   sw t5, 36(a0)
   
  
   
