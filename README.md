# Assembler interpreter

## Usage

```bash
asmint --help
```

```text
usage: asmint [-h] [-l] [-p] [-r] path

Assembler interpreter

positional arguments:
  path             the path to the program to be executed

optional arguments:
  -h, --help       show this help message and exit
  -l, --labels     show labels
  -p, --program    show prepared program
  -r, --registers  show register values
```

## Example

A program named **factorial.txt**:

```text
mov   a, 5
mov   b, a
mov   c, a
call  proc_fact
call  print
end

proc_fact:
    dec   b
    mul   c, b
    cmp   b, 1
    jne   proc_fact
    ret

print:
    msg   a, '! = ', c ; output text
    ret
```

Calling the utility:

```bash
asmint factorial.txt
```

Program output:

```text
Output:  5! = 120
```

## External links
This project was inspired by [this](https://www.codewars.com/kata/58e61f3d8ff24f774400002c) CodeWars kata