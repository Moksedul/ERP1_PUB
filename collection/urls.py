from django.urls import path
from .views import *
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('add_collection_sale', CollectionCreateSale.as_view(), name='add-collection-sale'),
    path('add_collection_local_sale', CollectionCreateLocalSale.as_view(), name='add-collection-local-sale'),
    path('collection/add_person', PersonCreateCollection.as_view(), name='add-person-collection'),
    path('load_sale_vouchers/', load_sale_vouchers, name='load-sale-vouchers'),
    path('load_local_sale_vouchers/', load_local_sale_vouchers, name='load-local-sale-vouchers'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('collection_list', CollectionListView.as_view(), name='collection-list'),
    path('collection/<int:pk>/detail', collection_details, name='collection-detail'),
    path('collection/<int:pk>/update_sale', CollectionUpdateViewSale.as_view(), name='collection-update-sale'),
    path('collection/<int:pk>/update_local_sale', CollectionUpdateViewLocalSale.as_view(), name='collection-update-local-sale'),
    path('collection/<int:pk>/delete', CollectionDeleteView.as_view(), name='collection-delete'),
]
