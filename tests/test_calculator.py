'''тесты вычислительного ядра калькулятора'''

from decimal import Decimal

import pytest

from toolkit.calculator import calculate


def test_addition():
    '''проверка сложения'''
    assert calculate('2+3') == 5.0


def test_subtraction():
    '''проверка вычитания'''
    assert calculate('10-4') == 6.0


def test_multiplication():
    '''проверка умножения'''
    assert calculate('3*4') == 12.0


def test_division():
    '''проверка деления'''
    assert calculate('10/2') == 5.0


def test_priority_operations():
    '''проверка приоритета умножения'''
    assert calculate('2+3*4') == 14.0


def test_brackets():
    '''проверка скобок'''
    assert calculate('(2+3)*4') == 20.0


def test_float_numbers():
    '''проверка вещественных чисел'''
    assert calculate('2.5+1.5') == 4.0


def test_unary_minus():
    '''проверка унарного минуса'''
    assert calculate('-5+10') == 5.0


def test_spaces_between_elements():
    '''проверка игнорирования пробелов'''
    assert calculate('2 + 3 * 4') == 14.0


def test_complex_priority_chain():
    '''проверка нескольких приоритетов и скобок'''
    assert calculate('150-(7+8)*(12-5)+64/8') == 53


def test_nested_four_operations():
    '''проверка вложенных скобок со всеми операциями'''
    assert calculate('((45/5+7)*(18-6))/8') == 24


def test_several_groups_in_parentheses():
    '''проверка разности произведений в скобках'''
    assert calculate('((2+3)*(4+5)-(6+7))/8') == 4


def test_negative_result_of_group():
    '''проверка отрицательного результата сложной скобки'''
    assert calculate('((100-36)/8+2.5)*(-4)') == -42


def test_nested_multiplication_groups():
    '''проверка вложенного умножения и сложения'''
    assert calculate('2*(3+(4*(5-2)))-7') == 23


def test_left_associative_division():
    '''проверка деления и умножения слева направо'''
    assert calculate('120/4/3*5-11') == 39


def test_left_associative_mixed():
    '''проверка чередования умножения и деления'''
    assert calculate('64/8*3/2+17') == 29


def test_parenthesized_denominator():
    '''проверка составного знаменателя со скобками'''
    assert calculate('(250-10*5)/(2*(7+3))') == 10


def test_product_of_negative_groups():
    '''проверка произведения двух отрицательных скобок'''
    assert calculate('(-12+8)*(-5-3)/4') == 8


def test_unary_minus_before_group():
    '''проверка минуса перед результатом скобки'''
    assert calculate('-(10-14)*(-3+9)') == 24


def test_nested_negations():
    '''проверка двойного отрицания во вложенных скобках'''
    assert calculate('(-(-5)+3)*(12/4)') == 24


def test_unary_with_several_terms():
    '''проверка унарных знаков в длинной сумме'''
    assert calculate('15+(-8)-(-6)+(-4)*2') == 5


def test_negative_factor_and_bracket():
    '''проверка отрицательных множителей и скобок'''
    assert calculate('3*-(2+5)+(-4)*-2') == -13


def test_negative_parenthesized_divisor():
    '''проверка отрицательного знаменателя и множителя'''
    assert calculate('24/-(-3)+-2*(4-7)') == 14


def test_negative_factors_before_groups():
    '''проверка двух отрицательных множителей-скобок'''
    assert calculate('-(2+3)*-(4-1)') == 15


def test_decimal_precedence():
    '''проверка точной арифметики десятичных дробей'''
    assert calculate('10.75-2.125*4+.5') == 2.75


def test_leading_and_trailing_decimal_dots():
    '''проверка чисел с пропущенной целой и дробной частью'''
    assert calculate('5. / .25 + 3.') == 23


def test_numbers_with_leading_zeroes():
    '''проверка ведущих нулей и десятичных дробей'''
    assert calculate('00012.500 / 05 + .125') == 2.625


def test_tiny_decimal_combined_with_exponent():
    '''проверка малой дроби и положительной степени'''
    assert calculate('0.0000001*1e7+1e-7') == Decimal('1.0000001')


def test_scientific_both_letter_cases():
    '''проверка научной записи с e и E'''
    assert calculate('1.2e3/4+2.5E-2') == Decimal('300.025')


def test_signed_scientific_exponents():
    '''проверка знаков при показателях степени'''
    assert calculate('3E+4*2e-3-.5E+1') == 55


def test_small_scientific_terms():
    '''проверка сложения нескольких маленьких степеней'''
    assert calculate('1e-5+2e-5-3e-6') == Decimal('0.000027')


def test_scientific_with_parentheses():
    '''проверка научной записи со скобками'''
    assert calculate('1.25E+2*(4-1.5)/5') == 62.5


def test_scientific_inside_parentheses():
    '''проверка десятичных степеней внутри скобок'''
    assert calculate('(2.5E-2+7.5E-2)*1e3') == 100


