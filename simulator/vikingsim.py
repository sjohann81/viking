#!/usr/bin/python

import sys, string
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import askopenfilename, asksaveasfilename
from tkSimpleDialog import *

#
# assembler
#
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
						program.insert(i+1, "\tldc1	at," + parts[1] + "\n")
						program.insert(i+2, "\tldw	" + parts[0] + ",r0,at\n")
					else :
						program[i] = "\tldw	" + parts[0] + ",r0," + parts[1] + "\n"
				if flds[0] == "stw" and len(parts) == 2 :
					if lookup.get(parts[1]) == None :
						program[i] = "\tldc0	at," + parts[1] + "\n"
						program.insert(i+1, "\tldc1	at," + parts[1] + "\n")
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
			textsym.insert(END, "%s" % tohex(pc) + ' ' + str(symb))
			flds2 = ' '.join(flds[1:])
			if flds2 :
				if flds2[0] == '"' and flds2[-1] == '"' :
					flds2 = lin
					flds2 = flds2[1:-1]
					flds2 = flds2.replace("\\t", chr(0x09))
					flds2 = flds2.replace("\\n", chr(0x0a))
					flds2 = flds2.replace("\\r", chr(0x0d))
					flds2 = flds2 + ' '
					while (flds2[0] != '"') :
						flds2 = flds2[1:]
					flds2 = flds2[1:-2] + '\0'
					while (len(flds2) % 2) != 0 :
						flds2 = flds2 + ' '
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
	pc = 0
	code = ""

	for lin in program :
		if lin == '' : continue
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
				flds2 = flds2 + '\0'
				while (flds2[0] != '"') :
					flds2 = flds2[1:]
				flds2 = flds2[1:-2] + ' '
				while (len(flds2) % 2) != 0 :
					flds2 = flds2 + '\0'
				flds3 = ''
				while True :
					flds3 += (str((int(ord(flds2[0])) << 8) | int(ord(flds2[1])))) + ' '
					flds2 = flds2[2:]
					if flds2 == '' : break
				flds3 = string.split(flds3)
				instruction = assemble(flds3)
				code += ("%04x %s\n" % (pc, tohex(instruction)))
				pc = pc + 2
				flds3 = flds3[1:]
				for f in flds3 :
					instruction = assemble(flds3)
					code += ("%04x %s\n" % (pc, tohex(instruction)))
					pc = pc + 2
					flds3 = flds3[1:]
				flds = ''
			else :
				if codes.get(flds[0]) == None :
					data = assemble(flds)
					code += ("%04x %s\n" % (pc, tohex(data)))
					pc = pc + 2
					flds = flds[1:]
					for f in flds :
						data = assemble(flds)
						code += ("%04x %s\n" % (pc, tohex(data)))
						pc = pc + 2
						flds = flds[1:]
				else :
					instruction = assemble(flds)
					code += ("%04x %s\n" % (pc, tohex(instruction)))
					pc = pc + 2
		except :
			code += ("???? %s" % lin)
	return code

def check(program) :
	for lin in program :
		flds = string.split(lin)
		if len(flds) != 2 and flds != [] :
			return 1
		for f in flds :
			if f == '****' :
				return 1
	return 0

def load(program) :
	global memory
	codes = {
		0x0000:"and", 0x1000:"or", 0x2000:"xor", 0x3000:"slt",
		0x4000:"sltu", 0x5000:"add", 0x6000:"sub", 0x8000:"ldr",
		0x9000:"ldc", 0x0001:"lsr", 0x1001:"asr",
		0x0002:"ldb", 0x1002:"stb", 0x4002:"ldw", 0x5002:"stw",
		0xa000:"bez", 0xb000:"bnz", 0x0003:"hcf"
	}
	memory = []

	textdump.delete(0, END)
	lines = 0
	# load program into memory
	for lin in program :
		flds = string.split(lin)
		data = int(flds[1], 16)
		memory.append(data)
		if (data & 0x0800) :
			if (data & 0xf000) in codes :
				textdump.insert(END, lin + "   %s r%d,%d" % (codes[data & 0xf000], (data & 0x0700) >> 8, (data & 0x00ff)))
			else :
				textdump.insert(END, lin + "   ???")
		else :
			if (data & 0xf003) in codes :
				textdump.insert(END, lin + "   %s r%d,r%d,r%d" % (codes[data & 0xf003], (data & 0x0700) >> 8, (data & 0x00e0) >> 5, (data & 0x001c) >> 2))
			else :
				textdump.insert(END, lin + "   ???")
		lines += 1
	out.insert(END, " done. Program size: " + str(len(memory) * 2) + " bytes (code + data).\n")
	out.see(END)

	# set the stack limit to the end of program section
	context[9] = (len(memory) * 2) + 2
	# reset breakpoint
	context[10] = context[9]

	# fill the rest of memory with zeroes
	for i in range(lines, 28672) :
		memory.append(0)
	reset()

