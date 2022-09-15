import re


class Interpreter:
    def __init__(self, program):
        self.registers = {}
        self.cmp_register1 = None
        self.cmp_register2 = None
        self.previous_index_stack = []
        self.msg = ''

        self.instructions = {
            'mov': self.__mov,
            'inc': self.__inc,
            'dec': self.__dec,
            'add': self.__add,
            'sub': self.__sub,
            'mul': self.__mul,
            'div': self.__div,
            'jmp': self.__jmp,
            'cmp': self.__cmp,
            'jne': self.__jne,
            'je': self.__je,
            'jge': self.__jge,
            'jg': self.__jg,
            'jle': self.__jle,
            'jl': self.__jl,
            'call': self.__call,
            'ret': self.__ret,
            'msg': self.__msg,
            'end': self.__end,
            'jnz': self.__jnz,
        }

        self.current_instruction_index = 0
        self.labels = {}
        self.program = []
        self.program_length = 0

        self.prepare(program)

    def prepare(self, program):
        lines = program.splitlines()
        i = 0
        while i < len(lines):
            instruction = lines[i]
            if re.fullmatch(r'\s*|\s*;.*', instruction):
                lines.remove(instruction)
                continue
            if ';' in instruction:
                lines[i] = lines[i][0: instruction.index(';')].strip()
            if m := re.fullmatch(r'\s*(\w+):\s*', instruction):
                self.labels[m.group(1)] = i
                del lines[i]
                continue

            lines[i] = self.parse_line(lines[i])

            i += 1

        self.program = lines
        self.program_length = len(self.program)

    def get_value(self, value):
        return self.registers[value] if value in self.registers else int(value)

    @staticmethod
    def parse_line(line):
        split = re.findall(r'(-?\w+:?|\'.*?\'),?\s*', line)

        return {
            'instruction_name': split[0],
            'operands': [arg.strip('\'') for arg in split[1:]],
        }

    def run(self):
        while self.current_instruction_index < self.program_length:
            current_command = self.program[self.current_instruction_index]

            self.current_instruction_index += 1
            result = self.instructions[current_command['instruction_name']](*current_command['operands'])
            if result:
                return result
        return -1

    def __mov(self, a, b):
        self.registers[a] = self.get_value(b)

    def __inc(self, a):
        self.registers[a] += 1

    def __dec(self, a):
        self.registers[a] -= 1

    def __add(self, a, b):
        self.registers[a] += self.get_value(b)

    def __sub(self, a, b):
        self.registers[a] -= self.get_value(b)

    def __mul(self, a, b):
        self.registers[a] *= self.get_value(b)

    def __div(self, a, b):
        self.registers[a] //= self.get_value(b)

    def __jmp(self, lbl):
        self.current_instruction_index = self.labels[lbl]

    def __cmp(self, x, y):
        self.cmp_register1 = self.get_value(x)
        self.cmp_register2 = self.get_value(y)

    def __jne(self, lbl):
        if self.cmp_register1 != self.cmp_register2:
            self.current_instruction_index = self.labels[lbl]

    def __je(self, lbl):
        if self.cmp_register1 == self.cmp_register2:
            self.current_instruction_index = self.labels[lbl]

    def __jge(self, lbl):
        if self.cmp_register1 >= self.cmp_register2:
            self.current_instruction_index = self.labels[lbl]

    def __jg(self, lbl):
        if self.cmp_register1 > self.cmp_register2:
            self.current_instruction_index = self.labels[lbl]

    def __jle(self, lbl):
        if self.cmp_register1 <= self.cmp_register2:
            self.current_instruction_index = self.labels[lbl]

    def __jl(self, lbl):
        if self.cmp_register1 < self.cmp_register2:
            self.current_instruction_index = self.labels[lbl]

    def __call(self, lbl):
        self.previous_index_stack.append(self.current_instruction_index)
        self.current_instruction_index = self.labels[lbl]

    def __ret(self):
        if not self.previous_index_stack:
            return -1
        self.current_instruction_index = self.previous_index_stack.pop()

    def __msg(self, *args):
        self.msg = ''
        for argument in args:
            if argument in self.registers:
                self.msg += str(self.registers[argument])
            else:
                self.msg += argument

    def __end(self):
        return self.msg

    def __jnz(self, a, b):
        if self.get_value(a) != 0:
            self.current_instruction_index += self.get_value(b) - 1
