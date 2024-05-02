import requests

res = requests.post(
    'http://127.0.0.1:8000/api_token_auth/',
    data={
        'username': 'user',
        'password': 'usertest'
    }
)

print(res.text)

res_json = res.json()
res2 = requests.post(
    'http://127.0.0.1:8000/api2/v2/product/',
    data={
        # 'username': 'user',
        # 'password': 'usertest',
        'name': 'product 1',
        'price': '1900',
        'user': 3
    },
    headers={
        'Authorization': f"Token {res_json['token']}"
    }
)

print(res2.text)