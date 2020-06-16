from django.urls import path
from .views import *
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('add_collection', CollectionCreate.as_view(), name='add-collection'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('collection_list', CollectionListView.as_view(), name='collection-list'),
    path('collection/<int:pk>/detail', payment_details, name='collection-detail'),
    path('collection/<int:pk>/update', CollectionUpdateView.as_view(), name='collection-update'),
    path('collection/<int:pk>/delete', CollectionDeleteView.as_view(), name='collection-delete'),
    # path('payment_search/', payment_search, name='payment-search'),
]
