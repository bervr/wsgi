from wsgiref.simple_server import make_server

from framework.main import Framework
from urls import routes as r
from views import routes
from framework.middlware import middleware

routes = routes | r  # объединим пути из urls и из views

application = Framework(routes, middleware)

if __name__ == "__main__":
    with make_server('', 8080, application) as httpd:
        print(f"Запущен сервер  на порту 8080... http://127.0.0.1:8080/")
        httpd.serve_forever()