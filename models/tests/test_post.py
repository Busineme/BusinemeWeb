# -*- coding: utf-8 -*-

from django.test import SimpleTestCase
from models.busline import Busline
from models.user import User
from models.terminal import Terminal
from models.post import Post
from exception.api import ApiException


class BuslineTest(SimpleTestCase):

    def setUp(self):
        Terminal.objects.all().delete()
        Busline.objects.all().delete()
        User.objects.all().delete()
        Post.objects.all().delete()

    def create_busline(self, line_number):
        busline = Busline()
        busline.line_number = line_number
        busline.description = "description"
        busline.via = "via"
        busline.route_size = 2.5
        busline.fee = 2.0
        terminal = Terminal(description="terminal")
        terminal.save()
        busline.save()
        busline.terminals.add(terminal)
        self.busline_id = busline.id
        return busline

    def create_user(self, username):
        user = User()
        user.username = username
        user.password = 'test_password'
        user.name = 'test_name'
        user.email = 'test@email.tes'
        user.save()
        return user

    def create_post(self, line_number, username):
        try:
            busline = self.create_busline(line_number)
            self.busline_same = busline
        except:
            busline = self.busline_same
        user = self.create_user(username)
        terminal = Terminal()
        terminal.description = 'teste'
        terminal.save()
        post = Post()
        post.comment = 'comentario'
        post.latitude = '0'
        post.longitude = '0'
        post.traffic = '3'
        post.capacity = '3'
        post.date = '01/01/01'
        post.time = '00:00'
        post.busline = busline
        post.user = user
        post.terminal_id = terminal.id
        post.save()
        return post

    def test_post_all(self):
        self.create_post('001', 'username')
        posts = Post.all()
        self.assertEquals(1, len(posts))

    def test_post_instance(self):
        post = Post()
        self.assertIsNotNone(post)

    def test_post_unicode(self):
        post = self.create_post('001', 'username')
        id = str(post.id)
        date = str(post.date)
        time = str(post.time)
        busline_id = str(post.busline.id)
        self.assertEquals(
            "id: " + id + " date: " + date + " " + time + " busline: " +
            busline_id + "", post.__unicode__())

    def test_post_all_empty(self):
        post = Post.all()
        self.assertEquals(0, len(post))

    def test_all_exception(self):
        Post.all()
        self.assertRaises(ApiException)

    def test_post_last_equals(self):
        self.create_post('001', 'username')
        post1 = Post.last(self.busline_id)
        self.create_post('001', 'username2')
        post2 = Post.last(self.busline_id)
        self.assertEquals(post1.busline, post2.busline)

    def test_post_last_differs(self):
        self.create_post('001', 'username')
        post1 = Post.last(self.busline_id)
        self.create_post('002', 'username2')
        post2 = Post.last(self.busline_id)
        self.assertNotEqual(post1.busline, post2.busline)
