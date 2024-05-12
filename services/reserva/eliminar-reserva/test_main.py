import unittest
from unittest.mock import patch, Mock
from main import eliminar_reserva_callback

class TestEliminarReservaCallback(unittest.TestCase):
    @patch('main.usar_bd')
    @patch('main.delete_from_db')
    def test_successful_reservation_deletion(self, mock_delete_from_db, mock_usar_bd):
        # Mock the message data
        message = Mock()
        message.data.decode.return_value = '{"data": {"method": "eliminar-reserva", "reservation_id": 1, "reservation_date": "2022-12-31", "start_time": "18:00:00"}}'

        # Mock the token decoding
        message.args.get.return_value = 'valid_token'

        # Mock the database queries
        mock_usar_bd.return_value = [('Reservation_ID', '1')]
        mock_usar_bd.side_effect = [[('Table_ID', '1'), ('Table_ID', '2')], []]

        # Call the callback function
        eliminar_reserva_callback(message)

        # Assert that the database queries and deletions were called correctly
        mock_usar_bd.assert_called_with("SELECT * FROM Reservations WHERE Reservation_ID = 1")
        mock_delete_from_db.assert_called_with("DELETE FROM Reservation_Tables_Association WHERE Reservation_ID = 1")
        mock_delete_from_db.assert_any_call("DELETE FROM Table_Availability WHERE Table_ID = 1 AND Date_Reserved = '2022-12-31' AND Start_Time = '18:00:00'")
        mock_delete_from_db.assert_any_call("DELETE FROM Table_Availability WHERE Table_ID = 2 AND Date_Reserved = '2022-12-31' AND Start_Time = '18:00:00'")
        mock_delete_from_db.assert_called_with("DELETE FROM Reservations WHERE Reservation_ID = 1")

    @patch('main.usar_bd')
    def test_missing_data_fields(self, mock_usar_bd):
        # Mock the message data
        message = Mock()
        message.data.decode.return_value = '{"data": {"method": "eliminar-reserva"}}'

        # Call the callback function
        result = eliminar_reserva_callback(message)

        # Assert that the response is as expected
        expected_result = '{"status": "400", "message": "Faltan datos en la solicitud"}'
        self.assertEqual(result, expected_result)

    @patch('main.usar_bd')
    def test_nonexistent_reservation(self, mock_usar_bd):
        # Mock the message data
        message = Mock()
        message.data.decode.return_value = '{"data": {"method": "eliminar-reserva", "reservation_id": 1, "reservation_date": "2022-12-31", "start_time": "18:00:00"}}'

        # Mock the database query
        mock_usar_bd.return_value = []

        # Call the callback function
        result = eliminar_reserva_callback(message)

        # Assert that the response is as expected
        expected_result = '{"status": "404", "message": "La reserva no existe"}'
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()