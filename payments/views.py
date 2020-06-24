from django.shortcuts import render
from django.db.models import Sum
from django.core.paginator import Paginator
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Payment
from vouchers.models import BuyVoucher
from organizations.models import Persons
from django.contrib.auth.decorators import login_required
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


@login_required()
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


@login_required()
def payment_search(request):
    persons = Persons.objects.all()
    buy_vouchers = BuyVoucher.objects.all()
    payments = Payment.objects.all()
    name_contains_query = request.GET.get('name_contains')
    voucher_contains_query = request.GET.get('voucher_no')
    phone_number_query = request.GET.get('phone_no')
    total = 0

    if name_contains_query != '' and name_contains_query is not None:
        payments = payments.filter(payed_to__contains=name_contains_query)

    elif phone_number_query != '' and phone_number_query is not None:
        v_id = []
        person = persons.filter(contact_number=phone_number_query)
        for person in person:
            pass
        voucher = buy_vouchers.filter(seller_name=person.id)
        for voucher in voucher:
            v_id.append(voucher.id)
        payments = payments.filter(voucher_no_id__in=v_id)

    elif voucher_contains_query != '' and voucher_contains_query is not 'Choose...':
        buy_voucher = buy_vouchers.filter(voucher_number=voucher_contains_query)
        for voucher in buy_voucher:
            payments = payments.filter(voucher_no_id=voucher.id)
            total = payments.filter(voucher_no_id=voucher.id).aggregate(Sum('payment_amount'))

    paginator = Paginator(payments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'vouchers': buy_vouchers,
        'total': total
    }
    return render(request, "payments/payment_search_form.html", context)


@login_required()
def payment_report(request):
    buy_vouchers = BuyVoucher.objects.all()
    payments = Payment.objects.all()
    voucher_contains_query = request.GET.get('voucher_no')
    total_unloading_cost = 0
    total_self_weight_of_bag = 0
    total_measuring_cost = 0
    total_payed = 0
    total_payable = 0
    payment_due = 0
    payment = []

    if voucher_contains_query != '' and voucher_contains_query is not 'Choose...':
        buy_voucher = buy_vouchers.filter(voucher_number=voucher_contains_query)

        for voucher in buy_voucher:
            payment = payments.filter(voucher_no_id=voucher.id)
            total_payed = payments.filter(voucher_no_id=voucher.id).aggregate(Sum('payment_amount'))
            rate = voucher.rate
            total_weight = voucher.number_of_bag * voucher.weight_per_bag

            if voucher.weight_of_each_bag is not None:
                total_self_weight_of_bag = voucher.weight_of_each_bag * voucher.number_of_bag

            if voucher.per_bag_unloading_cost is not None:
                total_unloading_cost = voucher.per_bag_unloading_cost * voucher.number_of_bag

            if voucher.measuring_cost_per_kg is not None:
                total_measuring_cost = voucher.measuring_cost_per_kg * total_weight

            weight_after_deduction = total_weight - total_self_weight_of_bag
            total_amount = rate*weight_after_deduction
            total_payable = total_amount - total_unloading_cost - total_measuring_cost

        if total_payed != 0 and total_payed['payment_amount__sum'] is not None:
            print(total_payed['payment_amount__sum'])
            payment_due = total_payable-total_payed['payment_amount__sum']

    context = {
        'page_obj': payment,
        'vouchers': buy_vouchers,
        'total_payed': total_payed,
        'total_payable': total_payable,
        'payment_due': payment_due,
        'buy_voucher': voucher_contains_query
    }
    return render(request, "payments/payment_report.html", context)