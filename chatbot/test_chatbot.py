# Import pytest
import pytest

# Import the module you want to test
from main import analyze_text, interpret_sentiment, generateAnswer
 
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

