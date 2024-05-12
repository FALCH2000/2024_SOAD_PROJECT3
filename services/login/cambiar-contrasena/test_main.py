import unittest
from unittest.mock import patch, call
from main import cambiar_contrasena_callback, usar_bd

# Define a MockMessage class
class MockMessage:
    def __init__(self, data):
        self.data = data
    def ack(self):
        pass

class TestCambiarContrasenaCallback(unittest.TestCase):
    @patch('main.usar_bd')
    @patch('main.usar_bd_sin_return')
    def test_not_successful_password_change(self, mock_usar_bd_sin_return, mock_usar_bd):
        # Mock the database queries
        mock_usar_bd.return_value = [('hashed_password',)]
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
        mock_usar_bd.return_value = [('1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223',)]
        mock_usar_bd_sin_return.return_value = None

        # Mock the Pub/Sub message
        message = MockMessage(data=b'{"method": "cambiar-contrasena", "username": "jusfb18", "new_password": "1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223", "security_answer": "Blue"}')

        # Call the callback function
        cambiar_contrasena_callback(message)

        # Assert that the correct database queries were made
        mock_usar_bd.assert_has_calls([call("SELECT * FROM User_ WHERE Username = 'jusfb18'"), call("SELECT Security_Answer FROM User_ WHERE Username = 'jusfb18'")])
        mock_usar_bd_sin_return.assert_called_once_with("UPDATE User_ SET Password = '1917E33407C28366C8E3B975B17E7374589312676B90229ADB4CE6E58552E223'")

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
