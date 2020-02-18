from django.contrib.gis.geos import GEOSGeometry
from django.db import IntegrityError
from django.test import TestCase
from api.models import Partner


class PartnerModelTest(TestCase):

    def create_partner(self, data):
        cnpj = ''.join(d for d in data.get('document') if d.isdigit())
        coverage_area = GEOSGeometry(str(data.get('coverageArea')))
        address = GEOSGeometry(str(data.get('address')))
        return Partner.objects.create(trading_name=data.get('tradingName'),
                                      owner_name=data.get('ownerName'),
                                      document=cnpj,
                                      coverage_area=coverage_area,
                                      address=address)


    def test_partner_creation(self):
        """test partner creation"""
        data1 = {
            "tradingName": "Adega da Cerveja - Pinheiros",
            "ownerName": "Zé da Silva",
            "document": "82.666.231/0001-01",
            "coverageArea": { 
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
            "tradingName": "Adega da Cerveja - Pinheiros",
            "ownerName": "Zé da Silva",
            "document": "82.666.231/0001-01",
            "coverageArea": { 
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

        data2 = {
            "tradingName": "Adega Emporio",
            "ownerName": "Eduardo Piroco",
            "document": "82.666.231/0001-01",
            "coverageArea": {
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

