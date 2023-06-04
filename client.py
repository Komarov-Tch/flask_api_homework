# import requests

# response = requests.post('http://127.0.0.1:8080/user/', json={'username': 'user1', 'password': '123456789', 'email':'user1@mail.ru'})
# print(response.json())
# response = requests.post('http://127.0.0.1:8080/news/', json={'title': 'title1', 'content': 'content1'}, params={'username': 'user1'})
# print(response.json())
# response = requests.get('http://127.0.0.1:8080/news/1')
# print(response.json())
# response = requests.patch('http://127.0.0.1:8080/news/1', json={
#    'title': 'важное объявление',
#    'content': 'Прям очень важное объявление2'
# }, params={
#    'username': 'user1',
#    'password': '123456789'
# })
# print(response.json())
# response = requests.delete('http://127.0.0.1:8080/news/1', params={'username': 'user1', 'password': '123456789'})
# print(response.json())
