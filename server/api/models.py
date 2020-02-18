import json
from django.contrib.gis.db import models


class Partner(models.Model):

    class Meta:
        app_label = 'api'
        constraints = [
            models.UniqueConstraint(fields=['document'], name='unique document')
        ]


    trading_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    document = models.CharField('CNPJ', max_length=14)
    coverage_area = models.MultiPolygonField()
    address = models.PointField()


    def get_address(self):
        return json.loads(self.address.geojson)


    def get_coverage_area(self):
        return json.loads(self.coverage_area.geojson)


    def get_document(self):
        cnpj = self.document
        return '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])


    def sanitize_document(self, document):
        return ''.join(d for d in document if d.isdigit())


    def __str__(self):
        return self.trading_name

