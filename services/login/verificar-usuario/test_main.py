import unittest
from unittest.mock import patch, Mock
from main import verificar_usuario_callback

class TestVerificarUsuarioCallback(unittest.TestCase):
    def test_valid_token(self):
        # Mock the request arguments
        request_args = {'token': 'valid_token'}

        # Mock the database query
        mock_usar_bd = patch('main.usar_bd').start()
        mock_usar_bd.return_value = [('hashed_password',)]

        # Call the callback function
        response = verificar_usuario_callback(request_args)

        # Assert that the response contains the expected status code and message
        expected_response = '{"status": 200, "message": "Usuario encontrado."}'
        self.assertEqual(response, expected_response)

        # Assert that the correct database query was made
        mock_usar_bd.assert_called_once_with("SELECT * FROM User_ WHERE Username = '' AND Encrypted_Password = 'hashed_password'")

    def test_invalid_token(self):
        # Mock the request arguments
        request_args = {'token': 'invalid_token'}

        # Call the callback function
        response = verificar_usuario_callback(request_args)

        # Assert that the response contains the expected status code and message
        expected_response = '{"status": 401, "message": "Error: EL TOKEN no es valido!"}'
        self.assertEqual(response, expected_response)

    def test_missing_username_or_password(self):
        # Mock the request arguments
        request_args = {'token': 'valid_token'}

        # Call the callback function
        response = verificar_usuario_callback(request_args)

        # Assert that the response contains the expected status code and message
        expected_response = '{"status": 400, "message": "Error: No se ha ingresado un username o password."}'
        self.assertEqual(response, expected_response)

    def test_user_not_found(self):
        # Mock the request arguments
        request_args = {'token': 'valid_token'}

        # Mock the database query
        mock_usar_bd = patch('main.usar_bd').start()
        mock_usar_bd.return_value = []

        # Call the callback function
        response = verificar_usuario_callback(request_args)

        # Assert that the response contains the expected status code and message
        expected_response = '{"status": 404, "message": "Error: Usuario no existe o la contrasena es incorrecta."}'
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()