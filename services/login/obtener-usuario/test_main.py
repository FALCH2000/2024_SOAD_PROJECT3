import unittest
from unittest.mock import patch, Mock
import json
import jwt
import hashlib
from main import obtener_usuario_callback

#Secret key to validate tokens
def encriptar_texto(texto):
    # Codifica el texto en UTF-8 antes de encriptar
    texto_codificado = texto.encode('utf-8')
    # Crea un objeto hash utilizando el algoritmo SHA-256
    hash_obj = hashlib.sha256()
    # Actualiza el hash con el texto codificado
    hash_obj.update(texto_codificado)
    # Obtiene el hash en formato hexadecimal
    hash_str_hexadecimal = str(hash_obj.hexdigest())
    return hash_str_hexadecimal

secret_key="6af00dfe63f6495195a3341ef6406c2c" 
class TestObtenerUsuarioCallback(unittest.TestCase):
    def test_successful_user_authentication(self):
        # Mock the request parameters
        username = "jusfb18"
        password = "1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223"
        headers = {}

        # Mock the database query
        mock_usar_bd = patch('main.usar_bd').start()
        mock_usar_bd.return_value = [('hashed_password',)]

        # Call the callback function
        response = obtener_usuario_callback(username, password, headers)
        

        # Assert that the response contains the expected token
        self.assertEqual(token_response['status'], 200)
        self.assertEqual(token_response['message'], "Usuario encontrado y token generado.")
        token_decoded = jwt.decode(jwt=token_response['token'], key=secret_key, algorithms="HS256")
        self.assertEqual(token_decoded['username'], username)
        self.assertEqual(token_decoded['password'], password)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[2], headers)

        # Assert that the correct database query was made
        mock_usar_bd.assert_called_once_with(f"SELECT * FROM User_ WHERE Username = 'testuser' and Encrypted_Password = '{encriptar_texto(password)}'")

    def test_invalid_username(self):
        # Mock the request parameters
        username = ""
        password = "testpass"
        headers = {}

        # Call the callback function
        response = obtener_usuario_callback(username, password, headers)

        # Assert that the response contains the expected error message and status code
        self.assertEqual(response[0], '{"status": 400, "message": "Error: No se ha ingresado un username."}')
        self.assertEqual(response[1], 400)
        self.assertEqual(response[2], headers)

    def test_user_not_found(self):
        # Mock the request parameters
        username = "aa18"
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