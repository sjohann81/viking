udivmodsi4
	sub	sp,2
	stw	r1,sp
	sub	sp,2
	stw	r2,sp
	sub	sp,2
	stw	r3,sp
	sub	sp,2
	stw	r4,sp
	
	ldr	r3,1
	xor	r4,r4,r4
	
	and	r2,sp,sp
	add	r2,14
	ldw	r1,r2
	sub	r2,2
	ldw	r2,r2
	
	sltu	sr,r2,r1
	bez	sr,8
	bez	r3,6
	lsl	r2,r2
	lsl	r3,r3
	bnz	r7,-12
	sltu	sr,r1,r2
	bnz	sr,4
	sub	r1,r1,r2
	add	r4,r4,r3
	lsr	r3,r3
	lsr	r2,r2
	bnz	r3,-14
	
	and	sr,sp,sp
	add	sr,10
	ldw	sr,sr
	bez	sr,4
	and	sr,r1,r1
	bez	sr,2
	and	sr,r4,r4
	
	ldw	r4,sp
	add	sp,2
	ldw	r3,sp
	add	sp,2
	ldw	r2,sp
	add	sp,2
	ldw	r1,sp
	add	sp,2	
	bnz	r7,lr
