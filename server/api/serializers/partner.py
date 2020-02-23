import json
import geojson
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from api.models import Partner


class PartnerSerializer(serializers.ModelSerializer):


    address = serializers.JSONField(source='get_address')
    coverage_area = serializers.JSONField(source='get_coverage_area')
    document = serializers.CharField(source='get_document')


    class Meta:
        model = Partner
        fields = '__all__'


    document_digit_qty = 14
    default_error_messages = {
        'document_digit_qty': ('The document must have {} digits.').format(document_digit_qty),
        'document_unique': ('There is another partner registered with this document.'),
        'invalid_address': ('The address coordinate is invalid'),
        'invalid_coverage_area': ('Coverage area coordinates are invalids'),
    }


    def validate(self, data):
        """Verify if the partner's document has 14 digits and if is unique"""
        errors = []
        document = data.get('get_document', None)
        address = data.get('get_address', None)
        coverage_area = data.get('get_coverage_area', None)

        if document is not None:
            if len(document) != self.document_digit_qty:
                errors.append({'document_digit_qty': _(self.error_messages['document_digit_qty'])})
            elif Partner.objects.filter(document=document).exists():
                errors.append({'document_unique': _(self.error_messages['document_unique'])})

        if address is not None:
            if not isinstance(geojson.loads(json.dumps(address)), geojson.GeoJSON) \
               or 'type' not in address or 'coordinates' not in address:
                errors.append({'invalid_address': _(self.error_messages['invalid_address'])})
        
        if coverage_area is not None:
            if not isinstance(geojson.loads(json.dumps(coverage_area)), geojson.GeoJSON) \
               or 'type' not in coverage_area or 'coordinates' not in coverage_area:
                errors.append({'invalid_coverage_area': _(self.error_messages['invalid_coverage_area'])})

        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return data

