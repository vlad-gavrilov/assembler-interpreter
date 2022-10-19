# Assembler interpreter

## Instructions

This assembler interpreter supports a number of basic instructions.
They are common to most of the different assembler dialects.
It also supports labels, user comments and creating an output message.
The entire list of supported instructions is shown below:

* ```mov x, y``` - copy y (either an integer or the value of a register) into register x.
* ```inc x``` - increase the content of register x by one.
* ```dec x``` - decrease the content of register x by one.
* ```add x, y``` - add the content of the register x with y (either an integer or the value of a register) and stores the result in x (i.e. ```register[x] += y```).
* ```sub x, y``` - subtract y (either an integer or the value of a register) from the register x and stores the result in x (i.e. ```register[x] -= y```).
* ```mul x, y``` - same with multiply (i.e. ```register[x] *= y```).
* ```div x, y``` - same with integer division (i.e. ```register[x] /= y```).
* ```label:``` - define a label position (```label = identifier + ":"```, an identifier being a string that does not match any other command). Jump commands and call are aimed to these labels positions in the program.
* ```jmp lbl```- jumps to the label ```lbl```.
* ```cmp x, y``` - compares x (either an integer or the value of a register) and y (either an integer or the value of a register). The result is used in the conditional jumps (```jne```, ```je```, ```jge```, ```jg```, ```jle``` and ```jl```)
* ```jne lbl``` - jump to the label ```lbl``` if the values of the previous ```cmp``` command were not equal.
* ```je lbl``` - jump to the label ```lbl``` if the values of the previous ```cmp``` command were equal.
* ```jge lbl``` - jump to the label ```lbl``` if x was greater or equal than y in the previous ```cmp``` command.
* ```jg lbl``` - jump to the label ```lbl``` if x was greater than y in the previous ```cmp``` command.
* ```jle lbl``` - jump to the label ```lbl``` if x was less or equal than y in the previous ```cmp``` command.
* ```jl lbl``` - jump to the label ```lbl``` if x was less than y in the previous ```cmp``` command.
* ```call lbl``` - call to the subroutine identified by ```lbl```. When a ```ret``` is found in a subroutine, the instruction pointer should return to the instruction next to this ```call``` command.
* ```ret``` - when a ```ret``` is found in a subroutine, the instruction pointer should return to the instruction that called the current function.
* ```msg 'Register: ', x``` - this instruction stores the output of the program. It may contain text strings (delimited by single quotes) and registers. The number of arguments isn't limited and will vary, depending on the program.
* ```end``` - this instruction indicates that the program ends correctly, so the stored output is returned (if the program terminates without this instruction it should return the default output: see below).
* ```; comment``` - comments should not be taken in consideration during the execution of the program.

The output format is a string. But if the program doesn't reach the ```end``` instruction, the number ```-1``` will be returned.

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

There is a directory ```examples``` containing a bunch of example programs implemented using this assembly language.
You can add your own interesting use case by creating a pull request on [GitHub](https://github.com/vlad-gavrilov/assembler-interpreter/pulls). All PRs are welcome :)

An example program named *factorial.txt*:

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

Another example of use - *power.txt*:

```text
mov   a, 2            ; value1
mov   b, 10           ; value2
mov   c, a            ; temp1
mov   d, b            ; temp2
call  proc_func
call  print
add   a, -1
end

proc_func:
    cmp   d, 1
    je    continue
    mul   c, a
    dec   d
    call  proc_func

continue:
    ret

print:
    msg a, '^', b, ' = ', c
    ret
```

Output:

```text
Output:  2^10 = 1024
```

This interpreter can also handle multiple tabs and spaces in program code and ignore all comment text.
Let's use a "mangled" version of the *power.txt* program. Let's call it *power_mangled.txt*. Here is the full code:

```text
mov   a, 2            ; value1
 mov   b, 10           ; value2
  mov   c, a            ; temp1
            mov   d, b            ; temp2
call            proc_func
call                                                print
add a, -1
end
; comment1
; comment2
; comment3
; yet another comment
proc_func:
cmp   d, 1
 je    continue
                        mul   c, a
    dec   d         ; here is a comment message
  call  proc_func

continue:
    ret
print:
; comment1
;comment2
;comment3
;             yet another comment
    msg a, '^', b, ' = ', c
ret
```

As you can see, the result is the same as in the previous example:
```text
Output:  2^10 = 1024
```

## External links
This project was inspired by [this](https://www.codewars.com/kata/58e61f3d8ff24f774400002c) CodeWars kata