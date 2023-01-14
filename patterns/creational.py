import datetime
from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect

from patterns.behavior import FileWriter, Subject
from patterns.architectural import DomainObject

class User:
    def __init__(self, name):
        self.name = name


class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class Teacher(User, DomainObject):
    def __init__(self, name):
        super().__init__(name)


staff = {
        'student': Student,
        'teacher': Teacher
    }


class CreateFactory:
    """Абстрактный класс фабричный метод"""
    def __new__(cls, types, *args, **kwargs):
        cls.types = types

    @classmethod
    def create(cls, _type, name):
        return cls.types[_type](name)


class UserFactory(CreateFactory):
    """Класс фабричный метод"""
    types = staff
    pass


class AbsPrototype:
    """Абстрактный класс прототип"""
    def clone(self):
        return deepcopy(self)


class Course(AbsPrototype, Subject):
    """Класс учебный курс, наследуем от прототипа, будем клонировать"""
    count_id  = 0
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        self.id = Course.count_id
        Course.count_id += 1
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student):
        if student not in self.students and self not in student.courses:
            self.students.append(student)
            student.courses.append(self)
            self.notify()


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class LectureCourse(Course):
    pass


courses = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
        'lecture': LectureCourse,
    }


class CourseFactory(CreateFactory):
    """Класс фабричный метод создания курса """
    # переопределим фабричный метод родителя, потому что у подклассов добавляется атрибуты
    types = courses
    @classmethod
    def create(cls, new_type, name, category):
        return cls.types[new_type](name, category)


class Category:
    """Категория курса"""
    count_id = 0

    def __init__(self, name, category):
        self.id = Category.count_id
        Category.count_id += 1
        self.name = name
        self.category = category
        self.courses = []
        self.is_category = True

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

    def get_sub_category(self):
        result = []
        if self.category:
            result.append(self.category.get_sub_category())
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
    def create_user(user_type, name):
        return UserFactory.create(user_type, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def get_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'{id} - Нет такой категори.')

    def get_course_by_id(self, id):
        for course in self.courses:
            if course.id == id:
                return course
        raise Exception(f'{id} - Нет такого курса.')

    @staticmethod
    def create_course(new_type, name, category):
        return CourseFactory.create(new_type, name, category)

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def get_student(self, name):
        for student in self.students:
            if student.name == name:
                return student
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
        # если класс с таким именем есть возвращаем его, если нет, то создаем
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):
    """Класс логгер наследуем от синглтона чтобы не плодить логеры"""
    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, data):
        # with open(f'{self.name}_log.txt', 'a', encoding='utf-8') as file:
        #     file.writelines(f'{datetime.datetime.now()} - {data} \n')
        text = f'{datetime.datetime.now()} - {data} \n'
        self.writer.write(text)


class BaseMapper:
    """
    Маппер для таблицы базы данных
    """
    def __init__(self, connection, tablename, obj_cls):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = tablename
        self.obj = obj_cls

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            item_obj = self.obj(name)
            item_obj.id = id
            result.append(item_obj)
            # student = Student(name)
            # student.id = id
            # result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return self.obj(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class StudentMapper(BaseMapper):
    def __init__(self, connection):
        super().__init__(connection, 'student', Student)


class CourseMapper(BaseMapper):
    def __init__(self, connection):
        super().__init__(connection, 'course', Course)


class CategoryMapper(BaseMapper):
    def __init__(self, connection):
        super().__init__(connection, 'category', Category)



connection = connect('wsgi_db.sqlite')


class MapperRegistry:
    """ архитектурный системный паттерн - Data Mapper """
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


