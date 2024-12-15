import unittest
import tempfile
import os
from main import parse_config  # Импортируем вашу функцию для тестирования
import toml


class TestConfigParser(unittest.TestCase):
    def test_single_number(self):
        config = "var a := 42"
        expected = {"a": 42}
        self.assertEqual(parse_config(config), expected)

    def test_array(self):
        config = "var array := (1, 2, 3, 4)"
        expected = {"array": [1, 2, 3, 4]}
        self.assertEqual(parse_config(config), expected)

    def test_postfix_expression(self):
        config = """
        var a := 3
        var b := 4
        var c := ${a b +}
        """
        expected = {"a": 3, "b": 4, "c": 7}
        self.assertEqual(parse_config(config), expected)

    def test_nested_array(self):
        config = """
        var a := (1, 2, (3, 4))
        """
        with self.assertRaises(ValueError):  # Наша реализация не поддерживает вложенные массивы
            parse_config(config)

    def test_postfix_with_min(self):
        config = """
        var a := 5
        var b := 10
        var c := ${a b min()}
        """
        expected = {"a": 5, "b": 10, "c": 5}
        self.assertEqual(parse_config(config), expected)

    def test_postfix_with_len(self):
        config = """
        var array := (1, 2, 3, 4, 5)
        var length := ${array len()}
        """
        expected = {"array": [1, 2, 3, 4, 5], "length": 5}
        self.assertEqual(parse_config(config), expected)

    def test_syntax_error(self):
        config = "var 1invalid := 42"
        with self.assertRaises(ValueError):
            parse_config(config)

    def test_empty_array(self):
        config = "var empty := ()"
        expected = {"empty": []}
        self.assertEqual(parse_config(config), expected)

    def test_invalid_expression(self):
        config = """
        var a := 5
        var b := ${a 2 + +}
        """
        with self.assertRaises(ValueError):
            parse_config(config)

    def test_subject_area_examples(self):
        # Пример из области физики
        physics_config = """
        var speed := 300
        var time := 2
        var distance := ${speed time *}
        """
        expected_physics = {"speed": 300, "time": 2, "distance": 600}
        self.assertEqual(parse_config(physics_config), expected_physics)

        # Пример из области экономики
        economics_config = """
        var price := 100
        var quantity := 50
        var revenue := ${price quantity *}
        """
        expected_economics = {"price": 100, "quantity": 50, "revenue": 5000}
        self.assertEqual(parse_config(economics_config), expected_economics)

        # Пример из области математики
        math_config = """
        var array := (1, 2, 3, 4, 5)
        var sum := ${1 2 3 4 5 + + + +}
        """
        expected_math = {"array": [1, 2, 3, 4, 5], "sum": 15}
        self.assertEqual(parse_config(math_config), expected_math)


if __name__ == "__main__":
    unittest.main()
