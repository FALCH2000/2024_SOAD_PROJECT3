# Import pytest
import pytest
import json

# Import the module you want to test
from main import analyze_text, interpret_sentiment, generateAnswer, chatbot
 
# Define test cases using PyTest
def test_analyze_text():
    text = "I am very happy!"
    sentiment_score = analyze_text(text).score
    assert sentiment_score > 0.25

def test_interpret_sentiment():
    assert interpret_sentiment(-0.5) == "Negative"
    assert interpret_sentiment(0) == "Neutral"
    assert interpret_sentiment(0.5) == "Positive"

def test_generateAnswer():
    assert generateAnswer("Negative") == "I'm sorry to hear that. We will try to improve our service."
    assert generateAnswer("Neutral") == "I understand. Thank you for sharing."
    assert generateAnswer("Positive") == "That's wonderful to hear! We're glad you enjoyed your experience."

def test_chatbot():
    # Mock request object
    class MockRequest:
        def __init__(self, args, path, method):
            self.args = args
            self.path = path
            self.method = method

    # Create a mock request
    request = MockRequest(args={"texto": "I am very happy!"}, path="/aa", method="GET")
    
    # Call the chatbot function with the mock request
    response = chatbot(request)

    # Check the response
    assert response == json.dumps({
        "status_code": 404,
        "message": "Not Found",
        "data": "Ruta no encontrada"
    })


