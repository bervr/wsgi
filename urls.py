
from views import HomePage, SecondPage, ContactUs, CoursesList, CategoryList, AddCourse, AddCategory, CopyCourse

routes = {
        '/about/': SecondPage(),
        '/contact/': ContactUs(),
        '/courses/': CoursesList(),
        '/addcourse/': AddCourse(),
        '/addcategory/': AddCategory(),
        '/copycourse/': CopyCourse(),
        }
