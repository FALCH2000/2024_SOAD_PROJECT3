import requests

# CAMBIAR EL FINAL DE LA URL
url = "https://us-central1-groovy-rope-416616.cloudfunctions.net/verificar-usuario/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiRG9tdGF4eCIsInBhc3N3b3JkIjoicGFzc3dvcmQiLCJleHAiOiIyMDI1LTA1LTEwIDAwOjUzOjMyLjkwMzE3MiJ9.QmIz9qWNvrpALn0gZ-_Hdt4oknyn38enY1i0oOn56KY"
response = requests.get(url)
print(response.content)
