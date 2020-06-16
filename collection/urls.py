from django.urls import path
from .views import *
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('add_collection', CollectionCreate.as_view(), name='add-collection'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('collection_list', CollectionListView.as_view(), name='collection-list'),
    # path('payment/<int:pk>/detail', payment_details, name='payment-detail'),
    # path('payment/<int:pk>/update', PaymentUpdateView.as_view(), name='payment-update'),
    path('collection/<int:pk>/delete', CollectionDeleteView.as_view(), name='collection-delete'),
    # path('payment_search/', payment_search, name='payment-search'),
]
