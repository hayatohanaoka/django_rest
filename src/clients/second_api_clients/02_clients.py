import requests

result = requests.get('http://127.0.0.1:8000/api2/')
print(result.text)
print(type(result.text))
data = result.json()
print(data)
for d in data:
    print(type(d))
    print(d['name'])
