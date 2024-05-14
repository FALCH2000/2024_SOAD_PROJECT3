import requests

# CAMBIAR EL FINAL DE LA URL
url = "https://us-central1-soa-project3.cloudfunctions.net/obtener-usuario/?username=admin1&password=admin1"

response = requests.get(url)
print(response.content)

