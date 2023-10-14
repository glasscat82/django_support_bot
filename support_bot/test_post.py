import requests
import json


def p(text, *args):
    print(text, *args, sep=' / ', end='\n')

# целевой URL-адрес
token_you_bot = ''
url = f'http://127.0.0.1:8000/quport/{token_you_bot}/'

if __name__ == '__main__':
    # данные в виде словаря
    param = {'some': 'data', 'k':12, 'w':23}

    # кодируем словарь в формат JSON
    json_param = json.dumps(param)

    # отправка POST-запроса с данными в формате JSON
    resp = requests.post(url, data=json_param)
    
    p(resp)