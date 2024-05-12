import requests
import json

url = "https://us-central1-soa-project3.cloudfunctions.net/feedback-chatbot"

data = {
    "texto": "I'm so happy!"
}

response = requests.get(url, params=data)
print(response.json())

