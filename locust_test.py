import time
import random
import json
from locust import HttpUser, task, tag, between


class RESTServerUser(HttpUser):
    """ Класс, эмулирующий пользователя / клиента сервера """
    wait_time = between(1.0, 10.0)       # время ожидания пользователя перед выполнением новой task

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.token = ""
       self.headers = {}

    def on_start(self):
        self.token = self.login()
        self.headers = {'Authorization': 'Token ' + self.token}

    def login(self):
        data = {"username": "Server", "password": "SV123456"}
        response = self.client.post("/application/token/login/", data=data)
        return json.loads(response._content)['auth_token']

    @tag("get_last_news")
    @task(3)
    def get_last_news(self):
        """ Тест GET-запроса (получение последних новостей) """
        with self.client.get('/dreamapp/news',
                             headers=self.headers,
                             catch_response=True,
                             name='/dreamapp/news') as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            # Иначе обозначаем как "отказ"
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("get_friend_list")
    @task(2)
    def get_friend_list(self):
        """ Тест GET-запроса (получение списка друзей) """
        with self.client.get('/dreamapp/friendlist/',
                             headers=self.headers,
                             catch_response=True,
                             name='/dreamapp/friendlist/') as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("get_server")
    @task(3)
    def get_server(self):
        """ Тест GET-запроса (получение списка серверов) """
        with self.client.get('/dreamapp/server',
                             headers=self.headers,
                             catch_response=True,
                             name='/dreamapp/server') as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("post_news")
    @task(1)
    def post_news(self):
        """ Тест POST-запроса (создание записи новости) """
        # Генерируем случайные данные в опредленном диапазоне
        test_data = {'topic': f"Случайная новость {random.randint(1, 10000)}",
                     'text': f"Эта новость сгенерирована случайно {random.randint(1, 10000)}"}
        post_data = json.dumps(test_data)       # сериализуем тестовые данные в json-строку
        headers = self.headers.copy()
        headers['content-type'] = 'application/json'
        # отправляем POST-запрос с данными (POST_DATA)
        with self.client.post('/dreamapp/news/post',
                              catch_response=True,
                              name='/dreamapp/news/post', data=post_data,
                              headers=headers) as response:
            # проверяем, корректность возвращаемого HTTP-кода
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("post_server")
    @task(1)
    def post_server(self):
        """ Тест POST-запроса (создание записи о сервере) """
        # Генерируем случайные данные в опредленном диапазоне
        test_data = {'ip': random.randint(1, 99999999),
                     'port': random.randint(1, 1000000),
                     'name': random.randint(7, 123456)}
        post_data = json.dumps(test_data)       # сериализуем тестовые данные в json-строку
        headers = self.headers.copy()
        headers['content-type'] = 'application/json'
        # отправляем POST-запрос с данными (POST_DATA)
        with self.client.post('/dreamapp/server/post',
                              catch_response=True,
                              name='/dreamapp/server/post', data=post_data,
                              headers=headers) as response:
            # проверяем, корректность возвращаемого HTTP-кода
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("put_server")
    @task(1)
    def put_server(self):
        """ Тест PUT-запроса (обновление записи о сервере) """
        test_data = {'ip': random.randint(1000, 9999),
                     'port': random.randint(1, 100)}
        put_data = json.dumps(test_data)
        headers = self.headers.copy()
        headers['content-type'] = 'application/json'
        # отправляем PUT-запрос
        with self.client.put(f'/dreamapp/server/update/{random.randint(1, 3)}',
                             catch_response=True,
                             name='/dreamapp/server/update/',
                             data=put_data,
                             headers=headers) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    def on_stop(self):
        pass
