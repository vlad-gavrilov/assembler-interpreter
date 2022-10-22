import pytest

from src.asmint.interpreter import Interpreter


program = '''
mov   a, {base}            ; value1
mov   b, {power}           ; value2
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
'''


@pytest.mark.parametrize("base, power", [
    (2, 10),
    (10, 2),
    (1, 10),
    (10, 1),
    (100, 100),
    (123456, 789),
    (99999, 99),
])
def test_power(base, power):
    interpreter = Interpreter(program.format(
        base=base,
        power=power,
    ))
    expected_output = '{base}^{power} = {result}'.format(
        base=base,
        power=power,
        result=base**power,
    )
    assert interpreter.run() == expected_output
