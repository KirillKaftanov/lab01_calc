'''конвертер величин'''

from toolkit.constants import (
    AVAILABLE_UNITS,
    LENGTH_UNITS,
    MASS_UNITS,
    TEMPERATURE_UNITS,
)
from toolkit.errors import raise_converter_error


def convert(value: str | float, from_unit: str, to_unit: str) -> float:
    '''главная функция конвертера'''

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    value = validate_conversion(value, from_unit, to_unit)

    number = float(value)

    if from_unit in LENGTH_UNITS:
        return convert_with_coefficient(number, from_unit, to_unit, LENGTH_UNITS)

    if from_unit in MASS_UNITS:
        return convert_with_coefficient(number, from_unit, to_unit, MASS_UNITS)

    if from_unit in TEMPERATURE_UNITS:
        return convert_temperature(number, from_unit, to_unit)

    raise_converter_error('неизвестная единица измерения')


def validate_conversion(value: str | float, from_unit: str, to_unit: str) -> str:
    '''проверка входных данных. проверяет: число, единицы, совместимость'''

    check_number(value)

    check_unit(from_unit)
    check_unit(to_unit)

    check_compatibility(from_unit, to_unit)

    return str(value)


def check_number(value: str | float) -> None:
    '''проверка числового значения'''

    try:
        float(value)

    except ValueError:
        raise_converter_error('неверное числовое значение')


def check_unit(unit: str) -> None:
    '''проверка существования единицы'''

    if unit not in AVAILABLE_UNITS:
        raise_converter_error(f'неизвестная единица: {unit}')


def check_compatibility(from_unit: str, to_unit: str) -> None:
    '''проверка совместимости единиц'''

    if (from_unit in LENGTH_UNITS and to_unit in LENGTH_UNITS):
        return

    if (from_unit in MASS_UNITS and to_unit in MASS_UNITS):
        return

    if (from_unit in TEMPERATURE_UNITS and to_unit in TEMPERATURE_UNITS):
        return

    raise_converter_error('несовместимые единицы измерения')


def convert_with_coefficient(value: float, from_unit: str, to_unit: str, units: dict) -> float:
    '''конвертация через базовую единицу'''

    base_value = value * units[from_unit]

    result = base_value / units[to_unit]

    return result


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    '''конвертация температуры'''

    if (from_unit == 'c' and value < -273.15) or (from_unit == 'f' and value < -459.67) or (from_unit == 'k' and value < 0):
        raise_converter_error('температура ниже абсолютного нуля')

    if from_unit == to_unit:
        return value


    celsius = value


    if from_unit == 'f':
        celsius = (value - 32) * 5 / 9

    elif from_unit == 'k':
        celsius = value - 273.15


    if to_unit == 'c':
        result = celsius

    elif to_unit == 'f':
        result = celsius * 9 / 5 + 32

    elif to_unit == 'k':
        result = celsius + 273.15

    else:
        raise_converter_error('неизвестная температурная единица')

    return result
