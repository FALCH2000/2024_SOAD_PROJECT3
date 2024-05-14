import unittest
from unittest.mock import patch, call
from main import cambiar_contrasena_callback, usar_bd
import hashlib

# Define a MockMessage class
class MockMessage:
    def __init__(self, data):
        self.data = data
    def ack(self):
        pass
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

class TestCambiarContrasenaCallback(unittest.TestCase):
    @patch('main.usar_bd')
    @patch('main.usar_bd_sin_return')
    def test_not_successful_password_change(self, mock_usar_bd_sin_return, mock_usar_bd):
        # Mock the database queries
        mock_usar_bd.return_value = [(encriptar_texto('answer'),)]
        mock_usar_bd_sin_return.return_value = None

        # Mock the Pub/Sub message
        message = MockMessage(data=b'{"method": "cambiar-contrasena", "username": "jusfb18", "new_password": "1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223", "security_answer": "answer"}')

        # Call the callback function
        cambiar_contrasena_callback(message)

        # Assert that the correct database queries were made
        mock_usar_bd.assert_has_calls([call("SELECT * FROM User_ WHERE Username = 'jusfb18'"), call("SELECT Security_Answer FROM User_ WHERE Username = 'jusfb18'")])

    @patch('main.usar_bd')
    @patch('main.usar_bd_sin_return')
    def test_successful_password_change(self, mock_usar_bd_sin_return, mock_usar_bd):
        # Mock the database queries
        mock_usar_bd.return_value = [('ec7d56a01607001e6401366417c5e2eb00ffa0df17ca1a9a831e0b32c8f11bf7',)]
        mock_usar_bd_sin_return.return_value = None

        # Mock the Pub/Sub message
        message = MockMessage(data=b'{"method": "cambiar-contrasena", "username": "jusfb18", "new_password": "1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223", "security_answer": "Blue"}')

        # Call the callback function
        cambiar_contrasena_callback(message)

        # Assert that the correct database queries were made
        mock_usar_bd.assert_has_calls([call("SELECT * FROM User_ WHERE Username = 'jusfb18'"), call("SELECT Security_Answer FROM User_ WHERE Username = 'jusfb18'")])
        mock_usar_bd_sin_return.assert_called_once_with(f"UPDATE User_ SET Encrypted_Password = 'db95ffcac8abb64382f35ffc2ef395e1ab5de705d2143e7f93c7299821492d02'                                WHERE username = 'jusfb18'")

    @patch('main.usar_bd')
    @patch('main.usar_bd_sin_return')
    def test_missing_attributes(self, mock_usar_bd_sin_return, mock_usar_bd):
        # Mock the database queries
        mock_usar_bd.return_value = []
        mock_usar_bd_sin_return.return_value = None

        # Mock the Pub/Sub message
        message = MockMessage(data=b'{"method": "cambiar-contrasena", "username": "jusfb18", "new_password": "1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223"}')

        # Call the callback function
        cambiar_contrasena_callback(message)

        # Assert that the correct database queries were made
        mock_usar_bd.assert_not_called()
        mock_usar_bd_sin_return.assert_not_called()
        

if __name__ == '__main__':
    unittest.main()