def loaderror(program) :
	global memory
	codes = {
		0x0000:"and", 0x1000:"or", 0x2000:"xor", 0x3000:"slt",
		0x4000:"sltu", 0x5000:"add", 0x6000:"sub", 0x8000:"ldr",
		0x9000:"ldc", 0x0001:"lsr", 0x1001:"asr",
		0x0002:"ldb", 0x1002:"stb", 0x4002:"ldw", 0x5002:"stw",
		0xa000:"bez", 0xb000:"bnz", 0x0003:"hcf"
	}
	memory = []

	textdump.delete(0, END)
	lines = 0
	# load program into memory
	for lin in program :
		flds = string.split(lin)
		try :
			data = int(flds[1], 16)
			if (data & 0x0800) :
				if (data & 0xf000) in codes :
					textdump.insert(END, lin + "   %s r%d,%d" % (codes[data & 0xf000], (data & 0x0700) >> 8, (data & 0x00ff)))
				else :
					textdump.insert(END, lin + "   ???")
			else :
				if (data & 0xf003) in codes :
					textdump.insert(END, lin + "   %s r%d,r%d,r%d" % (codes[data & 0xf003], (data & 0x0700) >> 8, (data & 0x00e0) >> 5, (data & 0x001c) >> 2))
				else :
					textdump.insert(END, lin + "   ???")
		except :
			textdump.insert(END, lin)
		lines += 1
	out.insert(END, " program has errors.\n")
	out.see(END)
	reset()


def assembler() :
	global lookup
	out.insert(END, "\nAssembling...")
	out.see(END)
	source_program = str(textasm.get('1.0', 'end'))
	textsym.delete(0, END)
	program = source_program.splitlines()

	lookup = {
	"r0":0, "r1":1, "r2":2, "r3":3,
	"r4":4, "r5":5, "r6":6, "r7":7,
	"at":0, "sr":5, "lr":6, "sp":7
	}

	pass1(program)
	pass2(program)
	code = pass3(program).splitlines()

	if (check(code)) :
		loaderror(code)
	else :
		load(code)

#
# simulator and user interface
#
context = [
	0x0000, 0x0000, 0x0000, 0x0000,		# r0 - r3
	0x0000, 0x0000, 0x0000, 0xdffe,		# r4 - r7
	0x0000, 0x0000, 0x0000			# pc, stack limit, breakpoint
]

memory = []
terminput = []

cycles = 0
cycle_delay = 1
RUNNING = -1
STOPPED = -2
machine = STOPPED

reg_names = ['r0 (at) : ', 'r1      : ', 'r2      : ', 'r3      : ', 'r4      : ', 'r5 (sr) : ', 'r6 (lr) : ', 'r7 (sp) : ', '\nPC      : ']

