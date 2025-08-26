from http import HTTPStatus
from .models import CatTransport, Transport, User, Basket
from django.test import TestCase
from django.urls import reverse


class GetPagesTestCase(TestCase):
    fixtures = ['transports.json', 'category.json']
    user_data = {'username': 'rool', 'password': 'pipipipi'}

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)
        self.product = Transport.objects.first()
        self.add_url = reverse('shop:basket_add', args=[self.product.id])
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=2)
        self.remove_url = reverse('shop:basket_remove', args=[self.basket.id])

    def test_case_1(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_category_page(self):
        path = reverse('shop:category', args=[1])  # category_id=1
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/products.html')

    def test_paginate_mainpage(self):
        page_number = 1
        paginate_by = 12
        path = reverse('shop:paginator', args=[page_number])
        response = self.client.get(path)
        a = Transport.objects.all()
        self.assertQuerySetEqual(
            response.context['transports'].object_list,
            a[(page_number - 1) * paginate_by: page_number * paginate_by]
        )

    def test_add_new_product_to_basket(self):
        response = self.client.post(self.add_url, HTTP_REFERER='/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        basket_item = Basket.objects.get(user=self.user, product=self.product)
        self.assertEqual(basket_item.quantity, 3)  # было 2, после add стало 3

    def test_remove_basket_from_basket(self):
        response = self.client.post(self.remove_url, HTTP_REFERER='/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Basket.objects.filter(id=self.basket.id).exists())

    def test_add_basket_not_auth_user(self):
        self.client.logout()
        response = self.client.post(self.add_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn(reverse('users:login'), response.url)

