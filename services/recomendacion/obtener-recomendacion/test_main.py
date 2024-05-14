import unittest
from unittest.mock import MagicMock
import json
from main import obtener_recomendacion_callback

class TestObtenerRecomendacionCallback(unittest.TestCase):
    def test_obtener_recomendacion_callback_with_quantity_1(self):
        recomendacion = [1]
        quantity = 1

        response = obtener_recomendacion_callback(recomendacion, quantity)
        response = json.loads(response)
        self.assertIsNotNone(response["data"]["Main_Dish"])
        self.assertIsNotNone(response["data"]["Drink"])
        self.assertIsNotNone(response["data"]["Dessert"])

    def test_obtener_recomendacion_callback_with_quantity_2(self):
        recomendacion = [1, 2]
        quantity = 2

        response = obtener_recomendacion_callback(recomendacion, quantity)

        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()