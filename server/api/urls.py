from django.urls import path
from api.views import partner

urlpatterns = [
    path('partners/', partner.PartnerList.as_view(), name='partners_list'),
    path('partners/<int:partner_id>/', partner.PartnerDetail.as_view(), name='partner_detail'),
]