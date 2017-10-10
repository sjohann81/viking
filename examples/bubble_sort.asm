main
	ldi	sr,array1
	sub	sp,2
	stw	sr,sp
	ldw	sr,array1_sz
	lsl	sr,sr
	sub	sp,2
	stw	sr,sp
	sub	sp,2
	stw	lr,sp
	ldi	lr,ret_sort1
	ldi	sr,sort
	bnz	r7,sr
ret_sort1
	ldw	lr,sp
	add	sp,4
	
	ldi	r1,array1
	ldw	r2,array1_sz
print_array1
	ldw	r3,r1
	ldw	r4,writei
	stw	r3,r4
	ldi	r3,32
	ldw	r4,writec
	stw	r3,r4
	add	r1,2
	sub	r2,1
	bnz	r2,print_array1
	ldi	r3,10
	stw	r3,r4

	ldi	sr,array2
	sub	sp,2
	stw	sr,sp
	ldw	sr,array2_sz
	lsl	sr,sr
	sub	sp,2
	stw	sr,sp
	sub	sp,2
	stw	lr,sp
	ldi	lr,ret_sort2
	ldi	sr,sort
	bnz	r7,sr
ret_sort2
	ldw	lr,sp
	add	sp,4
	
	ldi	r1,array2
	ldw	r2,array2_sz
print_array2
	ldw	r3,r1
	ldw	r4,writei
	stw	r3,r4
	ldi	r3,32
	ldw	r4,writec
	stw	r3,r4
	add	r1,2
	sub	r2,1
	bnz	r2,print_array2	
	ldi	r3,10
	stw	r3,r4

	hcf

sort
	sub	sp,2
	stw	r1,sp
	sub	sp,2
	stw	r2,sp
	sub	sp,2
	stw	r3,sp
	sub	sp,2
	stw	r4,sp
	xor	r1,r1,r1
beg_loop_i
	and	r4,sp,sp
	add	r4,10
	ldw	r4,r4
	sub	r4,2
	slt	r4,r4,r1
	bnz	r4,end_loop_i
	and	r2,r1,r1
	add	r2,2
beg_loop_j
	and	r4,sp,sp
	add	r4,10
	ldw	r4,r4
	sub	r4,2
	slt	r4,r4,r2
	bnz	r4,end_loop_j
	and	sr,sp,sp
	add	sr,12
	ldw	r3,sr
	add	r3,r3,r1
	ldw	r3,r3
	ldw	r4,sr
	add	r4,r4,r2
	ldw	r4,r4
	sub	sp,2
	stw	r3,sp
	slt	r3,r3,r4
	bnz	r3,no_swap
	and	sr,sp,sp
	add	sr,14
	ldw	r3,sr
	add	r3,r3,r1
	stw	r4,r3
	ldw	r4,sr
	add	r4,r4,r2
	ldw	r3,sp
	stw	r3,r4
no_swap
	add	sp,2
	add	r2,2
	bnz	r7,beg_loop_j
end_loop_j
	add	r1,2
	bnz	r7,beg_loop_i
end_loop_i
	ldw	r4,sp
	add	sp,2
	ldw	r3,sp
	add	sp,2
	ldw	r2,sp
	add	sp,2
	ldw	r1,sp
	add	sp,2
	bnz	r7,lr

writec		0xf000
writei		0xf002
array1		-5 3 23 -64 34 3 65 7 10 -4 10
array1_sz	11
array2		13121 6686 12335 6172 -13028 -4379 -3953 16045 -7613 -12561 -7188 -7141 -6281 8039 -12760 -2041	6212 -146 -3087 9151 -14015 7819 6590 -13079 549 13277 9033 -8114 -3338 -5071
array2_sz	30
