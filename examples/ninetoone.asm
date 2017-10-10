main
	ldi	r1,9
	ldi	r2,32
loop
	ldw	sr,writei
	stw	r1,sr
	ldw	sr,writec
	stw	r2,sr
	sub	r1,1
	bnz	r1,loop
	hcf
	
writec	0xf000
writei	0xf002
