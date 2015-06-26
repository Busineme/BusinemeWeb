# -*- coding: utf-8 -*-

from django.test import SimpleTestCase, Client
from models.user import User

STATUS_OK = 200
STATUS_REDIRECT = 302


class UserControllerTest(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        User.objects.all().delete()

    def create_user(self, username):
        self.user = User()
        self.user.username = username
        self.user.set_password('test_password')
        self.user.name = 'test_name'
        self.user.email = 'test@email.tes'
        self.user.save()

    def register_post_data(self, name, email, username, password):
        data = {'name': name,
                'email': email,
                'username': username,
                'password': password}
        return data

    def login_post_data(self, username, password):
        data = {'username': username,
                'password': password}
        return data

    def new_password(self, old_password, new_password):
        data = {'old_password': old_password,
                'new_password1': new_password,
                'new_password2': new_password}
        return data

    def test_register_user_page_loged(self):
        self.create_user('username-0')
        self.client.login(username='username-0', password='test_password')
        response = self.client.get('/cadastro/')
        self.assertEquals(response.status_code, STATUS_REDIRECT)
        self.client.logout()
        self.user.delete()

    def test_register_user_duplicate_email(self):
        data1 = self.register_post_data(
            'test_user1', 'same@email.com', 'test_user1', '1234')
        data2 = self.register_post_data(
            'test_user2', 'same@email.com', 'test_user2', '1234')
        response1 = self.client.post('/cadastrar/usuario/', data1, follow=True)
        response2 = self.client.post('/cadastrar/usuario/', data2, follow=True)

        self.assertEquals(
            response1.redirect_chain, [('http://testserver/login/', 302)])
        self.assertEquals(
            response2.redirect_chain, [])
        self.assertEquals(response1.status_code, STATUS_OK)
        self.assertEquals(response2.status_code, STATUS_OK)

    def test_register_user_invalid_email(self):
        data = self.register_post_data(
            'test_user2', 'testemail.com', 'test_user2', '1234')
        response = self.client.post('/cadastrar/usuario/', data, follow=True)
        self.assertEquals(response.redirect_chain, [])
        self.assertEquals(response.status_code, STATUS_OK)

    def test_register_user_invalid_username(self):
        data1 = self.register_post_data(
            'test_user1', 'test1@email.com', 'test_user_same', '1234')
        data2 = self.register_post_data(
            'test_user2', 'test2@email.com', 'test_user_same', '1234')
        response1 = self.client.post('/cadastrar/usuario/', data1, follow=True)
        response2 = self.client.post('/cadastrar/usuario/', data2, follow=True)

        self.assertEquals(
            response1.redirect_chain, [('http://testserver/login/', 302)])
        self.assertEquals(
            response2.redirect_chain, [])
        self.assertEquals(response1.status_code, STATUS_OK)
        self.assertEquals(response2.status_code, STATUS_OK)

    def test_register_user_page(self):
        response = self.client.get('/cadastro/')
        self.assertEquals(response.status_code, STATUS_OK)

    def test_register_user_success_status_code(self):
        data = self.register_post_data(
            'test_user', 'test@email.com', 'test_user', '1234')
        response = self.client.post('/cadastrar/usuario/', data)
        self.assertEquals(response.status_code, STATUS_REDIRECT)

    def test_register_user_success_db(self):
        data = self.register_post_data(
            'test_user', 'test@email.com', 'test_user', '1234')
        db_before = User.objects.all().count()
        self.client.post('/cadastrar/usuario/', data)
        db_after = User.objects.all().count()
        self.assertTrue(db_after > db_before)

    def test_register_user_blank_passowrd(self):
        data = self.register_post_data(
            'test_user2', 'testemail.com', 'test_user2', '')
        response = self.client.post('/cadastrar/usuario/', data, follow=True)
        self.assertEquals(response.redirect_chain, [])
        self.assertEquals(response.status_code, STATUS_OK)

    def test_loged_user(self):
        self.create_user('username-1')
        self.client.login(username='username-1', password='test_password')
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, STATUS_REDIRECT)
        self.client.logout()
        self.user.delete()

    def test_log_user_post(self):
        self.create_user('username-2')
        response = self.client.post(
            '/login/', self.login_post_data('username-2', 'test_password'))
        self.assertEquals(response.status_code, STATUS_REDIRECT)
        self.client.logout()
        self.user.delete()

    def test_log_user_deactivated(self):
        self.create_user('username-3')
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            '/login/', self.login_post_data('username-3', 'test_password'))
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_log_user_non_existing(self):
        response = self.client.post(
            '/login/', self.login_post_data('username-99', 'test_password'))
        self.assertEquals(response.status_code, STATUS_OK)

    def test_logout_user(self):
        self.create_user('username-4')
        self.client.login(username='username-4', password='test_password')
        response = self.client.get('/sair/')
        self.assertEquals(response.status_code, STATUS_REDIRECT)
        self.client.logout()
        self.user.delete()

    def test_user_account(self):
        self.create_user('username-5')
        self.client.login(username='username-5', password='test_password')
        response = self.client.get('/perfil/')
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_change_password_page(self):
        self.create_user('username-6')
        self.client.login(username='username-6', password='test_password')
        response = self.client.get('/alterar_senha/ ')
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_change_password(self):
        self.create_user('username-7')
        self.client.login(
            username='username-7', password='test_password')
        response = self.client.post(
            '/alterar_senha/', self.new_password('test_password', '1234'))
        self.assertEquals(response.status_code, STATUS_REDIRECT)
        self.client.logout()
        self.user.delete()

    def test_change_password_wrong_old(self):
        self.create_user('username-8')
        self.client.login(
            username='username-8', password='test_password')
        response = self.client.post(
            '/alterar_senha/', self.new_password('wrong', '1234'))
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_change_password_new_unmatch(self):
        self.create_user('username-8')
        self.client.login(
            username='username-8', password='test_password')
        response = self.client.post(
            '/alterar_senha/', {'old_password': 'test_password',
                                'new_password1': 'new_password',
                                'new_password2': 'new_password1'})
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_change_userdata(self):
        self.create_user('username-9')
        self.client.login(
            username='username-9', password='test_password')
        data = self.register_post_data(
            'test_user', 'test@email.com', 'username-7', '1234')
        response = self.client.post('/alterar_dados/', data)
        self.assertEquals(response.status_code, STATUS_REDIRECT)
        self.client.logout()
        self.user.delete()

    def test_deactivate_account_page(self):
        self.create_user('username-10')
        self.client.login(
            username='username-10', password='test_password')
        response = self.client.get('/desativar_perfil/')
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_deactivate_account(self):
        self.create_user('username-11')
        self.client.login(
            username='username-11', password='test_password')
        response = self.client.post(
            '/desativar_perfil/', {'password': 'test_password'})
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_deactivate_account_wrong_password(self):
        self.create_user('username-11')
        self.client.login(
            username='username-11', password='test_password')
        response = self.client.post(
            '/desativar_perfil/', {'password': 'wrong'})
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

    def test_register_user_page_feed(self):
        self.create_user('username-12')
        self.client.login(
            username='username-12', password='test_password')
        response = self.client.get('/')
        self.assertEquals(response.status_code, STATUS_OK)
        self.client.logout()
        self.user.delete()

   

    
