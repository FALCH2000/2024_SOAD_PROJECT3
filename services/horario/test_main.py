import unittest
from unittest.mock import patch, Mock
from main import ampliar_disponibilidad_reservas_callback

class TestAmpliarDisponibilidadReservasCallback(unittest.TestCase):
    @patch('main.usar_bd')
    @patch('main.insert_into_db')
    def test_valid_opening_and_closing_times(self, mock_insert_into_db, mock_usar_bd):
        # Mock the message data
        message = Mock()
        message.data.decode.return_value = '{"Local_ID": 1, "Opening_Time": "08:00:00", "Closing_Time": "20:00:00"}'

        # Mock the database query
        mock_usar_bd.return_value = [{'Opening_Time': '09:00:00', 'Closing_Time': '19:00:00'}]

        # Call the callback function
        ampliar_disponibilidad_reservas_callback(message)

        # Assert that the database was updated with the new opening and closing times
        mock_insert_into_db.assert_called_once_with("UPDATE Restaurant_Data SET Opening_Time = '08:00:00', Closing_Time = '20:00:00' WHERE Local_ID = 1")

    @patch('main.usar_bd')
    @patch('main.insert_into_db')
    def test_invalid_opening_and_closing_times(self, mock_insert_into_db, mock_usar_bd):
        # Mock the message data
        message = Mock()
        message.data.decode.return_value = '{"Local_ID": 1, "Opening_Time": "08:00:00", "Closing_Time": "20:00:00"}'

        # Mock the database query
        mock_usar_bd.return_value = [{'Opening_Time': '07:00:00', 'Closing_Time': '21:00:00'}]

        # Call the callback function
        ampliar_disponibilidad_reservas_callback(message)

        # Assert that the database was not updated
        mock_insert_into_db.assert_not_called()

    @patch('main.usar_bd')
    @patch('main.insert_into_db')
    def test_missing_data_fields(self, mock_insert_into_db, mock_usar_bd):
        # Mock the message data
        message = Mock()
        message.data.decode.return_value = '{"Local_ID": 1}'

        # Call the callback function
        ampliar_disponibilidad_reservas_callback(message)

        # Assert that the database was not queried or updated
        mock_usar_bd.assert_not_called()
        mock_insert_into_db.assert_not_called()

if __name__ == '__main__':
    unittest.main()