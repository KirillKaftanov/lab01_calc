'''калькулятор выражений'''

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

from toolkit.constants import MAX_BRACKET_DEPTH
from toolkit.errors import raise_error

getcontext().prec = 25
getcontext().rounding = ROUND_HALF_UP

def check_symbols(expression: str) -> None:
    '''проверяет допустимые символы'''

    allowed = '0123456789.+-*/()eE '

    for symbol in expression:

        if symbol not in allowed:
            raise_error(f'недопустимый символ: {symbol}')

def check_spaces_between_numbers(expression: str) -> None:
    '''проверяет отсутствие пробелов внутри чисел'''

    index = 0

    while index < len(expression):

        if expression[index] != ' ':
            index = index + 1
            continue

        space_start = index

        while index < len(expression) and expression[index] == ' ':
            index = index + 1

        if space_start == 0 or index == len(expression):
            continue

        left = expression[space_start - 1]
        right = expression[index]

        if left.isdigit() and right.isdigit():
            raise_error('пробел внутри числа')

        if left.isdigit() and right == '.':
            raise_error('пробел внутри числа')

        if left == '.' and right.isdigit():
            raise_error('пробел внутри числа')

        if left.isdigit() and right in 'eE':
            raise_error('пробел внутри научной записи числа')

        if left in 'eE' and (right.isdigit() or right in '+-'):
            raise_error('пробел внутри научной записи числа')

        if left in '+-' and space_start >= 2 and expression[space_start - 2] in 'eE' and right.isdigit():
            raise_error('пробел внутри научной записи числа')

def read_right_operand(expression: str, start_index: int) -> tuple[Decimal, int]:
    '''считывает число, включая знак и научную запись'''

    index = start_index
    digits_count = 0

    # знак самого числа
    if index < len(expression) and expression[index] in '+-':
        index = index + 1

    # целая часть
    while index < len(expression) and expression[index].isdigit():
        index = index + 1
        digits_count = digits_count + 1

    # дробная часть
    if index < len(expression) and expression[index] == '.':

        index = index + 1

        while index < len(expression) and expression[index].isdigit():
            index = index + 1
            digits_count = digits_count + 1

    if digits_count == 0:
        raise_error('неверное числовое значение')

    # научная запись
    if index < len(expression) and expression[index] in 'eE':

        index = index + 1

        # знак степени
        if index < len(expression) and expression[index] in '+-':
            index = index + 1

        exponent_start = index

        # цифры степени
        while index < len(expression) and expression[index].isdigit():
            index = index + 1

        if index == exponent_start:
            raise_error('неверная научная запись')

    #не допускаем продолжение некорректного числа
    if index < len(expression) and expression[index] in '.eE':
        raise_error('неверное числовое значение')

    number_text = expression[start_index:index]

    try:
        number = Decimal(number_text)

    except InvalidOperation:
        raise_error('неверное числовое значение')

    return number, index

def find_last_add_sub_operator(expression: str) -> int:
    '''находит последний бинарный + или -, игнорируя знаки чисел и степеней'''

    last_operator_index = -1

    for index, symbol in enumerate(expression):

        if symbol not in '+-':
            continue

        if index == 0:
            continue

        previous_symbol = expression[index - 1]

        if previous_symbol in 'eE+-*/(':
            continue

        last_operator_index = index

    if last_operator_index == -1 and expression[0] in '+-':
        last_operator_index = 0

    return last_operator_index

def check_numbers(expression: str) -> None:
    '''проверяет корректность чисел, включая научную запись'''

    index = 0

    while index < len(expression):

        current_symbol = expression[index]

        if current_symbol == ' ':
            index = index + 1
            continue

        if current_symbol in '+-*/()':
            index = index + 1
            continue

        _, index = read_right_operand(expression, index)


