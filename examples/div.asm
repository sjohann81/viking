main
	ldw	r2,readi
	ldw	r2,r0,r2
	ldw	r3,readi
	ldw	r3,r0,r3

	sub	sp,2
	stw	r0,r2,sp
	sub	sp,2
	stw	r0,r3,sp
	sub	sp,2
	stw	r0,lr,sp
	ldi	lr,ret_addr
	ldi	sr,divsi3
	bnz	r0,r7,sr
ret_addr
	ldw	lr,r0,sp
	add	sp,6
	
	and	r1,sr,sr
	ldw	sr,writei
	stw	r0,r1,sr
	hcf
	
	
writei	0xf002
readi	0xf006
