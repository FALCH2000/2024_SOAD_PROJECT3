import unittest
from unittest.mock import patch, Mock
from main import obtener_calendario_callback

class TestObtenerCalendarioCallback(unittest.TestCase):
    @patch('main.usar_bd')
    def test_all_tables_available(self, mock_usar_bd):
        # Mock the message data
        date_request = "2022-12-31"
        start_time_request = "08:00:00"
        headers = {}

        # Mock the database query
        mock_usar_bd.return_value = [('1', '4'), ('2', '2'), ('3', '6')]

        # Call the callback function
        response = obtener_calendario_callback(date_request, start_time_request, headers)

        # Assert that the response contains the expected data
        expected_response = (
            '{"data": {"available_tables": [{"Table_ID": "1", "Chairs": "4"}, {"Table_ID": "2", "Chairs": "2"}, {"Table_ID": "3", "Chairs": "6"}]}, "status": 200, "message": "Mesas disponibles obtenidas correctamente."}',
            200,
            {}
        )
        self.assertEqual(response, expected_response)

    @patch('main.usar_bd')
    def test_some_tables_available(self, mock_usar_bd):
        # Mock the message data
        date_request = "2022-12-31"
        start_time_request = "08:00:00"
        headers = {}

        # Mock the database query
        mock_usar_bd.return_value = [('1', '4'), ('2', '2'), ('3', '6')]
        mock_usar_bd.side_effect = [
            [('1', '4')],
            [('2', '2')],
            [('3', '6')]
        ]

        # Call the callback function
        response = obtener_calendario_callback(date_request, start_time_request, headers)

        # Assert that the response contains the expected data
        expected_response = (
            '{"data": {"available_tables": [{"Table_ID": "1", "Chairs": "4"}, {"Table_ID": "2", "Chairs": "2"}, {"Table_ID": "3", "Chairs": "6"}]}, "status": 200, "message": "Mesas disponibles obtenidas correctamente."}',
            200,
            {}
        )
        self.assertEqual(response, expected_response)

    @patch('main.usar_bd')
    def test_no_tables_available(self, mock_usar_bd):
        # Mock the message data
        date_request = "2022-12-31"
        start_time_request = "08:00:00"
        headers = {}

        # Mock the database query
        mock_usar_bd.return_value = [('1', '4'), ('2', '2'), ('3', '6')]
        mock_usar_bd.side_effect = [
            [('1', '4'), ('2', '2'), ('3', '6')]
        ]

        # Call the callback function
        response = obtener_calendario_callback(date_request, start_time_request, headers)

        # Assert that the response contains the expected data
        expected_response = (
            '{"data": {"available_tables": []}, "status": 404, "message": "No hay mesas disponibles para la fecha y hora solicitada."}',
            404,
            {}
        )
        self.assertEqual(response, expected_response)

    @patch('main.usar_bd')
    def test_error_getting_calendar(self, mock_usar_bd):
        # Mock the message data
        date_request = "2022-12-31"
        start_time_request = "08:00:00"
        headers = {}

        # Mock the database query to raise an exception
        mock_usar_bd.side_effect = Exception("Database error")

        # Call the callback function
        response = obtener_calendario_callback(date_request, start_time_request, headers)

        # Assert that the response contains the expected data
        expected_response = (
            '{"data": {}, "status": 500, "message": "Error al obtener el calendario: Database error"}',
            500,
            {}
        )
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()