from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.core.paginator import Paginator

from django.utils.timezone import now

from core.digit2words import d2w
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from LC.models import LC
from ledger.models import AccountLedger

from ledger.views import create_account_ledger

from .models import Payment
from vouchers.models import BuyVoucher
from organizations.models import Persons
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from core.views import buy_details_calc


def load_buy_vouchers(request):
    name = request.GET.get('name')
    vouchers = []
    if name != '':
        # person = Persons.objects.get(id=name)
        vouchers = BuyVoucher.objects.filter(seller_name=name).order_by('id')
    context = {
        'vouchers': vouchers,
    }
    return render(request, 'payments/voucher_dropdown_list_options.html', context)


# person creation from Payment form
class PersonCreatePayment(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'organizations/person_add.html'
    success_url = '/add_payment'


class PaymentCreate(LoginRequiredMixin, CreateView):
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'
    success_url = '/payment_list'

    def form_valid(self, form):
        form.instance.payed_by = self.request.user
        super().form_valid(form=form)
        voucher = get_object_or_404(Payment, id=self.object.id)
        data = {
            'general_voucher': None,
            'payment_no': voucher,
            'collection_no': None,
            'investment_no': None,
            'bk_payment_no': None,
            'salary_payment': None,
            'description': 'for buy',
            'type': 'P',
            'date': voucher.payment_date
        }
        create_account_ledger(data)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'New Payment'
        context['button_name'] = 'Save'
        context['tittle'] = 'New Payment'
        return context


class LCPaymentCreate(LoginRequiredMixin, CreateView):
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'
    success_url = '/payment_list'

    def form_valid(self, form):
        form.instance.payed_by = self.request.user
        super().form_valid(form=form)
        voucher = get_object_or_404(Payment, payment_no=form.cleaned_data['payment_no'])
        data = {
            'general_voucher': None,
            'payment_no': voucher,
            'collection_no': None,
            'investment_no': None,
            'bk_payment_no': None,
            'salary_payment': None,
            'description': 'for LC',
            'type': 'P',
            'date': voucher.payment_date
        }
        create_account_ledger(data)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'LC Payment'
        context['button_name'] = 'Save'
        context['tittle'] = 'LC Payment'
        return context


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    ordering = '-date_time_stamp'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_account_ledger_for_payments()
        admin = self.request.user.is_staff
        names = Persons.objects.all()
        lc_selection = LC.objects.all()
        buy_selection = BuyVoucher.objects.all()
        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')
        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'

        voucher_list = {'voucher': []}
        for lc in lc_selection:
            key = "voucher"
            voucher_list.setdefault(key, [])
            voucher_list[key].append({'voucher_no': lc.lc_number})
        for buy in buy_selection:
            key = "voucher"
            voucher_list.setdefault(key, [])
            voucher_list[key].append({'voucher_no': buy.voucher_number})
        today = now()
        context['names'] = names
        context['sale_voucher_selection'] = voucher_list['voucher']
        context['voucher_selected'] = voucher_contains
        context['name_selected'] = name_contains
        context['phone_no_selected'] = phone_no_contains
        context['tittle'] = 'Payment List'
        context['today'] = today
        context['admin'] = admin
        return context

    def get_queryset(self):
        lcs = LC.objects.all()
        buys = BuyVoucher.objects.all()
        payments = Payment.objects.all().order_by('-date_time_stamp')
        voucher_contains = self.request.GET.get('voucher_no')
        if voucher_contains is None:
            voucher_contains = 'Select Voucher'
        name_contains = self.request.GET.get('name')
        if name_contains is None:
            name_contains = 'Select Name'
        phone_no_contains = self.request.GET.get('phone_no')

        if phone_no_contains is None or phone_no_contains == '':
            phone_no_contains = 'Select Phone No'

        # checking name from input
        if name_contains != 'Select Name':
            person = Persons.objects.get(person_name=name_contains)
            payments = payments.filter(payment_for_person=person.id)

        # checking phone no from input
        if phone_no_contains != 'Select Phone No' and phone_no_contains != 'None':
            person = Persons.objects.get(contact_number=phone_no_contains)
            payments = payments.filter(payment_for_person=person.id)

        # checking voucher number from input
        if voucher_contains != '' and voucher_contains != 'Select Voucher':
            lcs = lcs.filter(lc_number=voucher_contains)
            if lcs:
                payments = payments.filter(lc_number__in=lcs)
            else:
                buys = buys.filter(voucher_number=voucher_contains)
                payments = payments.filter(voucher_no__in=buys)
        payments_final = payments
        return payments_final


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Payment Update'
        context['button_name'] = 'Update'
        context['tittle'] = 'Payment Update'
        return context


class LCPaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'LC Payment Update'
        context['button_name'] = 'Update'
        context['tittle'] = 'LC Payment Update'
        return context


@login_required()
def payment_details(request, pk):
    payment = Payment.objects.get(id=pk)
    payed_amount_word = d2w(payment.payment_amount)
    context = {
        'payment': payment,
        'payed_amount_word': payed_amount_word,
        'tittle': 'Payment Details'
    }
    return render(request, 'payments/payment_detail.html', context)


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'main/confirm_delete.html'
    success_url = '/payment_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Payment'
        context['tittle'] = 'Payment Delete'
        context['cancel_url'] = '/payment_list'
        return context


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
        voucher_total_price = voucher_total_price + buy_details_calc(voucher.id)

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


def update_account_ledger_for_payments():
    vouchers = Payment.objects.all()
    for voucher in vouchers:
        try:
            account_ledger = AccountLedger.objects.get(payment_no=voucher.id)
        except AccountLedger.DoesNotExist:
            account_ledger = None
        if not account_ledger:
            data = {
                'general_voucher': None,
                'payment_no': voucher,
                'collection_no': None,
                'investment_no': None,
                'bk_payment_no': None,
                'salary_payment': None,
                'description': 'for buy',
                'type': 'P',
                'date': voucher.payment_date
            }
            create_account_ledger(data)
            print('updated-' + str(voucher.id))


def delete_account_ledger_for_payments():
    vouchers = Payment.objects.all()
    account_ledger = AccountLedger.objects.filter(payment_no__in=vouchers)
    for a in account_ledger:
        a.delete()
        print(a.id)
