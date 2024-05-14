import unittest
from unittest.mock import MagicMock, patch, call
from main import crear_usuario_callback

class TestCrearUsuarioCallback(unittest.TestCase):
    def test_creates_user_successfully(self):
        message = MagicMock()
        message.data.decode.return_value = '{"method": "crear-usuario", "username": "jusfb18", "password": "testpassword", "first_name": "John", "last_name1": "Doe", "last_name2": "Smith", "security_question": "What is your favorite color?", "security_answer": "Blue"}'
        message.ack.return_value = None

        with patch('main.usar_bd_sin_return') as mock_usar_bd_sin_return:
            crear_usuario_callback(message)

            mock_usar_bd_sin_return.assert_has_calls([call("INSERT INTO User_ (Username, Encrypted_Password, First_Name, Last_Name1, Last_Name2, Security_Question, Security_Answer)                         VALUES ('jusfb18', '9f735e0df9a1ddc702bf0a1a7b83033f9f7153a00c29de82cedadc9957289b05', 'John', 'Doe',                         'Smith', 'dcc535df7b1cd1f8ee25ffb32741b81e069d01ccaeaeb3e6ae0a9830dd09db2e', 'ec7d56a01607001e6401366417c5e2eb00ffa0df17ca1a9a831e0b32c8f11bf7')"),call("INSERT INTO User_Type_Association (Username, Type_ID)                            VALUES ('jusfb18', 2)")])

        message.ack.assert_called_once()

    def test_missing_data_in_request(self):
        message = MagicMock()
        message.data.decode.return_value = '{"method": "crear-usuario", "username": "jusfb18", "password": "testpassword", "first_name": "John", "last_name1": "Doe"}'
        message.ack.return_value = None

        with patch('builtins.print') as mock_print:
            crear_usuario_callback(message)

            mock_print.assert_called_once_with("Codigo: 400. Faltan datos en la solicitud de creacion de usuario.")

        message.ack.assert_called_once()

    def test_incorrect_method(self):
        message = MagicMock()
        message.data.decode.return_value = '{"method": "update-usuario", "username": "jusfb18", "password": "testpassword", "first_name": "John", "last_name1": "Doe", "last_name2": "Smith", "security_question": "What is your favorite color?", "security_answer": "Blue"}'
        message.ack.return_value = None

        with patch('builtins.print') as mock_print:
            crear_usuario_callback(message)

            mock_print.assert_called_once_with("Codigo: 400. Metodo incorrecto.")

        message.ack.assert_called_once()

    def test_error_creating_user(self):
        message = MagicMock()
        message.data.decode.return_value = '{"method": "crear-usuario", "username": "jusfb18", "password": "testpassword", "first_name": "John", "last_name1": "Doe", "last_name2": "Smith", "security_question": "What is your favorite color?", "security_answer": "Blue"}'
        message.ack.return_value = None

        with patch('main.usar_bd_sin_return') as mock_usar_bd_sin_return:
            mock_usar_bd_sin_return.side_effect = Exception("Database error")

            with patch('builtins.print') as mock_print:
                crear_usuario_callback(message)

                mock_print.assert_called_once_with("Codigo: 500. Error al crear el usuario: Database error")

        message.ack.assert_called_once()

if __name__ == '__main__':
    unittest.main()