
from views import HomePage, SecondPage, ContactUs

routes = {
        '/': HomePage(),
        '/about/': SecondPage(),
        '/contact/': ContactUs(),
        '/courses/': CoursesList(),
        '/categories/': CategoryList(),
        '/addcourse/': AddCourse(),
        '/addcategory/': AddCategory(),
        '/copycourse/': CopyCourse(),
        }
