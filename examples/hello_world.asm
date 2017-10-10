main
	ldw	sr,writec
	ldi	r4,str
	ldi	r3,loop
loop
	ldb	r2,r4
	stw	r2,sr
	add	r4,1
	bnz	r2,r3
	hcf

writec	0xf000
str	"hello world!"
