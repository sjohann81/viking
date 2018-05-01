main

	ldi 	r2,ask
	ldi	lr,retask
	bnz	sp,print
retask
	ldi	r2,name
	ldi	lr,retget
	bnz	sp,getname
retget
	ldi	r2,str

	ldi 	r2,str
	ldi	lr,retstr
	bnz	sp,print
retstr
	ldi 	r2,name
	ldi	lr,retstr2
	bnz	sp,print
retstr2
	hcf

print
	ldb	r3,r2
	stw	r3,0xf000
	add	r2,1
	bnz	r3,print
	bnz	sp,lr

getname
	ldw	r3,0xf004
	stb	r3,r2
	add	r2,1
	bnz	r3,getname
	bnz	sp,lr

str	"\nhello "
ask	"enter your name: "
name	"                 "


