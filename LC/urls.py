from django.urls import path

from LC.views import lc_create, LCList, LCDelete, lc_update

urlpatterns = [
    path('new_lc', lc_create, name='new-lc'),
    path('lc_list', LCList.as_view(), name='lc-list'),
    path('lc/<int:pk>/delete', LCDelete.as_view(), name='delete-lc'),
    path('lc/<int:pk>/update', lc_update, name='update-lc'),
    # path('hut_buy/<int:pk>/detail', hut_buy_detail, name='detail-hut-buy'),
    # path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

