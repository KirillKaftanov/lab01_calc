'''тесты конвертера величин'''

import pytest

from toolkit.converter import convert


def test_length_conversion():
    '''проверка перевода длины'''
    assert convert('100', 'cm', 'm') == 1


def test_mass_conversion():
    '''проверка перевода массы'''
    assert convert('1000', 'g', 'kg') == 1


def test_temperature_conversion():
    '''проверка температуры'''
    assert convert('0', 'c', 'f') == 32


def test_same_unit_conversion():
    '''одинаковые единицы'''
    assert convert('10', 'm', 'm') == 10

def test_converter_return_float():
    '''проверка возвращаемого типа конвертера'''

    result = convert('100', 'cm', 'm')

    assert isinstance(result, float)

def test_absolute_zero_boundary():
    '''проверка допустимой температуры абсолютного нуля'''

    assert convert('0', 'k', 'c') == pytest.approx(-273.15)

'''негативные тесты'''


def test_unknown_unit():
    '''неизвестная единица'''
    with pytest.raises(ValueError):
        convert('100', 'abc', 'm')


def test_incompatible_units():
    '''несовместимые единицы'''
    with pytest.raises(ValueError):
        convert('10', 'kg', 'm')


def test_invalid_value():
    '''неверное число'''
    with pytest.raises(ValueError):
        convert('abc', 'cm', 'm')

def test_absolute_zero_error():
    '''проверка температуры ниже абсолютного нуля'''

    with pytest.raises(ValueError, match='абсолютного нуля'):
        convert('-1', 'k', 'k')
