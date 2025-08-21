from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

class GetPagesTestCase(TestCase):

    def test_case_1(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'shop/index.html')
