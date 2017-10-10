main
	xor	r1,r1,r1
	ldi	r2,1
	ldi	r4,21	
fib_loop
	ldw	sr,writei
	stw	r1,sr
	ldw	sr,writec
	ldi	r3,32
	stw	r3,sr
	
	add	r3,r1,r2
	and	r1,r2,r2
	and	r2,r3,r3
	
	sub	r4,1
	bnz	r4,fib_loop
	hcf

writec	0xf000
writei	0xf002