def check_brackets(expression: str) -> None:
    '''проверяет корректность скобок'''

    counter = 0

    if '(/' in expression or '(*' in expression or '*)' in expression or '/)' in expression:
        raise_error('пропущен операнд внутри скобки')

    for symbol in expression:

        if symbol == '(':
            counter = counter + 1

            if counter > MAX_BRACKET_DEPTH:
                raise_error(f'превышена максимальная глубина вложенности скобок {MAX_BRACKET_DEPTH}')

        elif symbol == ')':
            counter = counter - 1

            if counter < 0:
                raise_error('неверная последовательность скобок')

    for index in range(len(expression) - 1):

        current_symbol = expression[index]
        next_symbol = expression[index + 1]

        if current_symbol in '0123456789.eE' and next_symbol == '(':
            raise_error('пропущен оператор перед скобкой')

        if current_symbol == ')' and next_symbol in '0123456789.eE(':
            raise_error('пропущен оператор после скобки')

    if counter != 0:
        raise_error('количество открывающих и закрывающих скобок не совпадает')

def check_operators(expression: str) -> None:
    '''проверяет расположение операторов'''

    operators = '+-*/'

    for index in range(len(expression) - 1):

        current_symbol = expression[index]
        next_symbol = expression[index + 1]

        if current_symbol in operators and next_symbol in '*/':
            raise_error('два бинарных оператора подряд')

    for index in range(len(expression) - 2):

            current_symbol = expression[index]
            second_symbol = expression[index + 1]
            third_symbol = expression[index + 2]

            if current_symbol in operators and second_symbol in operators and third_symbol in operators:
                raise_error('неверное расположение операторов')

def check_missing_operand(expression: str) -> None:
    '''проверяет наличие операндов около операторов'''

    if expression[0] in '*/':
        raise_error('пропущен операнд')

    if expression[-1] in '+-*/':
        raise_error('пропущен операнд')

    if '+)' in expression or '-)' in expression or '()' in expression:
        raise_error('пропущен операнд')

def remove_spaces(expression: str) -> str:
    '''удаляет пробелы между элементами выражения'''

    return expression.replace(' ', '')

def normalize_unary_plus_minus(expression: str) -> str:
    '''удаляет унарные плюс и минус из выражения и упрощает соседние знаки'''

    if expression.startswith('+'):
        expression = expression.removeprefix('+')

    expression = expression.replace('(+', '(')
    expression = expression.replace('++', '+')
    expression = expression.replace('-+', '-')
    expression = expression.replace('+-', '-')
    expression = expression.replace('*+', '*')
    expression = expression.replace('/+', '/')
    expression = expression.replace('--', '+')

    return expression

def validate_expression(expression: str) -> str:
    '''проверяет математическое выражение'''

    if not expression.strip():
        raise_error('пустое выражение')

    expression = expression.strip()

    check_symbols(expression)
    check_spaces_between_numbers(expression)
    check_numbers(expression)
    expression = remove_spaces(expression)
    check_brackets(expression)
    check_operators(expression)
    check_missing_operand(expression)

    expression = normalize_unary_plus_minus(expression)

    return expression

def extract_parenthesized_expression(expression: str) -> str:
    '''собирает скобку для последующего вычисления'''

    parenthesized_expression = ''
    open_parentheses_count = 0
    close_parentheses_count = 0
    index = 0

    while (open_parentheses_count != close_parentheses_count or close_parentheses_count == 0) and index < len(expression):

        current_symbol = expression[index]
        parenthesized_expression = parenthesized_expression+current_symbol

        if current_symbol == '(':
            open_parentheses_count = open_parentheses_count+1

        elif current_symbol == ')':
            close_parentheses_count = close_parentheses_count+1

        index = index+1

    return parenthesized_expression

def evaluate_add_sub(expression: str) -> Decimal:
    '''вычисляет выражение, содержащее только числа, + и -'''

    if not expression:
        raise_error('пустое выражение')

    index = 0
    result = Decimal(0)
    first_number = True

    while index < len(expression):

        sign = 1
        signs_count = 0

        while index < len(expression) and expression[index] in '+-':

            if expression[index] == '-':
                sign = -sign

            signs_count = signs_count + 1

            if signs_count > 2:
                raise_error('неверное расположение операторов')

            index = index + 1

        number, index = read_right_operand(expression, index)

        if sign == -1:
            number = number.copy_negate()

        if first_number:
            result = number
            first_number = False

        else:
            result = result + number

        if index < len(expression) and expression[index] not in '+-':
            raise_error('неверное расположение операторов')

    return result

