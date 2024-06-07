.globl _start

.data
var1: .byte 15
var2: .byte 19
msg: .asciz "\n"


.text
_start:

li a7,1
la a0, var1			#address var1
ecall

li a7,4
la a0, msg	
ecall

li a7,1
la a0, var2			#address var2
ecall

li a7,4
la a0, msg
ecall

la a1,var1
la a2,var2
lb t0,var1
lb t1,var2

addi t0,t0,1
slli t1,t1,2

sb t0, (a1)
sb t1, (a2)

li a7,1
lb a0, var1			#var1
ecall

li a7,4
la a0, msg
ecall

li a7,1
lb a0, var2			#var2
ecall

li a7,4
la a0, msg
ecall

sb t0, (a2)
sb t1, (a1)

li a7,1
lb a0, var1
ecall

li a7,4
la a0, msg
ecall

li a7,1
lb a0, var2
ecall

li a7,4
la a0, msg
ecall



