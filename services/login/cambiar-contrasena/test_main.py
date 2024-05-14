import unittest
from unittest.mock import patch, Mock
from main import cambiar_contrasena_callback

# Define a MockMessage class
class MockMessage:
    def __init__(self, data):
        self.data = data
    def ack(self):
        pass

class TestCambiarContrasenaCallback(unittest.TestCase):
    @patch('main.usar_bd')
    @patch('main.usar_bd_sin_return')
    def test_successful_password_change(self, mock_usar_bd_sin_return, mock_usar_bd):
        # Mock the database queries
        mock_usar_bd.return_value = [('hashed_password',)]
        mock_usar_bd_sin_return.return_value = None

        # Mock the Pub/Sub message
        message = MockMessage(data=b'{"method": "cambiar-contrasena", "username": "testuser", "new_password": "newpass", "security_answer": "answer"}')

        # Call the callback function
        cambiar_contrasena_callback(message)

        # Assert that the correct database queries were made
        mock_usar_bd.assert_called_once_with("SELECT * FROM User_ WHERE Username = 'testuser'")
        mock_usar_bd_sin_return.assert_called_once_with("UPDATE User_ SET Encrypted_Password = 'hashed_newpass' WHERE username = 'testuser'")

    @patch('main.usar_bd')
    def test_user_not_found(self, mock_usar_bd):
        # Mock the database query
        mock_usar_bd.return_value = []

        # Mock the Pub/Sub message
        message = MockMessage(data=b'{"method": "cambiar-contrasena", "username": "testuser", "new_password": "newpass", "security_answer": "answer"}')

        # Call the callback function
        cambiar_contrasena_callback(message)

        # Assert that the correct database query was made
        mock_usar_bd.assert_called_once_with("SELECT * FROM User_ WHERE Username = 'testuser'")

    @patch('main.usar_bd')
    def test_incorrect_security_answer(self, mock_usar_bd):
        # Mock the database queries
        mock_usar_bd.return_value = [('hashed_password',), ('wrong_answer',)]

        # Mock the Pub/Sub message
        message = MockMessage(data=b'{"method": "cambiar-contrasena", "username": "testuser", "new_password": "newpass", "security_answer": "answer"}')

        # Call the callback function
        cambiar_contrasena_callback(message)

        # Assert that the correct database queries were made
        mock_usar_bd.assert_called_once_with("SELECT * FROM User_ WHERE Username = 'testuser'")
        mock_usar_bd.assert_called_once_with("SELECT Security_Answer FROM User_ WHERE Username = 'testuser'")

if __name__ == '__main__':
    unittest.main()