def cycle() :
	global cycles, terminput
	pc = context[8]
	# fetch an instruction from memory
	instruction = memory[pc >> 1]

	# predecode the instruction (extract opcode fields)
	opc = (instruction & 0xf000) >> 12
	imm = (instruction & 0x0800) >> 11
	rst = (instruction & 0x0700) >> 8
	rs1 = (instruction & 0x00e0) >> 5
	rs2 = (instruction & 0x001c) >> 2
	op2 = instruction & 0x0003
	immediate = instruction & 0x00ff

	# it's halt and catch fire, halt the simulator
	if instruction == 0x0003 : return 0

	# decode and execute
	if imm == 0 :
		if context[rs1] > 0x7fff : rs1 = context[rs1] - 0x10000
		else : rs1 = context[rs1]
		if context[rs2] > 0x7fff : rs2 = context[rs2] - 0x10000
		else : rs2 = context[rs2]
	else :
		if context[rst] > 0x7fff : rs1 = context[rst] - 0x10000
		else : rs1 = context[rst]
		if immediate > 0x7f : immediate -= 0x100
		rs2 = immediate

	if ((imm == 0 and (op2 == 0 or op2 == 3)) or imm == 1) :
		if opc == 0 :
					if (imm == 1) : rs2 &= 0xff
					context[rst] = rs1 & rs2
		elif opc == 1 :
					if (imm == 1) : rs2 &= 0xff
					context[rst] = rs1 | rs2
		elif opc == 2 :		context[rst] = rs1 ^ rs2
		elif opc == 3 :
					if rs1 < rs2 : context[rst] = 1
					else : context[rst] = 0
		elif opc == 4 :
					if (rs1 & 0xffff) < (rs2 & 0xffff) : context[rst] = 1
					else : context[rst] = 0
		elif opc == 5 :		context[rst] = (rs1 & 0xffff) + (rs2 & 0xffff)
		elif opc == 6 :		context[rst] = (rs1 & 0xffff) - (rs2 & 0xffff)
		elif opc == 8 :		context[rst] = rs2
		elif opc == 9 :		context[rst] = (context[rst] << 8) | (rs2 & 0xff)
		elif opc == 10 :
					if (imm == 1) :
						if rs1 == 0 : pc = pc + rs2;
					else :
						if rs1 == 0 : pc = rs2 - 2
		elif opc == 11 :
					if (imm == 1) :
						if rs1 != 0 : pc = pc + rs2;
					else :
						if rs1 != 0 : pc = rs2 - 2
		else :
					out.insert(END, ("\nInvalid computation / branch instruction at %04x.\n" % context[8]))
					out.see(END)
	elif (imm == 0 and op2 == 1) :
		if opc == 0 :		context[rst] = (rs1 & 0xffff) >> 1
		elif opc == 1 :		context[rst] = rs1 >> 1
		else :
					out.insert(END, ("\nInvalid shift instruction at %04x.\n" % context[8]))
					out.see(END)
	elif (imm == 0 and op2 == 2) :
		if opc == 0 :
					if (rs2 & 0x1) :
						byte = memory[(rs2 & 0xffff) >> 1] & 0xff
					else :
						byte = memory[(rs2 & 0xffff) >> 1] >> 8

					if byte > 0x7f : context[rst] = byte - 0x100
					else : context[rst] = byte
		elif opc == 1 :
					if (rs2 & 0x1) :
						memory[(rs2 & 0xffff) >> 1] = (memory[(rs2 & 0xffff) >> 1] & 0xff00) | (rs1 & 0xff)
					else :
						memory[(rs2 & 0xffff) >> 1] = (memory[(rs2 & 0xffff) >> 1] & 0x00ff) | ((rs1 & 0xff) << 8)
		elif opc == 4 :
					if (rs2 & 0xffff) == 0xf004 :			# emulate an input character device (address: 61444)
						if len(terminput) == 0 :
							terminput = askstring("Input", "string val:") + '\0';
						result = int(ord(terminput[0]))
						terminput = terminput[1:]
						context[rst] = result
					elif (rs2 & 0xffff) == 0xf006 :			# emulate an input integer device (address: 61446)
						result = askstring("Input", "int val:")
						if result :
							context[rst] = int(result)
					else :
						context[rst] = memory[(rs2 & 0xffff) >> 1]
		elif opc == 5 :
					if (rs2 & 0xffff) == 0xf000 :			# emulate an output character device (address: 61440)
						out.insert(END, chr(rs1 & 0xff))
						out.see(END)
					elif (rs2 & 0xffff) == 0xf002 :			# emulate an output integer device (address: 61442)
						out.insert(END, str(rs1))
						out.see(END)
					else :
						memory[(rs2 & 0xffff) >> 1] = rs1
		else :
					out.insert(END, ("\nInvalid load/store instruction at %04x.\n" % context[8]))
					out.see(END)
	else :
					out.insert(END, ("\nInvalid instruction at %04x.\n" % context[8]))
					out.see(END)

	# increment the program counter
	pc = pc + 2
	context[8] = pc
	# fix the stored word to the matching hardware size
	context[rst] &= 0xffff

	cycles += 1
	# update register labels
	refresh_regs()

	return 1


def newprogram() :
	textasm.delete('1.0', END)
	textasm.delete('1.0', END)

