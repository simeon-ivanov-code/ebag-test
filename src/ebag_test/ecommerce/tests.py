from django.test import TestCase
from django.urls import reverse

import json

from .models import *

class SearchTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product1 = Product.objects.create(title='Product 1', description='test', price=10, sku='00001', category=self.category)
        self.product2 = Product.objects.create(title='Product 2', description='test 2', price=5, sku='00002', category=self.category)

    def test_search_view(self):
        response = self.client.get(reverse('search', query={ 'title': '1' }))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/products.html')

    def as_json(self, params):
        return json.dumps(params, default=lambda o: o.__dict__)

    def test_search_api_no_params(self):
        response = self.client.get(reverse('search_api'))
        self.assertEqual(response.status_code, 200)
        response_as_list = json.loads(response.content)
        self.assertEqual(len(response_as_list), 2)

    def check_helper(self, params, expected):
        response = self.client.get(reverse('search_api', query={ 'params': self.as_json(params) }))
        self.assertEqual(response.status_code, 200)
        response_as_list = json.loads(response.content)
        self.assertEqual(len(response_as_list), expected)

    def test_search_api(self):
        params = SearchRequest()
        self.check_helper(params, 2)

    def test_search_api_title_1(self):
        params = SearchRequest()
        params.title = '1'
        self.check_helper(params, 1)

    def test_search_api_title_3(self):
        params = SearchRequest()
        params.title = '3'
        self.check_helper(params, 0)

    def test_search_api_title_sku(self):
        params = SearchRequest()
        params.title = '1'
        params.sku = '00001'
        self.check_helper(params, 1)

    def test_search_api_from_price(self):
        params = SearchRequest()
        params.from_price = 6
        self.check_helper(params, 1)

    def test_search_api_category(self):
        params = SearchRequest()
        params.category = 'Cat'
        self.check_helper(params, 2)

    def test_search_api_all(self):
        params = SearchRequest()
        params.title = 'Product'
        params.sku = '00'
        params.from_price = 6
        params.to_price = 12
        params.category = 'Category'
        params.has_image = False
        self.check_helper(params, 1)
