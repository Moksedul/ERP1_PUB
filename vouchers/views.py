from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import *


# buy voucher start
class BuyVoucherCreateView(LoginRequiredMixin, CreateView):
    form_class = BuyForm
    template_name = 'vouchers/buyvoucher_add_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class BuyListView(LoginRequiredMixin, ListView):
    model = BuyVoucher
    template_name = 'vouchers/buy_list.html'
    context_object_name = 'vouchers'
    paginate_by = 5


class BuyVoucherUpdateView(LoginRequiredMixin, UpdateView):
    model = BuyVoucher
    template_name = 'vouchers/buyvoucher_update_form.html'
    fields = '__all__'


class BuyDeleteView(LoginRequiredMixin, DeleteView):
    model = BuyVoucher
    success_url = '/buy_list'
# buy voucher end


# sale voucher start
class SaleCreateView(LoginRequiredMixin, CreateView):
    form_class = SaleForm
    template_name = 'vouchers/salevoucher_add_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class SaleListView(LoginRequiredMixin, ListView):
    model = SaleVoucher
    template_name = 'vouchers/sale_list.html'
    context_object_name = 'vouchers'
    paginate_by = 5


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    model = SaleVoucher
    form_class = SaleForm
    template_name = 'vouchers/sale_update_form.html'


class SaleDeleteView(LoginRequiredMixin, DeleteView):
    model = SaleVoucher
    template_name = 'vouchers/sale_confirm_delete.html'
    success_url = '/sale_list'
# sale voucher end


# buy general voucher start
class GeneralVoucherCreateView(LoginRequiredMixin, CreateView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_add_form.html'
    fields = '__all__'


class GeneralVoucherUpdateView(LoginRequiredMixin, UpdateView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_update_form.html'
    fields = '__all__'


class GeneralVoucherListView(LoginRequiredMixin, ListView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_list.html'
    context_object_name = 'vouchers'
    paginate_by = 5


class GeneralVoucherDeleteView(LoginRequiredMixin, DeleteView):
    model = GeneralVoucher
    template_name = 'vouchers/general_voucher_confirm_delete.html'
    success_url = '/general_voucher_list'
# sale general voucher end