import unittest
from unittest.mock import patch, Mock
from main import obtener_usuario_callback

class TestObtenerUsuarioCallback(unittest.TestCase):
    def test_successful_user_authentication(self):
        # Mock the request parameters
        username = "testuser"
        password = "testpass"
        headers = {}

        # Mock the database query
        mock_usar_bd = patch('main.usar_bd').start()
        mock_usar_bd.return_value = [('hashed_password',)]

        # Call the callback function
        response = obtener_usuario_callback(username, password, headers)

        # Assert that the response contains the expected token
        expected_token = "mocked_token"
        self.assertEqual(response[0], '{"token": "mocked_token", "status": 200, "message": "Usuario encontrado y token generado."}')
        self.assertEqual(response[1], 200)
        self.assertEqual(response[2], headers)

        # Assert that the correct database query was made
        mock_usar_bd.assert_called_once_with("SELECT * FROM User_ WHERE Username = 'testuser' and Encrypted_Password = 'hashed_testpass'")

    def test_invalid_username(self):
        # Mock the request parameters
        username = ""
        password = "testpass"
        headers = {}

        # Call the callback function
        response = obtener_usuario_callback(username, password, headers)

        # Assert that the response contains the expected error message and status code
        self.assertEqual(response[0], '{"status": 400, "message": "Error: No se ha ingresado un username.", "token": ""}')
        self.assertEqual(response[1], 400)
        self.assertEqual(response[2], headers)

    def test_user_not_found(self):
        # Mock the request parameters
        username = "testuser"
        password = "testpass"
        headers = {}

        # Mock the database query
        mock_usar_bd = patch('main.usar_bd').start()
        mock_usar_bd.return_value = []

        # Call the callback function
        response = obtener_usuario_callback(username, password, headers)

        # Assert that the response contains the expected error message and status code
        self.assertEqual(response[0], '{"status": 404, "message": "Error: Usuario no encontrado.", "token": ""}')
        self.assertEqual(response[1], 404)
        self.assertEqual(response[2], headers)

if __name__ == '__main__':
    unittest.main()