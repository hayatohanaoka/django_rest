import requests

URL = 'http://127.0.0.1:8000/api/datetime/'

print('============正常系=============')

# GET 正常系
get_response = requests.get(URL, params={'timezone': 'US/Eastern'})
print(get_response.status_code)
print(get_response.headers)
print(get_response.text)

print('=========================')

post_response = requests.post(URL, data={'timezone': 'US/Eastern'})
print(post_response.status_code)
print(post_response.headers)
print(post_response.text)

print('=========================')

delete_response = requests.delete(URL)
print(delete_response.status_code)
print(delete_response.headers)
print(delete_response.text)

print('=========================')

put_response = requests.put(URL)
print(put_response.status_code)
print(put_response.headers)
print(put_response.text)



print('============異常系=============')

# GET 異常系
get_response = requests.get(URL, params={'timezone': 'US/E'})
print(get_response.status_code)
print(get_response.headers)
print(get_response.text)

print('=========================')

# POST 異常系
post_response = requests.post(URL, data={'timezone': 'US/E'})
print(post_response.status_code)
print(post_response.headers)
print(post_response.text)
