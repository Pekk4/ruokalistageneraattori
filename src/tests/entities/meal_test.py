import unittest
from entities.meal import Meal

class TestMeal(unittest.TestCase):

    def setUp(self):
        self.meal = Meal("Uunimakkara")

    def test_meal_string_representation(self):
        self.assertEqual(str(self.meal), "Uunimakkara")
