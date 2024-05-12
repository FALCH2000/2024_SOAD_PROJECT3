import requests

# CAMBIAR EL FINAL DE LA URL
url = "https://us-central1-groovy-rope-416616.cloudfunctions.net/obtener-usuario/?username=Domtaxx&password=password"

response = requests.get(url)
print(response.content)

