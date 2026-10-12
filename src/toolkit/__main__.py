'''командный интерфейс калькулятора и конвертера'''

import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert

АВТОР = 'Кирилл Кафтанов'

def create_parser() -> argparse.ArgumentParser:
    '''создать описание командной строки программы'''

    parser = argparse.ArgumentParser(prog='python -m toolkit',usage=argparse.SUPPRESS,
        description=(
            'Консольный калькулятор и конвертер величин.\n\n'
            f'Автор: {АВТОР}\n\n'
            'Программа предоставляет два инструмента:\n\n'
            '1. Калькулятор\n'
            'Выполняет арифметические вычисления.\n\n'
            'Функциональные возможности:\n'
            '• поддержка целых чисел;\n'
            '• поддержка вещественных чисел;\n'
            '• сложение +;\n'
            '• вычитание -;\n'
            '• умножение *;\n'
            '• деление /;\n'
            '• поддержка унарного + и - перед числом;\n'
            '• поддержка научной записи числа;\n'
            '• игнорирование пробелов между элементами выражения;\n'
            '• соблюдение приоритета умножения и деления\n'
            '  над сложением и вычитанием.\n\n'
            'Калькулятор работает с математическими выражениями,\n'
            'состоящими из чисел и поддерживаемых операторов.\n\n'
            '2. Конвертер величин\n'
            'Переводит значения между единицами измерения:\n'
            'длина: миллиметры, сантиметры, метры, километры;\n'
            'масса: граммы, килограммы;\n'
            'температура: Цельсий, Фаренгейт, Кельвин.'
        ),
        epilog=(
            'Примеры команд:\n\n'
            'Калькулятор:\n'
            '  python -m toolkit calc \'2 + 3 * 4\'\n\n'
            'Конвертер:\n'
            '  python -m toolkit convert 100 --from cm --to m'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    commands = parser.add_subparsers(title='доступные команды', dest='command', required=True)

    calculator = commands.add_parser('calc', help='вычисление математического выражения')

    calculator.add_argument('expression', help='математическое выражение для вычисления')

    converter = commands.add_parser('convert', help='перевод значения из одной единицы измерения в другую')

    converter.add_argument('value', help='числовое значение для преобразования')

    converter.add_argument('--from', dest='from_unit', required=True, help='исходная единица измерения')

    converter.add_argument('--to', dest='to_unit', required=True, help='целевая единица измерения',)

    return parser


def main() -> int:
    '''запуск командного интерфейса'''

    parser = create_parser()

    arguments = sys.argv[1:]

    if (
        len(arguments) >= 2
        and arguments[0] == 'calc'
        and arguments[1].startswith('-')
        and arguments[1] not in ('-h', '--help', '--')
    ):
        arguments.insert(1, '--')

    args = parser.parse_args(arguments)

    if args.command == 'calc':

        try:
            result = calculate(args.expression)

        except ValueError as error:
            print(f'ошибка: {error}', file=sys.stderr)
            return 2

        print(result)
        return 0

    elif args.command == 'convert':

        try:
            conversion_result = convert(args.value, args.from_unit, args.to_unit)

        except ValueError as error:
            print(f'ошибка: {error}', file=sys.stderr)
            return 2

        print(conversion_result)
        return 0

    return 2


if __name__ == '__main__':
    raise SystemExit(main())
