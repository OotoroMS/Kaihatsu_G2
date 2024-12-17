# test_type_check.py
# 引数の型チェックのテスト
import unittest
from type_check import get_argument_value, check_argument_type, validate_argument_types

class TestTypeCheck(unittest.TestCase):

    # get_argument_value のテスト
    def test_get_argument_value_with_kwargs(self):
        args = (1, 2)
        kwargs = {'a': 10}
        result = get_argument_value('a', args, kwargs, 0)
        self.assertEqual(result, 10)

    def test_get_argument_value_with_position(self):
        args = (1, 2)
        kwargs = {}
        result = get_argument_value('a', args, kwargs, 0)
        self.assertEqual(result, 1)

    # check_argument_type のテスト
    def test_check_argument_type_correct_type(self):
        check_argument_type('a', 10, int)

    def test_check_argument_type_wrong_type(self):
        with self.assertRaises(TypeError):
            check_argument_type('a', 'string', int)

    def test_check_argument_type_list(self):
        check_argument_type('a', [1, 2, 3], list)

    def test_check_argument_type_list_item(self):
        with self.assertRaises(TypeError):
            check_argument_type('a[0]', 'string', int)

    # validate_argument_types のテスト
    def test_validate_argument_types(self):
        args = (1, 2)
        kwargs = {'a': 10}
        types = {'a': int, 0: int}
        try:
            validate_argument_types(args, kwargs, types)
        except TypeError:
            self.fail("validate_argument_types raised TypeError unexpectedly!")

    def test_validate_argument_types_invalid(self):
        args = (1, 2)
        kwargs = {'a': 'string'}
        types = {'a': int}
        with self.assertRaises(TypeError):
            validate_argument_types(args, kwargs, types)

if __name__ == '__main__':
    unittest.main()
