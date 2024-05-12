import json
import pytest
from main import obtener_menu_callback

def test_obtener_menu_callback():
    # Mock data
    message = {}

    # Call the function
    result = obtener_menu_callback(message)

    # Parse the result
    result_json = json.loads(result)

    # Assertions
    assert "data" in result_json
    assert "types" in result_json["data"]
    assert "MainCourses" in result_json["data"]
    assert "Drinks" in result_json["data"]
    assert "Desserts" in result_json["data"]
    assert "status" in result_json
    assert "message" in result_json
    assert result_json["status"] == 200
    assert result_json["message"] == "Menu obtenido correctamente"