def evaluate_parenthesized_expression(expression: str) -> Decimal:
    '''вычисляет скобку'''

    index = 0
    parenthesized_expression = ''

    while index < len(expression):

        current_symbol = expression[index]

        if current_symbol == '(':

            index = index + 1

            while index < len(expression):

                current_symbol = expression[index]

                if current_symbol != ')':

                    if current_symbol == '(':

                        parenthesized_expression = parenthesized_expression + str(evaluate_parenthesized_expression(extract_parenthesized_expression(expression[index:])))
                        index = index + len(extract_parenthesized_expression(expression[index:]))

                    elif current_symbol == '*' or current_symbol == '/':

                        operator_index = find_last_add_sub_operator(parenthesized_expression)
                        left_operand = Decimal(parenthesized_expression[operator_index + 1:])
                        operand_start = index + 1
                        bracket_sign = Decimal(1)

                        if operand_start + 1 < len(expression) and expression[operand_start] in '+-' and expression[operand_start + 1] == '(':

                            if expression[operand_start] == '-':
                                bracket_sign = Decimal(-1)

                            operand_start = operand_start + 1

                        if (operand_start < len(expression) and expression[operand_start] == '('):

                            bracket_expression = extract_parenthesized_expression(expression[operand_start:])
                            right_operand = evaluate_parenthesized_expression(bracket_expression)

                            if bracket_sign == -1:
                                right_operand = right_operand.copy_negate()

                            index = operand_start + len(bracket_expression)

                        else:

                            right_operand, index = read_right_operand(expression, index + 1,)

                        if current_symbol == '*':

                            operation_result = left_operand * right_operand

                        else:

                            if right_operand == 0:
                                raise_error('деление на ноль')

                            operation_result = left_operand / right_operand

                        parenthesized_expression = (parenthesized_expression[:operator_index + 1] + str(operation_result))

                    else:
                        parenthesized_expression = parenthesized_expression + current_symbol
                        index = index + 1

                else:
                    index = index + 1
                    break

    if parenthesized_expression[:2] == '--':
        parenthesized_expression = parenthesized_expression.replace('--', '', 1)

    parenthesized_expression = parenthesized_expression.replace('+-', '-')
    parenthesized_expression = parenthesized_expression.replace('--', '+')
    parenthesized_expression = parenthesized_expression.replace('-+', '-')

    return evaluate_add_sub(parenthesized_expression)

def calculate(expression: str) -> int | Decimal:
    '''выполняет вычисление заданного выражения'''

    expression = validate_expression(expression)
    index = 0
    processed_expression = ''

    while index < len(expression):

        current_symbol = expression[index]

        if current_symbol == '(':
            processed_expression = processed_expression + str(evaluate_parenthesized_expression(extract_parenthesized_expression(expression[index:])))
            index = index + len(extract_parenthesized_expression(expression[index:]))

        elif current_symbol == '*' or current_symbol == '/':

            operator_index = find_last_add_sub_operator(processed_expression)
            left_operand = Decimal(processed_expression[operator_index + 1:])
            operand_start = index + 1
            bracket_sign = Decimal(1)

            if operand_start + 1 < len(expression) and expression[operand_start] in '+-' and expression[operand_start + 1] == '(':

                if expression[operand_start] == '-':
                    bracket_sign = Decimal(-1)

                operand_start = operand_start + 1

            if expression[operand_start] == '(':

                bracket_expression = extract_parenthesized_expression(expression[operand_start:])
                right_operand = evaluate_parenthesized_expression(bracket_expression)

                if bracket_sign == -1:
                    right_operand = right_operand.copy_negate()

                index = operand_start + len(bracket_expression)

            else:

                right_operand, index = read_right_operand(expression, index + 1)

            if current_symbol == '*':

                operation_result = left_operand * right_operand

            else:

                if right_operand == 0:
                    raise_error('деление на ноль')

                operation_result = left_operand / right_operand

            processed_expression = (processed_expression[:operator_index + 1] + str(operation_result))

        else:
            processed_expression = processed_expression + current_symbol
            index = index + 1

    if processed_expression[:2] == '--':
        processed_expression=processed_expression.replace('--', '', 1)

    processed_expression = processed_expression.replace('+-', '-')
    processed_expression = processed_expression.replace('--', '+')
    processed_expression = processed_expression.replace('-+', '-')

    result = evaluate_add_sub(processed_expression)

    if result == 0:
        return 0

    if result == result.to_integral_value():
        return int(result)

    return result
