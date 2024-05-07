import requests
import json

url = "https://us-central1-groovy-rope-416616.cloudfunctions.net/feedback-chatbot"

data = {
    "texto": "I'm so happy!"
}

response = requests.get(url, params=data)
print(response.json())

