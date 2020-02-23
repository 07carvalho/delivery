'''
This script load the Delivery database with the partners in docs/pcvs.json
To run just load the enviroment and execute 

python load_partners.py

'''

import json
import os
import django
from django.db import transaction
from django.contrib.gis.geos import GEOSGeometry
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delivery.settings")
django.setup()

from api.models import Partner

with open('../docs/pdvs.json') as json_file:
    data = json.load(json_file)
    for partner in data['pdvs']:
        with transaction.atomic():
            cnpj = ''.join(d for d in partner.get('document')[0:18] if d.isdigit())
            coverage_area = GEOSGeometry(str(partner.get('coverageArea')))
            address = GEOSGeometry(str(partner.get('address')))
            p = Partner.objects.create(trading_name=partner.get('tradingName'),
                                       owner_name=partner.get('ownerName'),
                                       document=cnpj,
                                       coverage_area=coverage_area,
                                       address=address)

