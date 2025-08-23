from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class RegisterUserTest(TestCase):

    def setUp(self):
        self.data = {
            'username': 'rool',
            'city': 'Moscow',
            'birth_date': '2005-03-11',
            'email': 'rool@aks.com',
            'password1': 'jjisjd11',
            'password2': 'jjisjd11',
        }
        self.datas = {
            'username': 'rool',
            'password': 'pipipipi'
        }
        self.user = {
            'username': 'rool',
            'city': 'Minsk',
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTSDZkJpfJZuBUtCO2O5POp69VoIKklbXpFg&s',
            'email': 'tert@gmail.com',
        }

        self.update_user = {
            'username': 'rool',
            'password1': 'piupiu1',
            'password2': 'piupiu1',
        }

    def test_form_reg(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_form_reg_suc(self):
        user_model = get_user_model()
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_pass_error(self):
        self.data['password2'] = 'jijidw'
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают.')

    def test_user_registration_fail(self):
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        path = reverse('users:register')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_form_login(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_login_suc(self):
        user_model = get_user_model()
        user_model.objects.create_user(username=self.datas['username'], password=self.datas['password'])
        path = reverse('users:login')
        response = self.client.post(path, self.datas)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_login_fail(self):
        user_model = get_user_model()
        user_model.objects.create(username=self.datas['username'], password=self.datas['password'])
        path = reverse('users:login')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_password_resert_fail_pass(self):
        self.data['password2'] = 'jijidw'
        path = reverse('users:password_reset')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_password_resert_fail_username(self):
        self.data['username'] = 'jiejw'
        path = reverse('users:password_reset')
        response = self.client.post(path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь не найден')


    def test_user_profile(self):
        path = reverse('users:profile')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
