import datetime
from time import time


class AppRoute:
    """
    Определяем маршруты как в Flask
    Структурный паттерн - декоратор
    """
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        # Переопределяем метод call т.к. декоратор это callable object
        # при вызове декоратора заполняем словарь роутов
        self.routes[self.url] = cls()


class Timer:
    """
    Замеряем время выполнения
    Структурный паттерн - декоратор
    """
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        # В call методе определяем обертку
        # чтобы декорировать каждый отдельный метод
        def _wrapper(method):
            '''
            нужен для того, чтобы декоратор класса wrapper обернул во wrapper
            каждый метод декорируемого класса
            '''
            def timed(*args, **kwargs):
                start = time()
                result = method(*args, **kwargs)
                stop = time()
                execute_time = stop - start
                print(f'{datetime.datetime.now()} метод {self.name} выполнялся {execute_time:2.2f} мc')
                return result
            return timed
        return _wrapper(cls)


# class TimeToContext:
#     """
#     "контекстный процессор"
#     Структурный паттерн - декоратор
#     """
#     def __init__(self, **kwargs):
#         self.time = time()
#
#
#     def __call__(self, cls):
#         # В call методе определяем обертку
#         # чтобы декорировать каждый отдельный метод
#         def _wrapper(method):
#             '''
#             нужен для того, чтобы декоратор класса wrapper обернул во wrapper
#             каждый метод декорируемого класса
#             '''
#             def add_params(*args, **kw):
#                 if method == 'render':
#                     print(method)
#             return add_params()
#         return _wrapper(cls)
