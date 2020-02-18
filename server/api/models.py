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


    def __str__(self):
        return self.trading_name

