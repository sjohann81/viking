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
	ldi	r1,0
loop_i
	ldw	r3,N
	sub	r3,1
	slt	r3,r1,r3
	bez	r3,end_i

	xor	r0,r0,r0
	add	r2,r1,r0
	add	r2,1
loop_j
	ldw	r3,N
	slt	r3,r2,r3
	bez	r3,end_j

	ldi	r5,numbers
	add	r3,r5,r1
	add	r3,r3,r1
	ldw	r3,r3
	add	r4,r5,r2
	add	r4,r4,r2
	ldw	r4,r4

	slt	r5,r4,r3
	bez	r5,skip

	xor	r0,r0,r0
	add	r0,r3,r0

	ldi	r5,numbers
	add	r3,r5,r1
	add	r3,r3,r1
	stw	r4,r3

	add	r4,r5,r2
	add	r4,r4,r2
	stw	r0,r4
skip
	add	r2,1
	bnz	r7,loop_j
end_j
	add	r1,1
	bnz	r7,loop_i
end_i

	bnz	r7,lr

N	10
numbers	-5 8 -22 123 77 -1 99 -33 10 12

