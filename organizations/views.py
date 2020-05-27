from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import OrganizationsFrom
from .models import Persons, Companies


# Create your views here.
# @login_required()
# def add_organizations(request):
#     form = OrganizationsFrom()
#     if request.method == 'POST':
#         form = OrganizationsFrom(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/organization_list')
#     context = {'form': form}
#     return render(request, 'organizations/organizations_add.html', context)
class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)


class PersonListView(LoginRequiredMixin, ListView):
    model = Persons
    template_name = 'organizations/person_list.html'
    context_object_name = 'persons'
    # products = Products.objects.all()
    # return render(request, 'products/buy_list.html', {'products': products})


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    model = Persons
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()


class PersonDeleteView(LoginRequiredMixin, DeleteView):
    model = Persons
    success_url = '/person_list'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Companies
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)


class CompanyListView(LoginRequiredMixin, ListView):
    model = Companies
    template_name = 'organizations/Company_list.html'
    context_object_name = 'companies'
    # products = Products.objects.all()
    # return render(request, 'products/buy_list.html', {'products': products})


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Companies
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Companies
    success_url = '/company_list'