""" CPU COMPUTATION"""
import sys
import os.path

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """ Main CPU Class"""

    def __init__(self):
        """ Construct a New CPU"""
        # max writable ram
        self.reg = [0] * 8  # register 8 bits
        # SP points at the value at the top of the stack (most recently pushed), or at address F4 if empty.
        self.reg[7] = 0xF4  # 244 # int('F4', 16)
        self.ir = 0  # instruction register
        self.ram = [0] * 256  # ram is 256 bits
        self.mar = 0
        self.mdr = 0
        self.fl = 0
        self.pc = 0
        self.running = True
        self.execution_table = {HLT: self.hlt, LDI: self.ldi, PRN: self.prn, MUL: self.mul, PUSH: self.push,
                                POP: self.pop, CALL: self.call, ADD: self.add, RET: self.ret, JMP: self.jmp,
                                CMP: self.cmp, JEQ: self.jeq, JNE: self.jne}

    def ldi(self, reg_num, mdr):
        self.reg[reg_num] = mdr

    def prn(self, reg_num):
        print(self.reg[reg_num])

    def load(self, filename):
        """Load a program into memory."""
        memory_address = 0
        program = []
        with open(filename) as f:
            for line in f:
                split_line = line.split('#')[0]
                stripped_split_line = split_line.strip()
                if stripped_split_line != "":
                    command = int(stripped_split_line, 2)
                    program.append(command)
                    print(command)
        for instruction in program:
            self.ram[memory_address] = instruction
            memory_address += 1
