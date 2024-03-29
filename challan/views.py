from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from organizations.models import Persons, Companies, Organization
from .models import Challan
from .forms import ChallanForm


# company creation from Challan form
class CompanyCreateChallan(LoginRequiredMixin, CreateView):
    model = Companies
    fields = '__all__'
    template_name = 'organizations/companies_form.html'
    success_url = '/add_challan'


# person creation from Challan form
class PersonCreateChallan(LoginRequiredMixin, CreateView):
    model = Persons
    fields = '__all__'
    template_name = 'organizations/person_add.html'
    success_url = '/add_challan'


class ChallanCreateView(LoginRequiredMixin, CreateView):
    form_class = ChallanForm
    template_name = 'challan/challan_form.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'New Challan'
        context['button_name'] = 'Save'
        context['tittle'] = 'New Challan'
        return context


class ChallanUpdateView(LoginRequiredMixin, UpdateView):
    model = Challan
    form_class = ChallanForm
    template_name = 'challan/challan_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_name'] = 'Update Challan'
        context['button_name'] = 'Update'
        context['tittle'] = 'Update Challan'
        return context


class ChallanListView(LoginRequiredMixin, ListView):
    model = Challan
    template_name = 'challan/challan_list.html'
    context_object_name = 'challan'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challan_selection = Challan.objects.all()
        business = Organization.objects.all()
        company_names = Companies.objects.all()

        challan_contains = self.request.GET.get('challan_no')
        if challan_contains is None:
            challan_contains = 'Select Challan'

        business_contains = self.request.GET.get('business')
        if business_contains is None:
            business_contains = 'Select Business'

        company_name_contains = self.request.GET.get('company_name')
        if company_name_contains is None or company_name_contains == '':
            company_name_contains = 'Select Company Name'

        today = now()

        context['business'] = business
        context['company_names'] = company_names
        context['challan_selected'] = challan_contains
        context['challan_selection'] = challan_selection
        context['business_selected'] = business_contains
        context['company_name_selected'] = company_name_contains
        context['tittle'] = 'Challan List'
        context['today'] = today
        return context

    def get_queryset(self):
        challans = Challan.objects.all().order_by('-challan_date')
        order = self.request.GET.get('orderby')
        challan_contains = self.request.GET.get('challan_no')
        if challan_contains is None:
            challan_contains = 'Select Challan'

        business_contains = self.request.GET.get('business')
        if business_contains is None:
            business_contains = 'Select Business'

        company_name_contains = self.request.GET.get('company_name')
        if company_name_contains is None or company_name_contains == '':
            company_name_contains = 'Select Company Name'

        # checking name from input
        if business_contains != 'Select Business':
            business = Organization.objects.get(name=business_contains)
            challans = challans.filter(business_name=business.id)

        # checking phone no from input
        if company_name_contains != 'Select Company Name' and company_name_contains != 'None':
            company = Companies.objects.get(name_of_company=company_name_contains)
            challans = challans.filter(company_name=company.id)

        # checking voucher number from input
        if challan_contains != '' and challan_contains != 'Select Challan':
            challans = challans.filter(challan_serial=challan_contains)
        return challans

    def get_paginate_by(self, queryset):
        page = self.request.GET.get("paginated_by")
        if page is None:
            pass
        elif page == 'None':
            self.paginate_by = None
        else:
            self.paginate_by = page
        return self.paginate_by


class ChallanDeleteView(LoginRequiredMixin, DeleteView):
    model = Challan
    template_name = 'main/confirm_delete.html'
    success_url = '/challan_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'Challan'
        context['tittle'] = 'Challan Delete'
        context['cancel_url'] = '/challan_list'
        return context


@login_required
def challan_detail(request, pk):
    challan = Challan.objects.get(id=pk)
    driver_name = challan.name_of_driver
    challan_serial = challan.challan_serial.split('-')[-1]
    mode = request.GET.get('mode')

    template = 'challan/challan_detail_no_bg.html'
    if mode == 'pad':
        template = 'challan/challan_detail_bg.html'

    if driver_name is None:
        driver_name = ''

    context = {
        'object': challan,
        'driver_name': driver_name,
        'challan_serial': challan_serial,
        'mode': mode

    }
    return render(request, template, context=context)