def test_scientific_denominator():
    '''проверка научной записи в знаменателе'''
    assert calculate('1e+2/(5e-1)+2E-3') == Decimal('200.002')


def test_scientific_nested_groups():
    '''проверка сочетания нескольких научных записей и скобок'''
    assert calculate('((2e2-5e1)/5)+(1e-3*2e3)') == 32


def test_negative_scientific_division():
    '''проверка деления отрицательных чисел в научной записи'''
    assert calculate('(-2E+3)/(-4E+2)+0.125') == 5.125


def test_spaces_in_long_expression():
    '''проверка пробелов вокруг скобок и операций'''
    assert calculate('  ( 18 - 7 ) * ( 5 + 3 )  ') == 88


def test_spaces_around_fraction():
    '''проверка пробелов возле дробей без целой части'''
    assert calculate('1 + .5 * ( 8 - 2 )') == 4


def test_scientific_and_spaces():
    '''проверка пробелов между числами в научной записи и знаками'''
    assert calculate('1e-5 + 2E-5 * (4 + 1)') == Decimal('0.00011')


def test_subtraction_of_negative_product():
    '''проверка вычитания отрицательного произведения'''
    assert calculate('12--7*3+(-4)') == 29


def test_plus_and_minus_before_product():
    '''проверка соседних знаков перед умножением'''
    assert calculate('25+-5*(3+1)') == 5


def test_adjacent_signs_after_division():
    '''проверка соседних знаков после деления'''
    assert calculate('5/0.5--2') == 12


def test_nested_cancellation():
    '''проверка взаимного уничтожения вложенных частей'''
    assert calculate('((-(-2)*3)+2*-(4-1))') == 0


def test_mixed_unary_operators():
    '''проверка разных унарных знаков и скобок'''
    assert calculate('1/-(-2)+2*+(3+1)') == 8.5


def test_deep_parentheses():
    '''проверка глубины вложенных скобок до 60 уровней'''
    assert calculate('(' * 60 + '12.5*4-7' + ')' * 60) == 43


def test_long_mixed_chain():
    '''проверка длинной цепочки сложения, умножения и деления'''
    assert calculate('1+2*3-4/2+' * 80 + '5') == 405


def test_large_integer_without_rounding():
    '''проверка целого числа из 600 цифр без округления'''
    assert calculate('9' * 600) == int('9' * 600)


def test_long_fractional_literal():
    '''проверка дробного числа с тысячей ведущих нулей'''
    assert calculate('0.' + '0' * 1000 + '125') == Decimal('1.25E-1001')


def test_long_decimal_cancellation():
    '''проверка точной отмены длинных дробей'''
    assert calculate('-0.12345678901234567890123456+0.12345678901234567890123456') == 0


def test_long_divisor_rounding():
    '''проверка точности деления на длинное число в скобках'''
    assert calculate('1/(26786892822985746193223685)') == Decimal('3.733169078654405301598069E-26')


def test_periodic_decimal_rounding():
    '''проверка округления бесконечной десятичной дроби'''
    assert calculate('1/3') == Decimal('0.3333333333333333333333333')


def test_signed_scientific_multiplication():
    '''проверка отрицательных множителей в научной записи'''
    assert calculate('1e-5*-2e2+3') == Decimal('2.998')


def test_nested_unary_pluses():
    '''проверка унарных плюсов во вложенных скобках'''
    assert calculate('((+5)-(-3))*+2') == 16

'''негативные тесты'''

def test_empty_expression():
    '''проверка пустого выражения'''
    with pytest.raises(ValueError):
        calculate('')


def test_invalid_symbol():
    '''проверка запрещённого символа'''
    with pytest.raises(ValueError):
        calculate('2+a')


def test_invalid_number():
    '''проверка нескольких точек в числе'''
    with pytest.raises(ValueError):
        calculate('1.2.3')


def test_invalid_brackets():
    '''проверка неправильных скобок'''
    with pytest.raises(ValueError):
        calculate('(2+3')


def test_division_by_zero():
    '''проверка деления на ноль'''
    with pytest.raises(ValueError):
        calculate('5/0')


def test_only_spaces():
    '''проверка отказа от строки из одних пробелов'''
    with pytest.raises(ValueError, match='пустое выражение'):
        calculate('     ')


def test_invalid_letter_inside_formula():
    '''проверка отказа от букв в сложном выражении'''
    with pytest.raises(ValueError, match='недопустимый символ'):
        calculate('12+abc*3')


def test_comma_decimal_separator():
    '''проверка отказа от запятой вместо точки'''
    with pytest.raises(ValueError, match='недопустимый символ'):
        calculate('1,5*(2+3)')


def test_forbidden_power_operator():
    '''проверка отказа от оператора возведения в степень'''
    with pytest.raises(ValueError, match='два бинарных оператора подряд'):
        calculate('2**(3+4)')


def test_double_division_operator():
    '''проверка отказа от двойного знака деления'''
    with pytest.raises(ValueError, match='два бинарных оператора подряд'):
        calculate('12//(2+1)')


