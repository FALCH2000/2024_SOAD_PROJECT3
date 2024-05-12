import unittest
from unittest.mock import MagicMock
from main import obtener_recomendacion_callback

class TestObtenerRecomendacionCallback(unittest.TestCase):
    def test_obtener_recomendacion_callback_with_quantity_1(self):
        recomendacion = [1]
        quantity = 1
        expected_response = {
            "data": {
                "Main_Dish": "Main Dish 1",
                "Drink": "Drink 1",
                "Dessert": "Dessert 1"
            }
        }

        response = obtener_recomendacion_callback(recomendacion, quantity)

        self.assertEqual(response, expected_response)

    def test_obtener_recomendacion_callback_with_quantity_2(self):
        recomendacion = [1, 2]
        quantity = 2
        expected_response = {
            "data": {
                "Main_Dish": "Main Dish 1",
                "Drink": "Drink 2",
                "Dessert": "Dessert 1"
            }
        }

        response = obtener_recomendacion_callback(recomendacion, quantity)

        self.assertEqual(response, expected_response)

if __name__ == "__main__":
    unittest.main()