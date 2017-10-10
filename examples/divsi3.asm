divsi3
	sub	sp,2
	stw	r1,sp
	sub	sp,2
	stw	r2,sp
	sub	sp,2
	stw	r3,sp
	
	and	r2,sp,sp
	add	r2,10
	ldw	r1,r2
	sub	r2,2
	ldw	r2,r2
	xor	r3,r3,r3

	xor	at,at,at
	slt	sr,r1,at
	bez	sr,4
	sub	r1,at,r1
	or	r3,1
	slt	sr,r2,at
	bez	sr,4
	sub	r2,at,r2
	xor	r3,1
	
	sub	sp,2
	stw	r1,sp
	sub	sp,2
	stw	r2,sp
	sub	sp,2
	ldr	sr,0
	stw	sr,sp
	sub	sp,2
	stw	lr,sp
	ldi	lr,ret_divsi3
	ldi	sr,udivmodsi4
	bnz	r7,sr
ret_divsi3
	ldw	lr,sp
	add	sp,8
	bez	r3,4
	xor	at,at,at
	sub	sr,at,sr

	add	sp,2
	ldw	r3,sp
	add	sp,2
	ldw	r2,sp
	add	sp,2
	ldw	r1,sp
	
	bnz	r7,lr
