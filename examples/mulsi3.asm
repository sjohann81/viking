mulsi3
	sub	sp,2
	stw	r1,sp
	sub	sp,2
	stw	r2,sp
	sub	sp,2
	stw	r3,sp
	
	and	r3,sp,sp
	add	r3,10
	ldw	r2,r3
	sub	r3,2
	ldw	r3,r3
	
	xor	r1,r1,r1
	bez	r3,14
	and	sr,r3,r3
	and	sr,1
	bez	sr,2
	add	r1,r1,r2
	lsl	r2,r2
	lsr	r3,r3
	bnz	r7,-16

	and	sr,r1,r1
	add	sp,2
	ldw	r3,sp
	add	sp,2
	ldw	r2,sp
	add	sp,2
	ldw	r1,sp
	
	bnz	r7,lr
