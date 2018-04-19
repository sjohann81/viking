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
	ldw	r1,i
loop_i
	ldw	r3,N
	sub	r3,1
	slt	r3,r1,r3
	bez	r3,end_i

	xor	r0,r0,r0
	add	r2,r1,r0
	add	r2,1
	stw	r2,j
loop_j
	ldw	r1,i
	ldw	r3,N
	slt	r3,r2,r3
	bez	r3,end_j

	ldi	r4,numbers
	add	r3,r4,r1
	add	r3,r3,r1
	ldw	r1,r3
	add	r4,r4,r2
	add	r4,r4,r2
	ldw	r2,r4

	slt	r1,r2,r1
	bez	r1,skip

	ldw	r1,r3
	stw	r1,r4
	stw	r2,r3
skip
	ldw	r2,j
	add	r2,1
	stw	r2,j
	bnz	r7,loop_j
end_j
	ldw	r1,i
	add	r1,1
	stw	r1,i
	bnz	r7,loop_i
end_i
	bnz	r7,lr

i	0
j	0
N	10
numbers	-5 8 -22 123 77 -1 99 -33 10 12

