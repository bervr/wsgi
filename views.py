import os

from framework.templator import render

templates_path = os.path.join(os.getcwd(), 'templates')


"""Собираем шаблоны в старницы и обрабатываем их чтобы на выходе была вся красота """
class HomePage:
    def __init__(self):
        self.page = os.path.join(templates_path, 'home_site.html')

    def __call__(self, request):
        return '200 OK', render(self.page, date=request.get('date', None))

class SecondPage:
    def __init__(self):
        self.page = os.path.join(templates_path, 'second.html')

    def __call__(self, request):
        return '200 OK', render(self.page)

class ContactUs:
    def __init__(self):
        self.page = os.path.join(templates_path, 'contactus.html')

    def __call__(self, request):
        return '200 OK', render(self.page)



if __name__ == "__main__":
    pass
