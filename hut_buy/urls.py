from django.urls import path
from django.views.i18n import JavaScriptCatalog
from .views import hut_buy_create, HutBuyList, HutBuyDelete, hut_buy_update, hut_buy_detail

urlpatterns = [
    path('new_hut_buy', hut_buy_create, name='new-hut-buy'),
    path('hut_buy_list', HutBuyList.as_view(), name='hut-buy-list'),
    path('hut_buy/<int:pk>/delete', HutBuyDelete.as_view(), name='delete-hut-buy'),
    path('hut_buy/<int:pk>/update', hut_buy_update, name='update-hut-buy'),
    path('hut_buy/<int:pk>/detail', hut_buy_detail, name='detail-hut-buy'),
    # path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
