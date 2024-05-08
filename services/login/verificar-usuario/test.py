import requests

# CAMBIAR EL FINAL DE LA URL
url = "https://us-central1-groovy-rope-416616.cloudfunctions.net/verificar-usuario/?usuario=client1&contrasena=Blue"

response = requests.get(url)
print(response.content)
