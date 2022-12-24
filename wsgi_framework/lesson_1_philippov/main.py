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
        request = {}
        path = environ['PATH_INFO']
        request['path'] = path
        # взяли из словаря path запроса
        if not path.endswith('/'):
            path = f'{path}/'
        # добавили закрывающий слеш
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




