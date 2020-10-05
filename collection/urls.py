from django.urls import path
from .views import *
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('add_collection_sale', CollectionCreateSale.as_view(), name='add-collection-sale'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('collection_list', CollectionListView.as_view(), name='collection-list'),
    path('collection/<int:pk>/detail', collection_details, name='collection-detail'),
    path('collection/<int:pk>/update', CollectionUpdateView.as_view(), name='collection-update'),
    path('collection/<int:pk>/delete', CollectionDeleteView.as_view(), name='collection-delete'),
    path('collection/report', collection_report, name='collection-report'),
    path('collection_search/', collection_search, name='collection-search'),
]
