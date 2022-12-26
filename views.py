import os

from framework.templator import render

templates_path = os.path.join(os.getcwd(), 'templates')


"""Собираем шаблоны в старницы и обрабатываем их чтобы на выходе была вся красота """
class HomePage:
    def __init__(self):
        self.page = 'index.html'

    def __call__(self, request):
        return '200 OK', render(self.page, date=request.get('date', None))

class SecondPage:
    def __init__(self):
        self.page = 'second.html'

    def __call__(self, request):
        return '200 OK', render(self.page, date=request.get('date', None))

class ContactUs:
    def __init__(self):
        self.page = 'contacts.html'

    def __call__(self, request):
        return '200 OK', render(self.page,  date=request.get('date', None))



if __name__ == "__main__":
    pass