def openprogram() :
	name = askopenfilename()
	if (name) :
		program = open(name, "r")
		if program :
			program.seek(0)
			textasm.delete('1.0', END)
			for lin in program :
				textasm.insert(END, lin)
			program.close()

def openadditionalprogram() :
	name = askopenfilename()
	if (name) :
		program = open(name, "r")
		if program :
			program.seek(0)
			textasm.insert(END, "\n")
			for lin in program :
				textasm.insert(END, lin)
			program.close()

def saveprogram() :
	name = asksaveasfilename()
	if (name) :
		program = open(name, "w")
		if program :
			program.write(textasm.get('1.0', 'end'))
			program.close()

def reset() :
	global cycles, machine
	# clear GPRs
	for i in range(8) :
		context[i] = 0
	# set the stack pointer to the last memory position
	context[7] = len(memory) * 2 - 2
	# set pc to zero
	context[8] = 0
	# reset breakpoint
	machine = STOPPED

	cycles = 0
	refresh_regs()
	textdump.focus()
	textdump.activate(0)
	textdump.see(0)

def run() :
	global machine

	if len(memory) > 0 :
		if machine == STOPPED :
			machine = RUNNING
			run_step()
	else :
		showerror("Error", "No program in memory.")

def run_step() :
	inst = memory[context[8] >> 1]
	last_pc = context[8]

	if cycle() :
		textdump.focus()
		textdump.activate(context[8] >> 1)
		textdump.see(context[8] >> 1)

		if context[8] == context[10] :
			out.insert(END, ("\nBreakpoint at %04x.\n" % context[8]))
			out.see(END)
		else:
			if context[7] < context[9] :
				out.insert(END, ("\nStack overflow detected at %04x.\n" % context[8]))
				out.see(END)
			else :
				if machine != STOPPED :
					root.after(cycle_delay, run_step)
	else :
		out.insert(END, ("\nProgram halted at %04x.\n" % context[8]))
		out.see(END)

def stop() :
	global machine
	machine = STOPPED

def step() :
	if len(memory) > 0 :
		stop()
		inst = memory[context[8] >> 1]
		last_pc = context[8]

		if cycle() :
			textdump.focus()
			textdump.activate(context[8] >> 1)
			textdump.see(context[8] >> 1)

			if context[7] < context[9] :
				out.insert(END, ("\nStack overflow detected at %04x.\n" % context[8]))
				out.see(END)
		else :
			out.insert(END, ("\nProgram halted at %04x.\n" % context[8]))
			out.see(END)
	else :
		showerror("Error", "No program in memory.")

def refresh_regs() :
	for i in range(9) :
		root.reg_label[i].set(reg_names[i] + tohex(context[i]))
	root.cycle.set("Cycle: " + str(cycles) + "\n")

def set_breakpoint() :
	result = askstring("Set breakpoint", "Program address (hex):")
	if result :
		context[10] = int(result, 16)

def set_cycledelay() :
	global cycle_delay
	result = askstring("Set machine cycle delay", "Delay (ms):")
	if result > 0 :
		cycle_delay = int(result)

def clear_term() :
	out.delete('1.0', END)

def memdump() :
	memwindow = Toplevel(root)
	memwindow.title("Memory dump")
	memwindow.geometry("600x652+50+50")
	memwindow.resizable(0,0)
	mem_dump = Listbox(memwindow, height=24, width=65, font=('Courier', 11))
	mem_dumpscroll = Scrollbar(memwindow, command=mem_dump.yview)
	mem_dump.configure(yscrollcommand=mem_dumpscroll.set)
	mem_dump.pack(side=LEFT, fill=BOTH)
	mem_dumpscroll.pack(side=LEFT, fill=Y)

	k = 0
	while k < len(memory) * 2 :
		dump_line = str(tohex(k)) + ': '
		l = 0
		while l < 8 :
			dump_line = dump_line + tohex(memory[k / 2 + l]) + ' '
			l += 1
		dump_line += '|'
		l = 0
		while l < 8 :
			ch1 = memory[k / 2 + l] >> 8
			ch2 = memory[k / 2 + l] & 0xff
			if ((ch1 >= 32) and (ch1 <= 126)) :
				dump_line += chr(ch1)
			else :
				dump_line += '.'
			if ((ch2 >= 32) and (ch2 <= 126)) :
				dump_line += chr(ch2)
			else :
				dump_line += '.'
			l += 1
		dump_line += '|'
		mem_dump.insert(END, dump_line)
		k += 16

