main
	ldw	r2,readi
	ldw	r2,r2
	ldw	r3,readi
	ldw	r3,r3

	sub	sp,2
	stw	r2,sp
	sub	sp,2
	stw	r3,sp
	sub	sp,2
	stw	lr,sp
	ldi	lr,ret_addr
	ldi	sr,mulsi3
	bnz	r7,sr
ret_addr
	ldw	lr,sp
	add	sp,6
	
	and	r1,sr,sr
	ldw	sr,writei
	stw	r1,sr
	hcf
	
writei	0xf002
readi	0xf006
