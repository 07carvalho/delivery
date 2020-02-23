from django.urls import path, register_converter
from api.views import partner
from api.converters import FloatConverter

register_converter(FloatConverter, 'float')

urlpatterns = [
    path('partners/', partner.PartnerList.as_view(), name='partners_list'),
    path('partners/<int:partner_id>/', partner.PartnerDetail.as_view(), name='partner_detail'),
    path('partners/<float:lat>,<float:lng>/', partner.PartnerDetail.as_view(), name='partner_detail'),
]

