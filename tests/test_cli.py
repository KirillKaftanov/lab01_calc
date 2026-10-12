'''CLI тесты'''

import subprocess
import sys


def run_cli(*arguments):
    '''запуск CLI программы'''

    return subprocess.run([sys.executable, '-m', 'toolkit', *arguments], capture_output=True, text=True, check=False)


def test_cli_calculator():
    '''проверка калькулятора через CLI'''

    result = run_cli('calc', '2+3*4')

    assert result.stdout.strip() == '14'


def test_cli_converter():
    '''проверка конвертера через CLI'''

    result = run_cli('convert', '100', '--from', 'cm', '--to', 'm')

    assert result.stdout.strip() == '1.0'

def test_cli_calculator_error():
    '''проверка ошибки калькулятора через CLI'''

    result = run_cli('calc', '2/0')

    assert result.returncode == 2
    assert result.stdout == ''
    assert 'деление на ноль' in result.stderr


def test_cli_negative_expression():
    '''проверка отрицательного выражения через CLI'''

    result = run_cli('calc', '-5+10')

    assert result.returncode == 0
    assert result.stdout.strip() == '5'
    assert result.stderr == ''


def test_cli_converter_error():
    '''проверка ошибки конвертера через CLI'''

    result = run_cli('convert', 'abc', '--from', 'cm', '--to', 'm')

    assert result.returncode == 2
    assert result.stdout == ''
    assert 'неверное числовое значение' in result.stderr


def test_cli_converter_uppercase_unit():
    '''проверка регистра единиц в CLI'''

    result = run_cli('convert', '100', '--from', 'CM', '--to', 'M')

    assert result.returncode == 0
    assert result.stdout.strip() == '1.0'
