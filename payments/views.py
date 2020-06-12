from django.shortcuts import render
from django.core.paginator import Paginator
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Payment
from accounts.models import Accounts
from .forms import PaymentForm


# Create your views here.
class PaymentCreate(LoginRequiredMixin, CreateView):
    form_class = PaymentForm
    # model = Payment
    template_name = 'payments/payment_add_form.html'
    # fields = '__all__'

    def form_valid(self, form):
        # account = Accounts.objects.get(pk=form.cleaned_data['payment_from_account'].id)
        # amount = form.cleaned_data['payment_amount']
        # remaining_balance = account.remaining_balance
        # new_remaining_balance = amount + remaining_balance
        # account.remaining_balance = new_remaining_balance
        # account.save()
        print('response')
        return super().form_valid(form)


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 5


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_update_form.html'


def payment_details(request, pk):
    payment = Payment.objects.get(id=pk)
    payed_amount_word = string.capwords(num2words(payment.payment_amount))
    context = {
        'payment': payment,
        'payed_amount_word': payed_amount_word,
    }
    return render(request, 'payments/payment_Detail.html', context)


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'payments/payment_confirm_delete.html'
    success_url = '/payment_list'


def payment_search(request):
    payments = Payment.objects.all()
    name_contains_query = request.GET.get('name_contains')

    if name_contains_query != '' and name_contains_query is not None:
        payments = payments.filter(payed_to__contains=name_contains_query)
    paginator = Paginator(payments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, "payments/payment_search_form.html", context)