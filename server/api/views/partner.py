from django.db import transaction
from django.contrib.gis.geos import GEOSGeometry
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Partner
from api.serializers.partner import PartnerSerializer


class PartnerList(generics.ListCreateAPIView):

    description = 'This route is used to filter the nearest partners and to create a new partner.'
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()


    def get(self, request, *args, **kwargs):
        """
        List Partners
        """
        serializer = PartnerSerializer(self.get_queryset(), many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


    def create(self, request, *args, **kwargs):
        """
        Create a partner instance
        """
        data = request.data
        if data.get('document', None) is not None:
            data['document'] = Partner().sanitize_document(data.get('document'))

        serializer = PartnerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        
        try:
            coverage_area = GEOSGeometry(str(data.get('coverage_area')))
            address = GEOSGeometry(str(data.get('address')))

            partner = Partner.objects.create(trading_name=data.get('trading_name'),
                                             owner_name=data.get('owner_name'),
                                             document=data.get('document'),
                                             coverage_area=coverage_area,
                                             address=address)
            serializer = PartnerSerializer(partner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise serializers.ValidationError({'invalid_location': _('Something went wrong. Verify the coordinates and try again.')})


class PartnerDetail(APIView):
    """
    Get, update or delete a partner.
    """

    description = 'This route is used to get, update or delete a partner.'
    permission_classes = ()

    def get_object(self, partner_id):
        try:
            obj = Partner.objects.get(pk=partner_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except Partner.DoesNotExist:
            raise serializers.ValidationError({'not_found': _('This partner does not exist.')})


    def get(self, request, partner_id, format=None):
        partner = self.get_object(partner_id)
        serializer = PartnerSerializer(partner)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, partner_id, format=None):
        data = request.data

        if data.get('document', None) is not None:
            data['document'] = Partner().sanitize_document(data.get('document'))

        serializer = PartnerSerializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        partner = self.get_object(partner_id)
        with transaction.atomic():
            partner.trading_name = data.get('trading_name', partner.trading_name)
            partner.owner_name = data.get('owner_name', partner.owner_name)
            partner.document = data.get('document', partner.document)
            partner.address = GEOSGeometry(str(data.get('address'))) if data.get('address', None) else partner.address
            partner.address = GEOSGeometry(str(data.get('coverage_area'))) if data.get('coverage_area', None) else partner.coverage_area
            partner.save()

            serializer = PartnerSerializer(partner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, request, partner_id, format=None):
        partner = self.get_object(partner_id)
        with transaction.atomic():
            partner.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)