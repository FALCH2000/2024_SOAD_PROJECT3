import requests

url = "https://us-central1-groovy-rope-416616.cloudfunctions.net/obtener-calendario/?date=2050--12&start_time=12:00:00"

response = requests.get(url)
print(response.content)
