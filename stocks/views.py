from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Stocks


# Create your views here.
class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stocks
    template_name = 'stocks/stock_form.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


def stock_view(request):
    stocks = Stocks.objects.all()
    all_weights = []
    for stock in stocks:
        all_weights.append(stock.weight)
    total_weight = sum(all_weights)
    context = {"total_weight": int(total_weight)}
    return render(request, 'stocks/report.html', context)


class StockListView(LoginRequiredMixin, ListView):
    model = Stocks
    template_name = 'stocks/stock_list.html'
    context_object_name = 'stocks'
    paginate_by = 20


class StockUpdateView(LoginRequiredMixin, UpdateView):
    model = Stocks
    template_name = 'stocks/stock_update_form.html'
    fields = '__all__'


class StockDeleteView(LoginRequiredMixin, DeleteView):
    model = Stocks
    template_name = 'stocks/stock_confirm_delete.html'
    success_url = '/stock_list'
