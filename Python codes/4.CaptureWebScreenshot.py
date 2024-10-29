import requests
import urllib.parse

BASE = 'https://mini.s-shot.ru/1024x0/JPEG/1024/Z100/?' # you can modify size, format, zoom
url = 'https://stackoverflow.com/'#or whatever link you need
url = urllib.parse.quote_plus(url) #service needs link to be joined in encoded format
print(url)

path = 'target1.jpg'
response = requests.get(BASE + url, stream=True)

if response.status_code == 200:
    with open(path, 'wb') as file:
        for chunk in response:
            file.write(chunk)