from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from main.models import ParserCall


class APITestCase(TestCase):
    def setUp(self):
        pass

    def test_add(self):
        data = {
            "phrase": "gtx 4080",
            "region": "simferopol"
        }

        client = APIClient()
        response = client.post('/add/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['uid'] == '65d0e395536ecc745ee26d0a038748d40a2da1de1123f9d54c118e803372fcfc')
        self.assertTrue(response.data['phrase'] == 'gtx 4080')
        self.assertTrue(response.data['region'] == 'simferopol')

    def test_stats(self):
        ParserCall.objects.create(phrase_region_id='65d0e395536ecc745ee26d0a038748d40a2da1de1123f9d54c118e803372fcfc',
                                  phrase='gtx 4080',
                                  region='simferopol',
                                  number_of_ads=6).save()

        data2 = {
            "uid": "65d0e395536ecc745ee26d0a038748d40a2da1de1123f9d54c118e803372fcfc",
            "hours": "42"
        }

        client = APIClient()
        response = client.post('/stats/', data2, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in response.data.items():
            self.assertEqual(v, {'query': 'gtx 4080', 'region': 'simferopol', 'number_of_ads': 6})


class ParserTestCase(TestCase):
    def setUp(self):
        pass

    def test_start_parser(self):
        pass

    def test_periodic_parsing(self):
        pass
