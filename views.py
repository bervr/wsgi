import os

from framework.templator import render
from patterns.creational import Engine, Logger
site = Engine()
logger = Logger('views')

templates_path = os.path.join(os.getcwd(), 'templates')


"""Собираем шаблоны в старницы и обрабатываем их чтобы на выходе была вся красота """
class HomePage:
    def __init__(self):
        self.page = 'index.html'

    def __call__(self, request):
        return '200 OK', render(self.page,
                                date=request.get('date', None),
                                objects_list=site.categories,
        )

class SecondPage:
    def __init__(self):

        self.page =  'second.html'


    def __call__(self, request):
        return '200 OK', render(self.page, date=request.get('date', None))

class ContactUs:
    def __init__(self):
        self.page = 'contacts.html'


    def __call__(self, request):
        return '200 OK', render(self.page, date=request.get('date', None))
class CoursesList:
    def __call__(self, request):
        logger.log('Запрос списка курсов')
        try:
            category = site.get_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('courses.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    date=request.get('date', None),
                                    )
        except KeyError:
            return '200 OK', 'There are no courses here'


class CategoryList:
    def __call__(self, request):
        logger.log('Получаем список категорий')
        return '200 OK', render('categories.html',
                                objects_list=site.categories,
                                date=request.get('date', None),)



class AddCourse:
    """Create new course from form data"""
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST' and request['data']:
            data = request['data']
            name = data['course_name']
            name = site.decode_value(name)
            category = None
            if self.category_id >= 0:
                category = site.get_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)
            return '200 OK', render('courses.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    date=request.get('date', None),)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.get_category_by_id(int(self.category_id))

                return '200 OK', render('new_course.html',
                                        name=category.name,
                                        id=category.id,
                                        date=request.get('date', None),
                                        )
            except KeyError:
                return '200 OK', 'There are no categories fo courses. You have to create it before'


class AddCategory:
    """Create new category from form data"""
    def __call__(self, request):

        if request['method'] == 'POST' and request['data']:
            data = request['data']
            name = data['category_name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = site.get_category_by_id(int(category_id)) if category_id else None
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list=site.categories,
                                    date=request.get('date', None),)
        else:
            categories = site.categories
            return '200 OK', render('new_category.html',
                                    categories=categories,
                                    date=request.get('date', None),
                                    )


class CopyCourse:
    def __call__(self, request):
        req_params = request['request_params']
        try:
            name = req_params['name']
            course = site.get_course(name)
            if course:
                new_course = course.clone()
                new_course.name = f'copy_{name}'
                site.courses.append(new_course)



            return '200 OK', render('courses.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name,
                                    date=request.get('date', None),
                                    id=new_course.category.id,
                                    )
        except KeyError:
            return '200 OK', 'Не могу создать здесь'


if __name__ == "__main__":
    pass
