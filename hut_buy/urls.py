from django.urls import path
from django.views.i18n import JavaScriptCatalog
from .views import hut_buy_create

urlpatterns = [
    path('new_hut_buy', hut_buy_create, name='new-hut-buy'),
    # path('local_sale_list', LocalSaleList.as_view(), name='local-sale-list'),
    # path('local_sale/<int:pk>/delete', LocalSaleDelete.as_view(), name='delete-local-sale'),
    # path('local_sale/<int:pk>/update', sale_update, name='update-local-sale'),
    # path('local_sale/<int:pk>/detail', sale_detail, name='detail-local-sale'),
    # path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
