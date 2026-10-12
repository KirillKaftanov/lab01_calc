'''ошибки консольного калькулятора'''

from typing import NoReturn


def raise_error(message: str) -> NoReturn:
    '''останавливает выполнение программы и сообщает пользователю причину ошибки'''

    raise ValueError(message)

def raise_converter_error(message: str) -> NoReturn:
    '''вызывает ошибку конвертера и сообщает пользователю ее причину'''

    raise ValueError(message)
