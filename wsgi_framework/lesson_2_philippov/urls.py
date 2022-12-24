
from views import HomePage, SecondPage, ContactUs

routes = {
        '/': HomePage(),
        '/about/': SecondPage(),
        '/contact/': ContactUs(),
        }
