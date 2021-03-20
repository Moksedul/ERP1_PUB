from django.urls import path

from LC.views import lc_create, LCList

urlpatterns = [
    path('new_lc', lc_create, name='new-lc'),
    path('lc_list', LCList.as_view(), name='lc-list'),
    # path('hut_buy/<int:pk>/delete', HutBuyDelete.as_view(), name='delete-hut-buy'),
    # path('hut_buy/<int:pk>/update', hut_buy_update, name='update-hut-buy'),
    # path('hut_buy/<int:pk>/detail', hut_buy_detail, name='detail-hut-buy'),
    # path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

