import datetime
import os

templates_path = os.path.join(os.getcwd(), '../templates')


def log_controller(request, *args, **kwargs):
    request['key'] = 'key'

def date_controller(request, *args, **kwargs):
    request['date'] = datetime.date.today()

def css_controller(request, *args, **kwargs):
    request['CSS'] = os.path.join(templates_path, 'general.css')



middleware = [
    css_controller,
    log_controller,
    date_controller,
    ]
