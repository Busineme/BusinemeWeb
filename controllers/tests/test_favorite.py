
from django.test import SimpleTestCase, Client
from models.user import User
from models.busline import Busline
from models.terminal import Terminal
from models.favorite import Favorite

STATUS_OK = 200
STATUS_REDIRECT = 302


class FavoriteTest(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        User.objects.all().delete()
        Favorite.objects.all().delete()
        Busline.objects.all().delete()

    def create_busline(self):
        Busline.objects.all().delete()
        busline = Busline()
        busline.line_number = "0.001"
        busline.description = "description"
        busline.via = "via"
        busline.route_size = 2.5
        busline.fee = 2.0
        terminal = Terminal(description="terminal")
        terminal.save()
        busline.save()
        busline.terminals.add(terminal)
        return busline

    def create_user(self):
        User.objects.all().delete()
        user = User()
        user.username = "test_username"
        user.set_password('1234')
        user.name = 'test_name'
        user.email = 'test@email.tes'
        user.save()
        return user

    def create_favorite(self):
        Favorite.objects.all().delete()
        favorite = Favorite()
        favorite.user = self.create_user()
        favorite.busline = self.create_busline()
        return favorite

    def test_unfavorite_busline(self):
        self.create_favorite()
        self.client.login(
            username='test_username', password='1234')
        response = self.client.get('/fav/0.001/')
        self.assertEquals(response.status_code, STATUS_REDIRECT)
        self.client.logout()

    def test_favorite_busline(self):
        self.create_busline()
        self.create_user()
        self.client.login(
            username='test_username', password='1234')
        response = self.client.get('/fav/0.001/')
        self.assertEquals(response.status_code, STATUS_REDIRECT)

    def test_unfavorite_busline2(self):
        self.create_busline()
        self.create_user()
        self.client.login(
            username='test_username', password='1234')
        response = self.client.get('/un_fav/0.001/')
        self.assertEquals(response.status_code, STATUS_REDIRECT)


    def test_favorite_busline_page(self):
        self.create_favorite()
        self.client.login(username='test_username', password='1234')
        response = self.client.get('/fav_page/')
        self.assertEquals(response.status_code, STATUS_OK)
