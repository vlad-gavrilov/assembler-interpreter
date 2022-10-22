import pytest

from src.asmint.interpreter import Interpreter


@pytest.mark.parametrize("program_name, output", [
    ('first_program', '(5+1)/2 = 3'),
    ('factorial', '5! = 120'),
    ('power', '2^10 = 1024'),
    ('fibonacci', 'Term 8 of Fibonacci series is: 21'),
    ('modulo', 'mod(11, 3) = 2'),
    ('gcd', 'gcd(81, 153) = 9'),
    ('failing', -1),
    ('power_mangled', '2^10 = 1024'),
])
def test_interpreter_output(program_name, output):
    with open(f'../examples/{program_name}', 'r') as f:
        program = f.read()
    interpreter = Interpreter(program)
    assert interpreter.run() == output
