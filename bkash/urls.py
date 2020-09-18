from django.urls import path
from .views import *
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('add_agent', BkashAgentCreate.as_view(), name='add-agent'),
    path('add_transaction', TransactionCreate.as_view(), name='add-transaction'),
    path('bkash/add_person', PersonCreateBkash.as_view(), name='add-person-bkash'),
    path('bkash/add_agent', BkashAgentCreateTransaction.as_view(), name='add-agent-bkash'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('agent_list', BkashAgentList.as_view(), name='agent-list'),
    path('transaction_list', TransactionList.as_view(), name='transaction-list'),
    path('agent_payment_add', AgentPaymentCreate.as_view(), name='agent-payment-add'),
    path('agent_payment_list', AgentPaymentList.as_view(), name='agent-payment-list'),
    path('agent_payment_report', BkashAgentList.as_view(), name='agent-report'),
    # path('payment/<int:pk>/detail', payment_details, name='payment-detail'),
    path('agent/<int:pk>/update', BkashAgentUpdate.as_view(), name='agent-update'),
    path('transaction/<int:pk>/update', TransactionUpdate.as_view(), name='transaction-update'),
    path('agent_payment/<int:pk>/update', AgentPaymentUpdate.as_view(), name='agent-payment-update'),
    path('agent_payment/<int:pk>/delete', AgentPaymentDelete.as_view(), name='agent-payment-delete'),
    path('agent/<int:pk>/delete', AgentDelete.as_view(), name='agent-delete'),
    path('transaction/<int:pk>/delete', TransactionDelete.as_view(), name='transaction-delete'),
    # path('payment_search/', payment_search, name='payment-search'),
]
