import itertools
import os
from typing import List, Optional
from unittest import mock
import io
import re
import ast


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

def check(data) -> bool:
    """
    Функция строит абстрактное синтаксическое дерево
    и выполняет проверку имен пользовательских типов
    :param data: список строк из файла
    :return: True - дерево составлено и имена удовлетворяют правилам,
             False - либо ошибки при составлении дерева, либо есть несоответствие названия правилам.
    """
    arr_error = []
    data = ''.join(data)

    try:
        items = ast.parse(data)
    except SyntaxError:
        return False

    def check_name(node: ast.Module, is_capital: bool=False) -> None:
        """
        Функция обходит синтаксическое дерево и проверяет название каждого узла
        :param node: узел дерева
        :param is_capital: с заглавной или строчной буквы должно начинаться название узла
        """

        if 'name' in dir(node):
            if not isinstance(node, ast.ClassDef):
                if is_capital and not re.match(r'[A-Z]', node.name):
                    arr_error.append(False)
                elif not is_capital and not re.match(r'[a-z]', node.name):
                    arr_error.append(False)
                is_capital = True
            else:
                if not re.match(r'[A-Z]', node.name):
                    arr_error.append(False)
                is_capital = False
        else:
            # Если нет дочерних узлов - передаем управление
            return

        # Применяем функцию check_name ко всем дочерним элементам (древовидная рекурсия)
        list(map(check_name, node.body, itertools.repeat(is_capital)))

    for item in items.body:
        check_name(item, True)
    return len(arr_error) == 0

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
