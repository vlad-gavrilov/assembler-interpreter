import argparse
from os.path import exists

from .interpreter import Interpreter


def main():
    parser = argparse.ArgumentParser(description='Assembler interpreter')
    parser.add_argument('path', help='the path to the program to be executed')
    parser.add_argument('-l', '--labels', help='show labels', action='store_true')
    parser.add_argument('-p', '--program', help='show prepared program', action='store_true')
    parser.add_argument('-r', '--registers', help='show register values', action='store_true')
    args = parser.parse_args()

    if not exists(args.path):
        print(f'Cannot find the file in the path "{args.path}"')
    else:
        with open(args.path) as f:
            program = f.read()

        interpreter = Interpreter(program)

        output = interpreter.run()
        args.labels and print('Labels: ', interpreter.labels)
        args.program and print('Program: ', *interpreter.program, sep='\n')
        args.registers and print('Registers: ', interpreter.registers)
        print('Output: ', output)


if __name__ == '__main__':
    main()
