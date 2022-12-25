from jinja2 import Template

def render(template, **kwargs):
    with open(template, encoding='utf-8') as file:
        template = Template(file.read())
    return template.render(**kwargs)


if __name__ == "__main__":
    test = render('home_site.html', params=[{'username': 'Alex'}, {'city': 'Moscow'}])
    print(test)
