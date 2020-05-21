from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import OrganizationsFrom
from .models import Organizations


# Create your views here.
@login_required()
def add_organizations(request):
    form = OrganizationsFrom()
    if request.method == 'POST':
        form = OrganizationsFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/organizations_list')
    context = {'form': form}
    return render(request, 'organizations/organizations_add.html', context)