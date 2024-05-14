import unittest
from unittest.mock import patch, Mock
from main import verificar_usuario_callback

class TestVerificarUsuarioCallback(unittest.TestCase):
    def test_valid_token(self):
        # Mock the request arguments
        request_args = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluMSIsInBhc3N3b3JkIjoiYWRtaW4xIiwiZXhwIjo5OTk5OTk5OTk5fQ.C4eJAyZrLOLwkVQE2T1vK3u1eMp4fCwjGFDqy1MXt9M'

        # Mock the database query
        mock_usar_bd = patch('main.usar_bd').start()
        mock_usar_bd.return_value = [('hashed_password',)]

        # Call the callback function
        response = verificar_usuario_callback(request_args,{})

        # Assert that the response contains the expected status code and message
        expected_response = ('{"status": 200, "message": "Usuario encontrado."}',200,{})
        self.assertEqual(response, expected_response)

    def test_invalid_token(self):
        # Mock the request arguments
        request_args = 'invalid_token'

        # Call the callback function
        response = verificar_usuario_callback(request_args,{})

        # Assert that the response contains the expected status code and message
        expected_response = ('{"status": 401, "message": "Error: EL TOKEN no es valido!"}',401,{})
        self.assertEqual(response, expected_response)

    def test_missing_username_or_password(self):
        # Mock the request arguments
        request_args = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluMSIsImV4cCI6OTk5OTk5OTk5OX0.tNWRcTrAme-NhgiFSEUbKH1d-iO2dFqCjc2MH4od7NM"

        # Call the callback function
        response = verificar_usuario_callback(request_args,{})

        # Assert that the response contains the expected status code and message
        
        expected_response = ('{"status": 500, "message": "Error: \'password\'"}',500,{})
        self.assertEqual(response, expected_response)

    def test_user_not_found(self):
        # Mock the request arguments
        request_args = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluMSIsInBhc3N3b3JkIjoiICIsImV4cCI6OTk5OTk5OTk5OX0.cNnUyzhJDnBphL3mFFWvaNIlOmSlwMPJJFAe8-PUhLI"

        # Mock the database query
        mock_usar_bd = patch('main.usar_bd').start()
        mock_usar_bd.return_value = []

        # Call the callback function
        response = verificar_usuario_callback(request_args,{})

        # Assert that the response contains the expected status code and message
        expected_response = '{"status": 404, "message": "Error: Usuario no existe o la contrasena es incorrecta."}'
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()