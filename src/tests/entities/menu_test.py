import unittest
from datetime import datetime
from entities.menu import Menu

class TestMenu(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.date = datetime.now()

    def setUp(self):
        self.menu = Menu(list(range(7)), self.date)

    def test_menu_string_representation(self):
        self.assertEqual(str(self.menu), "Menu([0, 1, 2, 3, 4, 5, 6], " + str(self.date) + ")")

    def test_menu_raises_value_error_if_less_than_seven_meals(self):
        with self.assertRaises(ValueError) as error:
            menu = Menu(list(range(6)), self.date)

        self.assertEqual(str(error.exception), "Seven meals required!")
