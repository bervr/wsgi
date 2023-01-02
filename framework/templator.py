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
    # with open(template, encoding='utf-8') as file:
    #     template = Template(file.read())
    return template.render(**kwargs)


if __name__ == "__main__":
    test = render('home_site.html') # , params=[{'username': 'Alex'}, {'city': 'Moscow'}])
