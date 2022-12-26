import datetime
from copy import deepcopy
from quopri import decodestring
from abc import abstractmethod

class Student:
    pass

class Teacher:
    pass

staff = types = {
        'student': Student,
        'teacher': Teacher
    }

class CreateFactory:
    """Абстрактный класс фабричный метод"""
    def __new__(cls, types, *args, **kwargs):
        cls.types = types

    @classmethod
    def create(cls, new_type):
        return cls.types[new_type]()

# class UserFactory:
#     """Класс фабричный метод"""
#     types = {
#         'student': Student,
#         'teacher': Teacher
#     }
#     @classmethod
#     def create(cls, new_type):
#         return cls.types[new_type]()

class UserFactory(CreateFactory(staff)):
    """Класс фабричный метод"""
    pass


class AbsPrototype:
    """Абстрактный класс прототип"""

    def clone(self):
        return deepcopy(self)


class Course(AbsPrototype):
    """Класс учебный курс, наследуем от прототипа, будем клонировать"""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class LectureCourse(Course):
    pass


courses = types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
        'lecture': LectureCourse,
    }

# class CourseFactory:
#     types = {
#         'interactive': InteractiveCourse,
#         'record': RecordCourse
#     }
#
#     # порождающий паттерн Фабричный метод
#     @classmethod
#     def create(cls, new_type, name, category):
#         return cls.types[new_type](name, category)

class CourseFactory(CreateFactory(courses)):
    """Класс фабричный метод создания курса """
    # переопределим фабричный метод родителя, потому что у подклассов добавляется атрибуты
    @classmethod
    def create(cls, new_type, name, category):
        return cls.types[new_type](name, category)


class Category:
    """Категория курса"""
    category_id = 0

    def __init__(self, name, category):
        self.id = Category.category_id
        Category.category_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    """Класс-движок"""
    def __init__(self):
        # типа база данных
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(user_type):
        return UserFactory.create(user_type)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def get_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'{id} - Нет такой категори.')

    @staticmethod
    def create_course(new_type, name, category):
        return CourseFactory.create(new_type, name, category)

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')



class Singleton(type):
    """Класс синглтон"""
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']
        # если класс с таким имене есть возвращаем его, если нет, то создаем
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):
    """Класс логгер наследуем от синглтона чтобы не плодить логеры"""
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(data):
        with open(f'{Logger.name}_log.txt', 'a', encoding='utf-8') as file:
            file.writelines(f'{datetime.datetime.now()} - {data}')
