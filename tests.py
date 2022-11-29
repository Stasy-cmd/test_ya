import unittest
from function import open_file, check, test_eval


class TestForFunction(unittest.TestCase):
    """
    Тесты к файлу function.py
    """
    def test_open_file_correct(self):
        """
        Проверка работы функции 'open_file' при корректном файле:
        файл существует и в нем есть данные
        """
        assert len(open_file('data/foo_1.py')) > 0

    def test_open_file_not_exist(self):
        """
        Проверка работы функции 'open_file' при отсутствии файла
        """
        assert open_file('foo_1.py') is None

    def test_open_file_empty(self):
        """
        Проверка работы функции 'open_file' при пустом файле
        """
        assert len(open_file('data/empty.py')) == 0

    def test_check_class_correct(self):
        """
        Проверка работы функции 'check' при корректном описании класса
        """
        str_test = ['class Triangle():\n',
                   '    def method_one(self): \n',
                   '        pass \n',
                   '    def method_two(self): \n',
                   '        pass']
        assert check(str_test) is True

    def test_check_class_lowercase_class(self):
        """
        Проверка работы функции 'check': название класса с маленькой буквы
        """
        str_test = ['class triangle():\n',
                   '    def method_one(self): \n',
                   '        pass \n',
                   '    def method_two(self): \n',
                   '        pass']
        assert check(str_test) is False

    def test_check_class_capital_def(self):
        """
        Проверка работы функции 'check': название метода класса с заглавной буквы
        """
        str_test = ['class Triangle():\n',
                   '    def Method_one(self): \n',
                   '        pass \n',
                   '    def method_two(self): \n',
                   '        pass']
        assert check(str_test) is False

    def test_check_class_symbol_def(self):
        """
        Проверка работы функции 'check': название метода с символа
        """
        str_test = ['class Triangle():\n',
                   '    def _method_one(self): \n',
                   '        pass \n',
                   '    def method_two(self): \n',
                   '        pass']
        assert check(str_test) is False

    def test_check_def_correct(self):
        """
        Проверка работы функции 'check' при корректном описании функции
        """
        str_test = ['def CircleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")']
        assert check(str_test) is True

    def test_check_def_lowercase(self):
        """
        Проверка работы функции 'check': название функции с маленькой буквы
        """
        str_test = ['def circleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")']
        assert check(str_test) is False

    def test_check_comment(self):
        """
        Проверка работы функции 'check': использование комментариев
        """
        str_test = ['# комментарий']
        assert check(str_test) is True

    def test_check_call_def_correct(self):
        """
        Проверка работы функции 'check': вызов функции внутри файла
        """
        str_test = ['def CircleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")\n',
                    'CircleFactory()']
        assert check(str_test) is True

    def test_check_call_def_incorrect(self):
        """
        Проверка работы функции 'check': неправильный вызове функции внутри файла
        """
        str_test = ['def CircleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")\n',
                    'CircleFactory1()']
        assert check(str_test) is False

    def test_check_call_print(self):
        """
        Проверка работы функции 'check': вызов функции print() внутри файла
        """
        str_test = ['def CircleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")\n',
                    'print()']
        assert check(str_test) is True


    def test_check_eval_correct(self):
        """
        Проверка работы функции 'test_eval'
        (в файле написан код, который выполняется, и результат совпадает с ожидаемым)
        """
        str_test = ['def CircleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")\n',
                    'CircleFactory()']
        assert test_eval(str_test, 'hello\nworld\n') is True

    def test_check_eval_incorrect(self):
        """
        Проверка работы функции 'test_eval'
        (в файле написан код, который выполняется, но результат не совпадает с ожидаемым)
        """
        str_test = ['def CircleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")\n',
                    'CircleFactory1()']
        assert test_eval(str_test, 'hello\nworld\n') is False

    def test_check_eval_incorrect_not_fulfilled(self):
        """
        Проверка работы функции 'test_eval'
        (в файле написан код, который не выполняется)
        """
        str_test = ['def CircleFactory():\n',
                    '    print("hello")\n',
                    '    print("world")\n',
                    'CircleFactory1()']
        assert test_eval(str_test, 'hello\nworld\n') is False
