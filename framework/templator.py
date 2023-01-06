import datetime
import os

from jinja2 import FileSystemLoader
from jinja2 import Environment

folder = 'templates'
root_dir = os.getcwd()
templates_folder = os.path.join(root_dir, folder)


def render(template_name, folder=templates_folder, **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)

    template = env.get_template(template_name)
    env.filters['debug'] = debug
    # with open(template, encoding='utf-8') as file:
    #     template = Template(file.read())
    kwargs['date'] = datetime.date.today()
    return template.render(**kwargs)

def debug(text):
    print(text)
    return ''


if __name__ == "__main__":
    templates_path = os.path.join(os.path.dirname(os.getcwd()), 'templates')
    test = render('index.html', templates_path ) # , params=[{'username': 'Alex'}, {'city': 'Moscow'}])
