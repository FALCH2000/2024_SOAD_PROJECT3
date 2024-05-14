import unittest
from unittest.mock import patch, MagicMock,call
from main import crear_reserva_callback

class TestCrearReservaCallback(unittest.TestCase):
    @patch('main.usar_bd')
    @patch('main.insert_into_db')
    @patch('main.publicar_mensaje')
    def test_successful_reservation_creation(self, mock_publicar_mensaje, mock_insert_into_db, mock_usar_bd):
        # Mock the message data
        message = MagicMock()
        message.data.decode.return_value = '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluMSIsInBhc3N3b3JkIjoiYWRtaW4xIiwiZXhwIjo5OTk5OTk5OTk5fQ.C4eJAyZrLOLwkVQE2T1vK3u1eMp4fCwjGFDqy1MXt9M", "data": {"method": "crear-reserva", "number_of_people": 4, "reservation_date": "2022-12-31", "start_time": "18:00:00", "selected_tables": [1, 2, 3]}}'

        # Mock the token verification
        mock_requests_get = patch('main.requests.get').start()
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {"username": "testuser"}

        # Mock the database queries
        mock_usar_bd.side_effect = [[(1,)], [("08:00:00",)], [("22:00:00",)]]

        # Call the callback function
        crear_reserva_callback(message)

        # Assert that the appropriate database queries were made
        mock_usar_bd.assert_has_calls([
            call("SELECT Chairs FROM Tables WHERE Table_Number = 1"),
            call("SELECT Chairs FROM Tables WHERE Table_Number = 2"),
            call("SELECT Chairs FROM Tables WHERE Table_Number = 3"),
            call("SELECT Opening_Time FROM Restaurant_Data WHERE Local_ID = 1"),
            call("SELECT Closing_Time FROM Restaurant_Data WHERE Local_ID = 1"),
            call("INSERT INTO Reservations (User_ID, Number_Of_People, Date_Reserved, Start_Time, End_Time) VALUES ('testuser', 4, '2022-12-31', '18:00:00', '20:00:00')"),
            call("SELECT Reservation_ID FROM Reservations WHERE User_ID = 'testuser' AND Date_Reserved = '2022-12-31' AND Start_Time = '18:00:00' AND End_Time = '20:00:00'"),
            call("INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) VALUES (1, '2022-12-31', '18:00:00', '20:00:00')"),
            call("INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) VALUES (2, '2022-12-31', '18:00:00', '20:00:00')"),
            call("INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) VALUES (3, '2022-12-31', '18:00:00', '20:00:00')"),
            call("INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) VALUES (1, 1)"),
            call("INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) VALUES (1, 2)"),
            call("INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) VALUES (1, 3)")
        ])

        # Assert that the appropriate message was published
        mock_publicar_mensaje.assert_called_once_with({
            "data": "",
            "status": 200,
            "message": "Reserva creada con éxito"
        })

    @patch('main.publicar_mensaje')
    def test_invalid_token(self, mock_publicar_mensaje):
        # Mock the message data
        message = MagicMock()
        message.data.decode.return_value = '{"token": "invalid_token", "data": {"method": "crear-reserva", "number_of_people": 4, "reservation_date": "2022-12-31", "start_time": "18:00:00", "selected_tables": [1, 2, 3]}}'

        # Mock the token verification
        mock_requests_get = patch('main.requests.get').start()
        mock_requests_get.return_value.status_code = 400

        # Call the callback function
        crear_reserva_callback(message)

        # Assert that the appropriate message was published
        mock_publicar_mensaje.assert_called_once_with({
            "data": "",
            "status": 400,
            "message": "Token invalido"
        })

    @patch('main.publicar_mensaje')
    def test_missing_attributes(self, mock_publicar_mensaje):
        # Mock the message data
        message = MagicMock()
        message.data.decode.return_value = '{"token": "mocked_token", "data": {"method": "crear-reserva", "number_of_people": 4, "reservation_date": "2022-12-31"}}'

        # Call the callback function
        crear_reserva_callback(message)

        # Assert that the appropriate message was published
        mock_publicar_mensaje.assert_called_once_with({
            "data": "",
            "status": 400,
            "message": "Faltan atributos en la solicitud"
        })

if __name__ == '__main__':
    unittest.main()