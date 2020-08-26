from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.core.paginator import Paginator
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from daily_cash.views import create_daily_cash
from .models import Payment
from vouchers.models import BuyVoucher
from organizations.models import Persons
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from core.views import buy_total_amount


class PaymentCreate(LoginRequiredMixin, CreateView):
    form_class = PaymentForm
    template_name = 'payments/payment_add_form.html'
    success_url = '/payment_list'

    def form_valid(self, form):
        form.instance.payed_by = self.request.user
        super().form_valid(form=form)
        voucher = get_object_or_404(Payment, payment_no=form.cleaned_data['payment_no'])
        print(form.cleaned_data['payment_no'])
        if str(voucher.payment_from_account) == 'Daily Cash':
            data = {
                'general_voucher': None,
                'payment_no': voucher,
                'collection_no': None,
                'investment_no': None,
                'description': voucher.voucher_no,
                'type': 'P'
            }
            create_daily_cash(data)
        return HttpResponseRedirect(self.get_success_url())


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_update_form.html'


@login_required()
def payment_details(request, pk):
    payment = Payment.objects.get(id=pk)
    payed_amount_word = string.capwords(num2words(payment.payment_amount))
    context = {
        'payment': payment,
        'payed_amount_word': payed_amount_word,
    }
    return render(request, 'payments/payment_detail.html', context)


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'payments/payment_confirm_delete.html'
    success_url = '/payment_list'


@login_required()
def payment_search(request):
    persons = Persons.objects.all()
    buy_vouchers = BuyVoucher.objects.all()
    buy_voucher = buy_vouchers
    payments = Payment.objects.all()
    name_contains_query = request.GET.get('name_contains')
    phone_number_query = request.GET.get('phone_no')
    voucher_total_price = 0

    if name_contains_query != '' and name_contains_query is not None:
        payments = payments.filter(payed_to__contains=name_contains_query)

    elif phone_number_query != '' and phone_number_query is not None:
        v_id = []
        person = persons.filter(contact_number=phone_number_query)
        for person in person:
            buy_voucher = buy_vouchers.filter(seller_name=person.id)
        for voucher in buy_voucher:
            v_id.append(voucher.id)
        payments = payments.filter(voucher_no_id__in=v_id)

    for voucher in buy_voucher:
        voucher_total_price = voucher_total_price + buy_total_amount(voucher.id)

    total_payed = payments.aggregate(Sum('payment_amount'))
    total_payed = total_payed['payment_amount__sum']
    remaining_amount = 0
    if total_payed is not None:
        remaining_amount = voucher_total_price - total_payed

    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_payed': total_payed,
        'voucher_total_price': voucher_total_price,
        'remaining_amount': remaining_amount
    }
    return render(request, "payments/payment_search_form.html", context)
