
.globl _start

.data
array1: .word -1 22 8 35 5 4 11 2 1 78

.text
_start:

	#input args
	la a0, array1
	li a1, 0	#lo 
	li a2, 9	#hi
	jal ra, quicksort
	j realend
	
quicksort:
	addi sp, sp , -4
	sw ra, 0(sp)
	
	jal ra, checkIsLessThan
	
	lw ra, 0(sp)	#target jump location
	addi sp, sp, 4
	jalr zero, 0(ra) 

checkIsLessThan:
	bge a1, a2, Back	# hi greater or equal to lo
	
	#sore original ra
	addi sp, sp, -4
	sw ra, 0(sp)
	
# partition

	jal ra, partition
	#p-1 && store hi
	addi sp, sp, -4
	
	addi t0, s0, -1 # t0 = p-1
	sw a2, 0(sp)	#store original hi
	
	add a2, t0, zero	#turn hi into p-1
	jal ra, quicksort
	lw a2, 0(sp)		#set back orignal hi
	
	addi t0, s0, 1		# t0 = p+1 
	sw a1, 0(sp)		#store original  lo
	
	add a1, t0, zero	#turn lo into p+1
	jal ra, quicksort
	lw a1, 0(sp)
	addi sp, sp, 4
	
	lw ra, 0(sp)
	addi sp, sp, 4
	jalr zero, 0(ra)
	
Back:
	jalr zero, 0(ra)
	
partition:
	addi sp, sp, -4
	sw ra, 0(sp)
	
	addi sp, sp, -16
	add a3, a1, zero	#lo / j
	add a4, a2, zero	#hi
	
	# privot information
	slli t0, a4, 2
	add t0, t0, a0
	sw t0, 0(sp)	#address of privot
	lw t0, 0(t0)
	sw t0, 4(sp)	#value of privot
	
	addi t0, a3, -1	#t0 = i
	sw t0, 8(sp)	#value of i
	
	#jump to loop
	j loop
	
#loop
loop:
	bge a3, a4, end
	
	slli t0, a3, 2  #A[j]
	add t0, t0, a0
	sw t0, 12(sp)	#address of A[j]
	
	#condition
	jal ra, check

	addi a3, a3, 1
	j loop
#loop

#check
check:
	lw t0, 0(t0)	#A[j] value
	lw t1, 4(sp)	#prvot
	
	ble  t0, t1, swap
	
	jalr zero, 0(ra)
#

#condition_effect
swap:
	#i=i+1
	lw t2, 8(sp)
	addi t2, t2, 1
	sw t2, 8(sp)
	
	
	#A[1] swap A[j]
	slli t2, t2, 2	#i
	add t2, t2, a0
	lw t3, 0(t2)	#value of A[i]
	sw t0, 0(t2)	#store value 
	
	lw t4, 12(sp) #address of A[j]
	sw t3, 0(t4)
	
	jalr zero, 0(ra)
#

#end partition
end:
	
	lw t0, 8(sp)	#A[i+1]
	addi t0,t0 ,1
	slli t0, t0, 2
	add t3, t0, a0	#address A[i+1]
	
	lw t0, 0(t3)
		
	slli t1, a2, 2	#address A[j]
	add t4, t1, a0
	lw t1, 0(t4)
	
	sw t0, 0(t4)
	sw t1, 0(t3)
	
	
	#return
	lw s0, 8(sp)
	addi s0, s0, 1
	
	#stack pointer
	addi sp, sp, 16
	
	lw ra, 0(sp)
	addi sp, sp, 4
	jalr zero, 0(ra)
#
realend:


