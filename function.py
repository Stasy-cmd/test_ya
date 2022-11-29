import os
from typing import List, Optional
from unittest import mock
import io
import re


def open_file(filename: str) -> Optional[List[str]]:
    """
    Функция открывает файл и считывает все строчки
    :param filename: имя файла
    :return: возвращает список строк из файла
    """
    if not os.path.exists(filename):
        return None

    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()


def check(lines: List[str]) -> bool:
    """
     Функция проверяет на имена классов и функций в файле студента.
    :param lines: список строк из файла студента
    :return: True в случае корректного файла, False - в случае ошибки.
    """

    is_class = False
    is_done = True
    set_def = {'print', 'input'}

    for line in lines:
        if 'class' in line:
            if re.match(r'class\s[A-Z]', line):
                is_class = True
            else:
                is_done = False

        elif 'def' in line:
            if re.match(r'def\s[A-Z]', line):
                is_class = False
                name_func = re.split(r'def\s+', line.strip(':\n').split('(', maxsplit=1)[0])[1]
                set_def.add(name_func)
            elif is_class and re.match(r'\s{4}def\s[a-z]', line):
                continue
            else:
                is_done = False

        # если пустая строчка или комментарий
        elif not line.strip('\n').strip(' ') or re.match('#', line):
            continue

        # если конструкция вне функции и вызывается функция, которая раньше была не определена
        elif not re.match(r'\s{4}', line) or (not re.match(r'\s{8}', line) and is_class):
            if line.strip('\n').split('(', maxsplit=1)[0] not in set_def:
                is_done = False

        if not is_done:
            break

    return is_done


def test_eval(data: List[str], out_result: str) -> bool:
    """
    Функция проверяет, что вывод студента совпадает с ожидаемым результатом
    :param data: список команд из файла
    :param out_result: ожидаемый вывод
    :return: True - корректный вывод, False - ожидаемый результат не совпадает с действительным.
    """
    with mock.patch('sys.stdout', new=io.StringIO()) as func_stdout:
        try:
            exec(''.join(data))
            return func_stdout.getvalue() == out_result
        except:
            return False


def start(filename: str, expected_result: str) -> int:
    """
    Функция-агрегатор для проверки файла студентов
    :param filename: название файла
    :param expected_result: строка с ожидаемым результатом
    :return: 0 - корректный код, 1 - ошибки во время выполнения или в синтаксисе
    """
    data = open_file(filename)
    if not data:
        return 1
    result_check = check(data)
    if not result_check:
        return 1
    result_eval = test_eval(data, expected_result)
    if not result_eval:
        return 1
    return 0
