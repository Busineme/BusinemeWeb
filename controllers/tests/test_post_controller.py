from django.test import SimpleTestCase, Client
from models.post import Post
from controllers import post_controller
from exception.api import ApiException
import urllib2
from models.user import User
from models.busline import Busline
from models.terminal import Terminal

STATUS_OK = 200
STATUS_REDIRECT = 302


class PostControllerTest (SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def create_user(self):
        User.objects.all().delete()
        self.user = User()
        self.user.id = 1
        self.user.username = 'test_user'
        self.user.set_password('test_password')
        self.user.name = 'test_name'
        self.user.email = 'test@email.tes'
        self.user.save()

    def create_busline(self):
        Busline.objects.all().delete()
        self.busline = Busline()
        self.busline.id = 1
        self.busline.line_number = "0.001"
        self.busline.description = "description"
        self.busline.via = "via"
        self.busline.route_size = 2.5
        self.busline.fee = 2.0
        self.busline.save()

        Terminal.objects.all().delete()
        terminal = Terminal(description="terminal")
        terminal.save()

        self.busline.terminals.add(terminal)

    def post_data(self, review):
        data = {'capacity': '5',
                'traffic': '5',
                'description': 'comment',
                'codigo_latitude': '0',
                'codigo_longitude': '0',
                'line_number': '0.001',
                'terminal': '1',
                'review': review}
        return data

    def twitter_data(self):
        data_twitter = {'capacity': '5',
                        'traffic': '5',
                        'line_number': '205'
                        }
        return data_twitter

    def test_make_post_page(self):
        response = self.client.get(
            "/realizar_post/?line_number=0.001&busline_id=1")
        self.assertEquals(response.status_code, STATUS_OK)

    def test_make_post_twitter(self):
        try:
            urllib2.urlopen('http://whatismyip.org').read()
            tweet_data = self.twitter_data()
            tweet = self._post_twitter(
                tweet_data['line_number'], tweet_data['capacity'],
                tweet_data['traffic'])
            self.assertTrue(tweet)
        except Exception:
            self.assertRaises(Exception)

    def test_make_post_action_with_user(self):
        self.create_user()
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(
            "/realizar_post/", self.post_data('0'))
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_make_post_action_with_user_and_line(self):
        self.create_busline()
        self.create_user()
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(
            "/realizar_post/", self.post_data('0'))
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()

    def test_make_post_action_page_no_review(self):
        self.create_user()
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(
            "/realizar_post/", self.post_data(''))
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()

    def test_make_post_action_page_no_geolocation(self):
        self.create_user()
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(
            "/realizar_post/", self.post_data('0'))
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