def test_asterisk_after_opening_bracket():
    '''проверка пропущенного левого операнда после скобки'''
    with pytest.raises(ValueError, match='пропущен операнд внутри скобки'):
        calculate('2+(*3)')


def test_division_after_opening_bracket():
    '''проверка деления без левого операнда после скобки'''
    with pytest.raises(ValueError, match='пропущен операнд внутри скобки'):
        calculate('10+(/2)')


def test_operator_before_closing_bracket():
    '''проверка отсутствующего операнда перед закрывающей скобкой'''
    with pytest.raises(ValueError, match='пропущен операнд'):
        calculate('2*(3+)')


def test_empty_nested_brackets():
    '''проверка пустых вложенных скобок'''
    with pytest.raises(ValueError, match='пропущен операнд'):
        calculate('(2+())*3')


def test_extra_closing_brackets():
    '''проверка лишних закрывающих скобок'''
    with pytest.raises(ValueError, match='неверная последовательность скобок'):
        calculate('2+3))')


def test_missing_closing_bracket_nested():
    '''проверка незакрытой вложенной скобки'''
    with pytest.raises(ValueError, match='количество открывающих и закрывающих скобок'):
        calculate('((2+3)')


def test_implicit_multiplication_before_bracket():
    '''проверка неявного умножения перед скобкой'''
    with pytest.raises(ValueError, match='пропущен оператор перед скобкой'):
        calculate('2(3+4)')


def test_implicit_multiplication_after_bracket():
    '''проверка неявного умножения после скобки'''
    with pytest.raises(ValueError, match='пропущен оператор после скобки'):
        calculate('(2+3)4')


def test_adjacent_brackets_without_operator():
    '''проверка соседних скобок без арифметического знака'''
    with pytest.raises(ValueError, match='пропущен оператор после скобки'):
        calculate('(2+3)(4+5)')


def test_decimal_point_after_bracket():
    '''проверка точки сразу после закрывающей скобки'''
    with pytest.raises(ValueError, match='пропущен оператор после скобки'):
        calculate('(2+3).5')


def test_decimal_point_before_bracket():
    '''проверка точки перед открывающей скобкой'''
    with pytest.raises(ValueError, match='пропущен оператор перед скобкой'):
        calculate('2.(3+4)')


def test_two_decimal_points_in_operand():
    '''проверка нескольких десятичных точек в операнде'''
    with pytest.raises(ValueError, match='неверное числовое значение'):
        calculate('10.5.2+3')


def test_repeated_exponent_marker():
    '''проверка повторного e внутри одного числа'''
    with pytest.raises(ValueError, match='неверное числовое значение'):
        calculate('1e2e3+5')


def test_missing_exponent_digits_plus():
    '''проверка плюса без цифр в научной записи'''
    with pytest.raises(ValueError, match='неверная научная запись'):
        calculate('1e+(2+3)')


def test_missing_exponent_digits_minus():
    '''проверка минуса без цифр в научной записи'''
    with pytest.raises(ValueError, match='неверная научная запись'):
        calculate('1e-(2+3)')


def test_space_inside_scientific_exponent():
    '''проверка пробела после знака показателя степени'''
    with pytest.raises(ValueError, match='пробел внутри научной записи числа'):
        calculate('2e- 3+1')


def test_space_between_integer_digits():
    '''проверка пробела внутри целой части числа'''
    with pytest.raises(ValueError, match='пробел внутри числа'):
        calculate('12 34+5')


def test_space_after_decimal_dot():
    '''проверка пробела внутри дробной части числа'''
    with pytest.raises(ValueError, match='пробел внутри числа'):
        calculate('12. 34+5')


def test_space_before_decimal_dot():
    '''проверка пробела перед десятичной точкой'''
    with pytest.raises(ValueError, match='пробел внутри числа'):
        calculate('12 .34+5')


def test_space_before_exponent():
    '''проверка пробела перед показателем степени'''
    with pytest.raises(ValueError, match='пробел внутри научной записи числа'):
        calculate('12 e3+5')


def test_space_after_exponent_marker():
    '''проверка пробела между e и знаком степени'''
    with pytest.raises(ValueError, match='пробел внутри научной записи числа'):
        calculate('1e +3+2')


def test_three_consecutive_operators():
    '''проверка трёх арифметических знаков подряд'''
    with pytest.raises(ValueError, match='неверное расположение операторов'):
        calculate('1---2')


def test_division_by_zero_inside_denominator():
    '''проверка нулевого значения скобки в знаменателе'''
    with pytest.raises(ValueError, match='деление на ноль'):
        calculate('10/(4-2*2)')


def test_division_by_zero_in_nested_bracket():
    '''проверка деления на ноль во вложенном выражении'''
    with pytest.raises(ValueError, match='деление на ноль'):
        calculate('(1+(6/(3-3)))*2')


def test_forbidden_tab_inside_expression():
    '''проверка запрещённой табуляции между токенами'''
    with pytest.raises(ValueError, match='недопустимый символ'):
        calculate('2\t+\t3')
