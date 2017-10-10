main
	ldi r1,str1
	sub sp,2
	stw r1,sp
	sub sp,2
	stw lr,sp
	ldi lr,ret_print1
	ldi sr,print_str
	bnz r7,sr
ret_print1
	ldw lr,sp
	add sp,4
	
	ldi r1,str2
	sub sp,2
	stw r1,sp
	sub sp,2
	stw lr,sp
	ldi lr,ret_print2
	ldi sr,print_str
	bnz r7,sr
ret_print2
	ldw lr,sp
	add sp,4
	
	hcf

print_str
	ldw sr,writec
	sub sp,2
	stw r1,sp
	sub sp,2
	stw r2,sp

	and r1,sp,sp
	add r1,6
	ldw r1,r1
print_loop
	ldb r2,r1
	stw r2,sr
	add r1,1
	bnz r2,-8
	
	ldw r2,sp
	add sp,2
	ldw r1,sp
	add sp,2
	bnz r7,lr


writec	0xf000
str1	"this is the first call\n"
str2	"and this is the second!\n"
