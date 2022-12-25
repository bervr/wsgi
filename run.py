from wsgiref.simple_server import make_server

from framework.main import Framework
from urls import routes
from framework.middlware import middleware

application = Framework(routes, middleware)

if __name__ == "__main__":
    with make_server('', 8080, application) as httpd:
        print("Запущен сервер  на порту 8080...")
        httpd.serve_forever()