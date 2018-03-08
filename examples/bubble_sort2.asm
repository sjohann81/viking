main
	ldi	lr,ret_print1
	bnz	r7,print_numbers
ret_print1
	ldi	lr,ret_sort
	bnz	r7,sort
ret_sort
	ldi	lr,ret_print2
	bnz	r7,print_numbers
ret_print2
	hcf

print_numbers
	ldi	r1,0
	ldw	r2,N
	ldi	r3,numbers
loop_print
	ldw	r4,r3
	stw	r4,0xf002
	ldi	r4,32
	stw	r4,0xf000
	add	r1,1
	add	r3,2
	sub	r5,r1,r2
	bnz	r5,loop_print
	ldi	r4,10
	stw	r4,0xf000
	bnz	r7,lr

sort
	bnz	r7,lr

i	0
j	0
N	10
numbers	-5 8 -22 123 77 -1 99 -33 10 12

