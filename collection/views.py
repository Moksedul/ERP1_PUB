from django.shortcuts import render
from django.db.models import Sum
from django.core.paginator import Paginator
import string
from num2words import num2words
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Collection
from vouchers.models import BuyVoucher
from django.contrib.auth.decorators import login_required
from accounts.models import Accounts
from .forms import CollectionForm


class CollectionCreate(LoginRequiredMixin, CreateView):
    form_class = CollectionForm
    template_name = 'collections/collection_add_form.html'


class CollectionListView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'
    paginate_by = 5


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Collection
    template_name = 'collections/collection_confirm_delete.html'
    success_url = '/collection_list'

