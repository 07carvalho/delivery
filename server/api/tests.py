from django.contrib.gis.geos import GEOSGeometry
from django.db import IntegrityError
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from api.models import Partner


class PartnerModelTest(TestCase):

    def create_partner(self, data):
        cnpj = Partner().sanitize_document(data.get('document'))
        coverage_area = GEOSGeometry(str(data.get('coverage_area')))
        address = GEOSGeometry(str(data.get('address')))
        return Partner.objects.create(trading_name=data.get('trading_name'),
                                      owner_name=data.get('owner_name'),
                                      document=cnpj,
                                      coverage_area=coverage_area,
                                      address=address)


    def test_partner_creation(self):
        """test partner creation"""
        data1 = {
            "trading_name": "Adega da Cerveja - Pinheiros",
            "owner_name": "Zé da Silva",
            "document": "82.666.231/0001-01",
            "coverage_area": { 
                "type": "MultiPolygon", 
                "coordinates": [
                    [[[30, 20], [45, 40], [10, 40], [30, 20]]], 
                    [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
                ]
            },
            "address": { 
                "type": "Point",
                "coordinates": [-46.57421, -21.785741]
            },
        }

        partner1 = self.create_partner(data1)
        self.assertTrue(isinstance(partner1, Partner))
        self.assertEqual(partner1.__str__(), partner1.trading_name)


    def test_uniqueness(self):
        """test partner creation and if document/CNPJ is unique"""
        data1 = {
            "trading_name": "Adega da Cerveja - Pinheiros",
            "owner_name": "Zé da Silva",
            "document": "82.666.231/0001-01",
            "coverage_area": { 
                "type": "MultiPolygon", 
                "coordinates": [
                    [[[30, 20], [45, 40], [10, 40], [30, 20]]], 
                    [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
                ]
            },
            "address": { 
                "type": "Point",
                "coordinates": [-46.57421, -21.785741]
            },
        }

        p = Partner.objects.create(trading_name=data1.get('trading_name'),
                                   owner_name=data1.get('owner_name'),
                                   document=Partner().sanitize_document(data1.get('document')),
                                   coverage_area=GEOSGeometry(str(data1.get('coverage_area'))),
                                   address=GEOSGeometry(str(data1.get('address'))))

        data2 = {
            "trading_name": "Adega Emporio",
            "owner_name": "Eduardo Piroco",
            "document": "82.666.231/0001-01",
            "coverage_area": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[-67.83039, -9.95782], [-67.83176, -9.98487],
                      [-67.78627,-9.98825], [-67.78885, -9.95105],
                      [-67.83039, -9.95782]]]
                ]
            },
            "address": {
                "type": "Point",
                "coordinates": [-67.81702,-9.970223]
            }
        }
        with self.assertRaises(IntegrityError):
            partner2 = self.create_partner(data2)


class PartnerListAPIViewTestCase(APITestCase):

    def setUp(self):
        data1 = {
            "trading_name": "Adega da Cerveja - Pinheiros",
            "owner_name": "Zé da Silva",
            "document": "11.666.231/0001-01",
            "coverage_area": { 
                "type": "MultiPolygon", 
                "coordinates": [
                    [[[30, 20], [45, 40], [10, 40], [30, 20]]], 
                    [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
                ]
            },
            "address": { 
                "type": "Point",
                "coordinates": [-46.57421, -21.785741]
            },
        }

        cnpj1 = Partner().sanitize_document(data1.get('document'))
        coverage_area1 = GEOSGeometry(str(data1.get('coverage_area')))
        address1 = GEOSGeometry(str(data1.get('address')))
        p1 = Partner.objects.create(trading_name=data1.get('trading_name'),
                                    owner_name=data1.get('owner_name'),
                                    document=cnpj1,
                                    coverage_area=coverage_area1,
                                    address=address1)
        
        data2 = {
            "trading_name": "Adega Emporio",
            "owner_name": "Eduardo Piroco",
            "document": "22.666.231/0001-01",
            "coverage_area": {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[-67.83039, -9.95782], [-67.83176, -9.98487],
                      [-67.78627,-9.98825], [-67.78885, -9.95105],
                      [-67.83039, -9.95782]]]
                ]
            },
            "address": {
                "type": "Point",
                "coordinates": [-67.81702,-9.970223]
            }
        }

        cnpj2 = Partner().sanitize_document(data2.get('document'))
        coverage_area2 = GEOSGeometry(str(data2.get('coverage_area')))
        address2 = GEOSGeometry(str(data2.get('address')))
        p2 = Partner.objects.create(trading_name=data2.get('trading_name'),
                                    owner_name=data2.get('owner_name'),
                                    document=cnpj2,
                                    coverage_area=coverage_area2,
                                    address=address2)


    def test_list_partner(self):
        partners_list_url = reverse('partners_list')
        response = self.client.get(partners_list_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.data.get('count'))

