import requests
import json

url = 'http://127.0.0.1:8000/generic_api/posts/'
res = requests.get(url)

# print('ステータス', res.status_code)
# print('ヘッダ', res.headers)
# print('内容', res.text)
json_res = json.loads(res.text)
if 'next' in json_res.keys():
    next_url = json_res['next']
    res = requests.get(next_url)
    print(res.text)
