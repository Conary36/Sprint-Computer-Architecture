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

    @property
    def sp(self):
        return self.reg[7]

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        else:
            raise Exception("Unsopported ALU operations")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not HLT:
            # ir (Instruction Register) = value at memory address in PC (Program Counter)
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(ir, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == self.HLT:
            self.HLT = True
            self.pc += 1
        elif instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2
        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3
        elif instruction == MUL:
            self.reg[operand_a] *= operand_b
            self.pc += 3


        elif instruction == PUSH:
            chosen_register = self.ram[self.pc + 1]
            current_reg_value = self.reg[chosen_register]
            # Decrement pointer
            self.reg[self.sp] -= 1
            self.ram[self.reg[self.sp]] = current_reg_value
            self.pc += 2

        elif instruction == POP:
            chosen_register = self.ram[self.pc + 1]
            current_mem_val = self.ram[self.reg[self.sp]]
            self.reg[chosen_register] = current_mem_val
            # Increment pointer
            self.reg[self.sp] += 1
            self.pc += 2

        elif instruction == CALL:
            # PUSH the return address onto the stack
            ## Find address/index of the command after call
            next_command_address = self.pc + 2
            # Push the address onto the stack
            ## Decrement the pointer
            self.reg[self.sp] -= 1
            # add next command address into stack pointer memory
            self.ram[self.reg[self.sp]] = next_command_address
            # Jump and set the PC to address directed to by register
            reg_number = self.ram[self.pc + 1]
            # Get address of Subroutine out of register
            address_to_jump_to: int = self.reg[reg_number]
            # set the PC
            self.pc = address_to_jump_to



        elif instruction == RET:
            self.pc = self.ram[self.reg[self.sp]]
            # pop from stack
            self.reg[self.sp] += 1
