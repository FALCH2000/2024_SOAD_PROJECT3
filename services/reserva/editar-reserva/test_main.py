import unittest
from unittest.mock import patch, Mock
from main import editar_reserva_callback

class TestEditarReservaCallback(unittest.TestCase):
    @patch('main.usar_bd')
    @patch('main.usar_bd_sin_return')
    def test_successful_reservation_edit(self, mock_usar_bd_sin_return, mock_usar_bd):
        # Mock the database queries
        mock_usar_bd.return_value = [('2022-12-31', '18:00:00')]
        mock_usar_bd_sin_return.return_value = None

        # Mock the Pub/Sub message
        message = Mock(data=b'{"method": "editar-reserva", "reservation_id": 1, "number_of_people": 4, "reservation_date": "2022-12-31", "start_time": "18:00:00", "selected_tables": [1, 2]}')

        # Call the callback function
        editar_reserva_callback(message)

        # Assert that the correct database queries were made
        mock_usar_bd.assert_called_once_with("SELECT * FROM Reservations WHERE Reservation_ID = 1")
        mock_usar_bd_sin_return.assert_called_once_with("UPDATE Reservations SET Number_Of_People = 4, Date_Reserved = '2022-12-31', Start_Time = '18:00:00', End_Time = '20:00:00' WHERE Reservation_ID = 1 AND User_ID = 'testuser'")
        mock_usar_bd_sin_return.assert_called_with("DELETE FROM Table_Availability WHERE Table_ID = 1 AND Date_Reserved = '2022-12-31' AND Start_Time = '18:00:00' AND End_Time = '20:00:00'")
        mock_usar_bd_sin_return.assert_called_with("INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) VALUES (1, '2022-12-31', '18:00:00', '20:00:00')")
        mock_usar_bd_sin_return.assert_called_with("DELETE FROM Reservation_Tables_Association WHERE Reservation_ID = 1 AND Table_ID = 1")
        mock_usar_bd_sin_return.assert_called_with("INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) VALUES (1, 1)")
        mock_usar_bd_sin_return.assert_called_with("DELETE FROM Table_Availability WHERE Table_ID = 2 AND Date_Reserved = '2022-12-31' AND Start_Time = '18:00:00' AND End_Time = '20:00:00'")
        mock_usar_bd_sin_return.assert_called_with("INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) VALUES (2, '2022-12-31', '18:00:00', '20:00:00')")
        mock_usar_bd_sin_return.assert_called_with("DELETE FROM Reservation_Tables_Association WHERE Reservation_ID = 1 AND Table_ID = 2")
        mock_usar_bd_sin_return.assert_called_with("INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) VALUES (1, 2)")

    @patch('main.usar_bd')
    def test_reservation_not_found(self, mock_usar_bd):
        # Mock the database query
        mock_usar_bd.return_value = []

        # Mock the Pub/Sub message
        message = Mock(data=b'{"method": "editar-reserva", "reservation_id": 1, "number_of_people": 4, "reservation_date": "2022-12-31", "start_time": "18:00:00", "selected_tables": [1, 2]}')

        # Call the callback function
        editar_reserva_callback(message)

        # Assert that the correct database query was made
        mock_usar_bd.assert_called_once_with("SELECT * FROM Reservations WHERE Reservation_ID = 1")

    @patch('main.usar_bd')
    def test_past_reservation_edit(self, mock_usar_bd):
        # Mock the database query
        mock_usar_bd.return_value = [('2021-12-31', '18:00:00')]

        # Mock the Pub/Sub message
        message = Mock(data=b'{"method": "editar-reserva", "reservation_id": 1, "number_of_people": 4, "reservation_date": "2021-12-31", "start_time": "18:00:00", "selected_tables": [1, 2]}')

        # Call the callback function
        editar_reserva_callback(message)

        # Assert that the correct database query was made
        mock_usar_bd.assert_called_once_with("SELECT * FROM Reservations WHERE Reservation_ID = 1")

if __name__ == '__main__':
    unittest.main()