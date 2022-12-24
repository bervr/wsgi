import pprint
from quopri import decodestring

from lesson_2_philippov.http_requests import PostReq, GetReq


class Page404:
    def __call__(self, request):
        return '404 Not Found', '<p>404 PAGE Not Found</p>'

class Framework:
    """Основной обработчик. Используется в качестве callable функции, чтобы передать
    роуты и использовать мидлвейрс.  Т.к. application по стандарту PEP-3333 принимает только два параметра.
    Поскольку приложением у нас должен быть callable-объект, то для решения проблемы мы вместо
    функции application сделаем класс Framework и перегрузим в нем метод __call__()."""

    def __init__(self, routes, middleware):
        self.routes = routes
        self.controllers = middleware

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'
        # добавили закрывающий слеш
        request = {'path': path, 'data':{}}

        # for k, v in environ.items():
        #     print(k, v)
        method = environ['REQUEST_METHOD']
        # определяем метод и добавляем в request
        request['method'] = method
        if method == 'POST':
            data = PostReq().get_requests_params(environ)
            request['data'] = Framework.decode_values(data)
            print(f'получили POST {Framework.decode_values(data)}')
            Framework.save_file(request)
        if method == 'GET':
            params = GetReq().get_requests_params(environ)
            request['request_params'] = Framework.decode_values(params)
            print(f'получили GET {Framework.decode_values(params)}')
            Framework.save_file(request)
        if path in self.routes:
            view = self.routes[path]
        else:
            view = Page404()
        # отпределили нужную вьюху
        for controller in self.controllers:
            controller(request)
        # прогнали через все мидлвайрсы
        status, body = view(request)
        # собираем все вместе и отвечаем
        start_response(status, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_values(data):
        result_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
            val_decode = decodestring(val).decode('UTF-8')
            result_data[k] = val_decode
        return result_data

    @staticmethod
    def save_file(data):
        if data["method"] == "POST":
            data_req = data["data"]
        elif data["method"] == "GET":
            data_req = data["request_params"]
        if data_req:
            with open('request_log.txt', 'a', encoding='utf-8') as file:
                file.writelines(f'Получен {data["method"]} запрос содержащий {data_req}\n')