root = Tk()
menu = Menu(root)
root.geometry("1000x692+30+30")
root.resizable(0,0)
root.config(menu=menu)

programmenu = Menu(menu)
menu.add_cascade(label="Program", menu=programmenu)
programmenu.add_command(label="New", command=newprogram)
programmenu.add_command(label="Load", command=openprogram)
programmenu.add_command(label="Load additional file", command=openadditionalprogram)
programmenu.add_command(label="Save as", command=saveprogram)
programmenu.add_separator()
programmenu.add_command(label="Assemble", command=assembler)
programmenu.add_separator()
programmenu.add_command(label="Exit", command=root.quit)

machinemenu = Menu(menu)
menu.add_cascade(label="Machine", menu=machinemenu)
machinemenu.add_command(label="Reset", command=reset)
machinemenu.add_command(label="Stop", command=stop)
machinemenu.add_command(label="Run", command=run)
machinemenu.add_command(label="Step", command=step)
machinemenu.add_separator()
machinemenu.add_command(label="Set breakpoint", command=set_breakpoint)
machinemenu.add_command(label="Set machine cycle delay", command=set_cycledelay)
machinemenu.add_command(label="Clear terminal", command=clear_term)
machinemenu.add_command(label="Memory dump", command=memdump)

topframe = Frame(root)
topframe.pack()
middleframe = Frame(root)
middleframe.pack()
bottomframe = Frame(root)
bottomframe.pack()

Label(topframe, text="Program:", width=46, font=('Courier', 11, 'bold'), anchor=W).pack(side=LEFT)
Label(topframe, text="Object code / disassembly:", width=28, font=('Courier', 11, 'bold'), anchor=W).pack(side=LEFT)
Label(topframe, text="Symbol table:", width=22, font=('Courier', 11, 'bold'), anchor=W).pack(side=LEFT)
Label(topframe, text="Registers:", width=16, font=('Courier', 11, 'bold'), anchor=W).pack(side=LEFT)

asmxscrollbar = Scrollbar(middleframe, orient=HORIZONTAL)
asmyscrollbar = Scrollbar(middleframe)
textasm = Text(middleframe, wrap=NONE, xscrollcommand=asmxscrollbar.set, yscrollcommand=asmyscrollbar.set, height=24, width=44, font=('Courier', 11))
asmxscrollbar.pack(side=BOTTOM, fill=X)
textasm.pack(side=LEFT, fill=BOTH)
asmyscrollbar.pack(side=LEFT, fill=Y)
asmxscrollbar.config(command=textasm.xview)
asmyscrollbar.config(command=textasm.yview)

textdump = Listbox(middleframe, height=24, width=26, font=('Courier', 11))
textdumpscroll = Scrollbar(middleframe, command=textdump.yview)
textdump.configure(yscrollcommand=textdumpscroll.set)
textdump.pack(side=LEFT, fill=BOTH)
textdumpscroll.pack(side=LEFT, fill=Y)

textsym = Listbox(middleframe, height=24, width=18, font=('Courier', 11))
textsymscroll = Scrollbar(middleframe, command=textsym.yview)
textsym.configure(yscrollcommand=textsymscroll.set)
textsym.pack(side=LEFT, fill=BOTH)
textsymscroll.pack(side=LEFT, fill=Y)

root.reg_label = []
for i in range(9):
	root.reg_label.append(StringVar())

for i in range(9) :
	Label(middleframe, textvariable=root.reg_label[i], width=25, font=('Courier', 11)).pack()

Label(middleframe, text="\nControl:\n", width=25, font=('Courier', 11, 'bold')).pack()

root.cycle = StringVar()
Label(middleframe, textvariable=root.cycle, width=25, font=('Courier', 11)).pack()

refresh_regs()

Button(middleframe, text='Reset', width=14, command=reset).pack()
Button(middleframe, text='Stop', width=14, command=stop).pack()
Button(middleframe, text='Run', width=14, command=run).pack()
Button(middleframe, text='Step', width=14, command=step).pack()

out = Text(bottomframe, height=14, width=122, font=('Courier', 10))
outscroll = Scrollbar(bottomframe, command=out.yview)
out.configure(yscrollcommand=outscroll.set)
out.pack(side=LEFT, fill=BOTH)
outscroll.pack(side=LEFT, fill=Y)

mainloop()
