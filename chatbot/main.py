import functions_framework
import json
from markupsafe import escape
from google.cloud import language_v1

def analyze_text(text):

    if isinstance(text, str) and len(text) > 5:
        client = language_v1.LanguageServiceClient()

        # The text to analyze
        document = language_v1.types.Document(
            content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
        )

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment

        return sentiment
    else:
        return 1
    

# Function to interpret sentiment score
def interpret_sentiment(score):
    if score < -0.25:
        return "Negative"
    elif score > 0.25:
        return "Positive"
    else:
        return "Neutral"

def generateAnswer(kind):
    responses = {
        'Negative': "I'm sorry to hear that. We will try to improve our service.",
        'Neutral': "I understand. Thank you for sharing.",
        'Positive': "That's wonderful to hear! We're glad you enjoyed your experience."
    }
    return responses.get(kind, "Unable to determine sentiment.")

@functions_framework.http
def chatbot(request):
    request_args = request.args
    path = (request.path)

    if path == "/" and request.method == 'GET':
        if request_args and "texto" in request_args:
            text = request_args["texto"]
            # ESTAS 2 LINEAS CONSUMEN CREDITOS SI SE USAN
            sentiment = analyze_text(text)

            if sentiment != 1:
                kind = interpret_sentiment(sentiment.score)

                answer = {
                    "status_code": 200,
                    "message": "OK",
                    "data": generateAnswer(kind)
                }
            
                return json.dumps(answer, ensure_ascii=False)
            else:
                answer = {
                    "status_code": 400,
                    "message": "Bad Request",
                    "data": "Texto debe tener al menos 5 caracteres"
                }
                return json.dumps(answer, ensure_ascii=False)
        else:
            answer = {
                "status_code": 400,
                "message": "Bad Request",
                "data": "Texto no encontrado"
            }
            return json.dumps(answer, ensure_ascii=False)
    else:
        answer = {
            "status_code": 404,
            "message": "Not Found",
            "data": "Ruta no encontrada"
        }

        return json.dumps(answer, ensure_ascii=False)