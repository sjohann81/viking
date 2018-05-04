#!/usr/bin/python

import sys, string

codes = {
	"and":0x0000, "or":0x1000, "xor":0x2000, "slt":0x3000,
	"sltu":0x4000, "add":0x5000, "sub":0x6000, "ldr":0x8000,
	"ldc":0x9000, "lsr":0x0001, "asr": 0x1001,
	"ldb":0x0002, "stb":0x1002, "ldw":0x4002, "stw":0x5002,
	"bez":0xa000, "bnz":0xb000,
	"ldc0":0x9000, "ldc1":0x9000, "hcf":0x0003				# special ops
}

lookup = {
	"r0":0, "r1":1, "r2":2, "r3":3,
	"r4":4, "r5":5, "r6":6, "r7":7,
	"at":0, "sr":5, "lr":6, "sp":7
}

def is_number(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def tohex(n):
	return "%s" % ("0000%x" % (n & 0xffff))[-4:]

def getval(s) :
	"return numeric value of a symbol or number"
	if not s : return 0							# empty symbol - zero
	a = lookup.get(s)							# get value or None if not in lookup
	if a == None : return int(s, 0)						# just a number (prefix can be 0x.. 0o.. 0b..)
	else : return a

def pass1(program) :
	"process pseudo operations"
	i = 0
	for lin in program :
		flds = string.split(lin)
		if flds :
			if flds[0] == ";" :
				program[i] = '\n'
			if flds[0] == "nop" :
				program[i] = "\tand	r0,r0,r0\n"
			if flds[0] == "hcf" :
				program[i] = "\thcf	r0,r0,r0\n"
			if len(flds) > 1 :
				parts  = string.split(flds[1],",")
				if flds[0] == "not" :
					program[i] = "\txor	" + parts[0] + ",-1\n"
				if flds[0] == "neg" :
					program[i] = "\txor	" + parts[0] + ",-1\n"
					program.insert(i+1, "\tadd	" + parts[0] + ",1\n")
				if flds[0] == "mov" :
					program[i] = "\tand	" + parts[0] + "," + parts[1] + "," + parts[1] + "\n"
				if flds[0] == "lsr" :
					program[i] = "\tlsr	" + parts[0] + "," + parts[1] + "," + "r0\n"
				if flds[0] == "asr" :
					program[i] = "\tasr	" + parts[0] + "," + parts[1] + "," + "r0\n"
				if flds[0] == "lsl" :
					program[i] = "\tadd	" + parts[0] + "," + parts[1] + "," + parts[1] + "\n"
				if flds[0] == "ldi" :
					if is_number(parts[1]) :
						if ((int(parts[1]) < 256) and (int(parts[1]) >= -128)) :
							program[i] = "\tldr	" + flds[1] + "\n"
						else :
							program[i] = "\tldr	" + parts[0] + "," + str((int(parts[1]) >> 8) & 0xff) + "\n"
							program.insert(i+1, "\tldc	" + parts[0] + "," + str(int(parts[1]) & 0xff) + "\n")
					else :
						program[i] = "\tldc0	" + flds[1] + "\n"
						program.insert(i+1, "\tldc1	" + flds[1] + "\n")
				if flds[0] == "ldb" and len(parts) == 2 :
					if lookup.get(parts[1]) == None :
						program[i] = "\tldc0	at," + parts[1] + "\n"
						program.insert(i+1, "\tldc1	at," + parts[1] + "\n")
						program.insert(i+2, "\tldb	" + parts[0] + ",r0,at\n")
					else :
						program[i] = "\tldb	" + parts[0] + ",r0," + parts[1] + "\n"
				if flds[0] == "stb" and len(parts) == 2 :
					if lookup.get(parts[1]) == None :
						program[i] = "\tldc0	at," + parts[1] + "\n"
						program.insert(i+1, "\tldc1	at," + parts[1] + "\n")
						program.insert(i+2, "\tstb	r0," + parts[0] + ",at\n")
					else :
						program[i] = "\tstb	r0," + parts[0] + "," + parts[1] + "\n"
				if flds[0] == "ldw" and len(parts) == 2 :
					if lookup.get(parts[1]) == None :
						program[i] = "\tldc0	at," + parts[1] + "\n"
						program.insert(i+1, "\tldc1	at," + parts[1] + "\n");
						program.insert(i+2, "\tldw	" + parts[0] + ",r0,at\n")
					else :
						program[i] = "\tldw	" + parts[0] + ",r0," + parts[1] + "\n"
				if flds[0] == "stw" and len(parts) == 2 :
					if lookup.get(parts[1]) == None :
						program[i] = "\tldc0	at," + parts[1] + "\n"
						program.insert(i+1, "\tldc1	at," + parts[1] + "\n");
						program.insert(i+2, "\tstw	r0," + parts[0] + ",at\n")
					else :
						program[i] = "\tstw	r0," + parts[0] + "," + parts[1] + "\n"
				if flds[0] == "bez" and len(parts) == 2 :
					if lookup.get(parts[1]) == None :
						if is_number(parts[1]) == False :
							program[i] = "\tldc0	at," + parts[1] + "\n"
							program.insert(i+1, "\tldc1	at," + parts[1] + "\n")
							program.insert(i+2, "\tbez	r0," + parts[0] + ",at\n")
					else :
						program[i] = "\tbez	r0," + parts[0] + "," + parts[1] + "\n"
				if flds[0] == "bnz" and len(parts) == 2 :
					if lookup.get(parts[1]) == None :
						if is_number(parts[1]) == False :
							program[i] = "\tldc0	at," + parts[1] + "\n"
							program.insert(i+1, "\tldc1	at," + parts[1] + "\n")
							program.insert(i+2, "\tbnz	r0," + parts[0] + ",at\n")
					else :
						program[i] = "\tbnz	r0," + parts[0] + "," + parts[1] + "\n"
				if flds[0] == "lsrm" and len(parts) == 2 and is_number(parts[1]) == False :
					program[i] = "\tlsr	" + parts[0] + "," + parts[0] + ",r0\n"
					program.insert(i+1, "\tsub	" + parts[1] + ",1\n")
					program.insert(i+2, "\tbnz	" + parts[1] + ",-6\n")
				if flds[0] == "asrm" and len(parts) == 2 and is_number(parts[1]) == False :
					program[i] = "\tasr	" + parts[0] + "," + parts[0] + ",r0\n"
					program.insert(i+1, "\tsub	" + parts[1] + ",1\n")
					program.insert(i+2, "\tbnz	" + parts[1] + ",-6\n")
				if flds[0] == "lslm" and len(parts) == 2 and is_number(parts[1]) == False :
					program[i] = "\tadd	" + parts[0] + "," + parts[0] + "," + + parts[0] + "\n"
					program.insert(i+1, "\tsub	" + parts[1] + ",1\n")
					program.insert(i+2, "\tbnz	" + parts[1] + ",-6\n")
		i += 1

def pass2(program) :
	"determine addresses for labels and add to the lookup dictionary"
	global lookup
	pc = 0
	for lin in program :
		flds = string.split(lin)
		if not flds : continue						# just an empty line
		if lin[0] > ' ' :
			symb = flds[0]						# a symbol - save its address in lookup
			lookup[symb] = pc
			flds2 = ' '.join(flds[1:])
			if flds2 :
				if flds2[0] == '"' and flds2[-1] == '"' :
					flds2 = lin
					flds2 = flds2[1:-1]
					flds2 = flds2.replace("\\t", chr(0x09))
					flds2 = flds2.replace("\\n", chr(0x0a))
					flds2 = flds2.replace("\\r", chr(0x0d))
					while (flds2[0] != '"') :
						flds2 = flds2[1:]
					flds2 = flds2[1:-1] + '\0'
					while (len(flds2) % 2) != 0 :
						flds2 = flds2 + '\0'
					pc = pc + len(flds2)
				else:
					flds = flds[1:]
					for f in flds :
						pc = pc + 2
		else :
			pc = pc + 2

def assemble(flds) :
	"assemble instruction to machine code"
	opval = codes.get(flds[0])
	symb = lookup.get(flds[0])
	if symb != None :
		return symb
	else :
		if opval == None : return int(flds[0], 0)			# just a number (prefix can be 0x.. 0o.. 0b..)
		parts  = string.split(flds[1],",")				# break opcode fields
		if len(parts) == 2 :
			parts = [0,parts[0],parts[1]]
			if (flds[0] == "ldc0") :				# ldc0 .. ldc1 are special steps of ldc
				return (opval | 0x0800 | (getval(parts[1]) << 8) | ((getval(parts[2]) >> 8) & 0xff))
			else :
				return (opval | 0x0800 | (getval(parts[1]) << 8) | (getval(parts[2]) & 0xff))
		if len(parts) == 3 :
			parts = [0,parts[0],parts[1],parts[2]]
			return (opval | (getval(parts[1]) << 8) | (getval(parts[2]) << 5) | (getval(parts[3]) << 2))

def pass3(program) :
	"translate assembly code and symbols to machine code"
	args = sys.argv[1:]
	if args :
		args = args[0]
	else :
		args = ''

	pc = 0

	if args == "debug" :
		for lin in program :
			flds = string.split(lin)
			if lin[0] > ' ' : flds = flds[1:]			# drop symbol if there is one
			if not flds : print (lin),				# print now if only a symbol
			else :
				try :
					flds2 = ' '.join(flds)
					if flds2[0] == '"' and flds2[-1] == '"' :
						flds2 = lin
						flds2 = flds2[1:-1]
						flds2 = flds2.replace("\\t", chr(0x09))
						flds2 = flds2.replace("\\n", chr(0x0a))
						flds2 = flds2.replace("\\r", chr(0x0d))
						while (flds2[0] != '"') :
							flds2 = flds2[1:]
						flds2 = flds2[1:] + '\0'
						while (len(flds2) % 2) != 0 :
							flds2 = flds2 + '\0'
						flds3 = ''
						while True :
							flds3 += (str((int(ord(flds2[0])) << 8) | int(ord(flds2[1])))) + ' '
							flds2 = flds2[2:]
							if flds2 == '' : break
						flds3 = string.split(flds3)
						instruction = assemble(flds3)
						print ("%04x %s    %s" % (pc, tohex(instruction), lin)),
						pc = pc + 2
						flds3 = flds3[1:]
						for f in flds3 :
							instruction = assemble(flds3)
							print ("%04x %s" % (pc, tohex(instruction)))
							pc = pc + 2
							flds3 = flds3[1:]
						flds = ''
					else :
						if codes.get(flds[0]) == None :
							data = assemble(flds)
							print ("%04x %s %s" % (pc, tohex(data), lin)),
							pc = pc + 2
							flds = flds[1:]
							for f in flds :
								data = assemble(flds)
								print ("%04x %s" % (pc, tohex(data)))
								pc = pc + 2
								flds = flds[1:]
						else :
							instruction = assemble(flds)
							print ("%04x %s    %s" % (pc, tohex(instruction), lin)),
							pc = pc + 2
				except :
					print ("**** ????    %s" % lin),
	else :
		for lin in program :
			flds = string.split(lin)
			if lin[0] > ' ' : flds = flds[1:]			# drop symbol if there is one
			if not flds : continue
			try :
				flds2 = ' '.join(flds)
				if flds2[0] == '"' and flds2[-1] == '"' :
					flds2 = lin
					flds2 = flds2[1:-1]
					flds2 = flds2.replace("\\t", chr(0x09))
					flds2 = flds2.replace("\\n", chr(0x0a))
					flds2 = flds2.replace("\\r", chr(0x0d))
					while (flds2[0] != '"') :
						flds2 = flds2[1:]
					flds2 = flds2[1:-1] + '\0'
					while (len(flds2) % 2) != 0 :
						flds2 = flds2 + '\0'
					flds3 = ''
					while True :
						flds3 += (str((int(ord(flds2[0])) << 8) | int(ord(flds2[1])))) + ' '
						flds2 = flds2[2:]
						if flds2 == '' : break
					flds3 = string.split(flds3)
					instruction = assemble(flds3)
					print ("%04x %s" % (pc, tohex(instruction)))
					pc = pc + 2
					flds3 = flds3[1:]
					for f in flds3 :
						instruction = assemble(flds3)
						print ("%04x %s" % (pc, tohex(instruction)))
						pc = pc + 2
						flds3 = flds3[1:]
					flds = ''
				else :
					if codes.get(flds[0]) == None :
						data = assemble(flds)
						print ("%04x %s" % (pc, tohex(data)))
						pc = pc + 2
						flds = flds[1:]
						for f in flds :
							data = assemble(flds)
							print ("%04x %s" % (pc, tohex(data)))
							pc = pc + 2
							flds = flds[1:]
					else :
						instruction = assemble(flds)
						print ("%04x %s" % (pc, tohex(instruction)))
						pc = pc + 2
			except :
				print ("**** ????    %s" % lin),

def main() :
	program = sys.stdin.readlines()
	pass1(program)
	pass2(program)
	pass3(program)

if __name__ == "__main__" : main()
