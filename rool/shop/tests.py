from http import HTTPStatus
from .models import CatTransport, Transport
from django.test import TestCase
from django.urls import reverse

class GetPagesTestCase(TestCase):
    fixtures = ['transports.json', 'category.json']
    # def setUp(self):
    #     self.category = CatTransport.objects.create(name='Водный транспорт', id=1)
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


