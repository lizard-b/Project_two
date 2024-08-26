import datetime

import pytz
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView, TemplateView, )
from .models import Advert, Author, Category


class AdvertsListView(ListView):

    model = Advert
    ordering = 'time_create'
    template_name = 'adverts/adverts_list.html'
    context_object_name = 'adverts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class AdvertsDetailView(DetailView):
    model = Advert
    template_name = 'adverts/adverts_detail.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class AdvertsByCategoryListView(ListView):
    model = Advert
    template_name = 'adverts/adverts_list.html'
    context_object_name = 'adverts'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Advert.objects.all().filter(category__slug=self.category.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Объявления из категории: {self.category.name}'
        return context


# Create your views here.
