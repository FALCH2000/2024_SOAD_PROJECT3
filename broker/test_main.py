import json
import unittest
from unittest.mock import MagicMock

from main import broker

class TestBroker(unittest.TestCase):
    def test_broker_creates_reserva(self):
        request = MagicMock()
        request.method = "POST"
        request.path = "/"
        request.get_json.return_value = {
            "data": {
                "method": "crear-reserva"
            }
        }
        expected_response = ("Creando reserva...", 200, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        })

        response = broker(request)

        self.assertEqual(response, expected_response)

if __name__ == "__main__":
    unittest.main()