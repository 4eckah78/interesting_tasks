import unittest
from solution import strict


@strict
def bool_func(a: bool) -> bool:
    return a


@strict
def int_func(a: int) -> int:
    return a


@strict
def float_func(a: float) -> float:
    return a


@strict
def str_func(a: str) -> str:
    return a


@strict
def multi_func(a: int, b: float, c: bool, d: str) -> str:
    return f"{a} {b} {c} {d}"


@strict
def pos_keyword_func(a: int, b: int) -> str:
    return f"{a} {b}"


class TestStrictDecorator(unittest.TestCase):
    def test_bool(self):
        self.assertEqual(bool_func(True), True)
        self.assertEqual(bool_func(False), False)

        with self.assertRaises(TypeError):
            bool_func(1)
        with self.assertRaises(TypeError):
            bool_func("True")

    def test_int(self):
        self.assertEqual(int_func(42), 42)
        self.assertEqual(int_func(0), 0)

        with self.assertRaises(TypeError):
            int_func(True)
        with self.assertRaises(TypeError):
            int_func(3.14)
        with self.assertRaises(TypeError):
            int_func("42")

    def test_float(self):
        self.assertEqual(float_func(3.14), 3.14)
        self.assertEqual(float_func(0.0), 0.0)

        with self.assertRaises(TypeError):
            float_func(42)
        with self.assertRaises(TypeError):
            float_func(True)
        with self.assertRaises(TypeError):
            float_func("3.14")

    def test_str(self):
        self.assertEqual(str_func("hello"), "hello")
        self.assertEqual(str_func("42"), "42")

        with self.assertRaises(TypeError):
            str_func(42)
        with self.assertRaises(TypeError):
            str_func(True)
        with self.assertRaises(TypeError):
            str_func(3.14)

    def test_multi_func(self):
        self.assertEqual(multi_func(1, 2.0, True, "test"), "1 2.0 True test")

        with self.assertRaises(TypeError):
            multi_func(True, 2.0, True, "test")
        with self.assertRaises(TypeError):
            multi_func(1, 2, True, "test")
        with self.assertRaises(TypeError):
            multi_func(1, 2.0, 1, "test")
        with self.assertRaises(TypeError):
            multi_func(1, 2.0, True, 42)

    def test_pos_keyword_func(self):
        self.assertEqual(pos_keyword_func(a=1, b=2), "1 2")
        self.assertEqual(pos_keyword_func(1, b=2), "1 2")

        with self.assertRaises(TypeError):
            multi_func(1, b=21.0)
        with self.assertRaises(TypeError):
            multi_func(a="sd", b=2)
        with self.assertRaises(TypeError):
            multi_func(1, 2.0)
        with self.assertRaises(TypeError):
            multi_func(1, True)

    def test_int_bool(self):
        self.assertEqual(pos_keyword_func(a=1, b=2), "1 2")

        with self.assertRaises(TypeError):
            multi_func(1, False)
        with self.assertRaises(TypeError):
            multi_func(True, 2)


if __name__ == "__main__":
    unittest.main()
