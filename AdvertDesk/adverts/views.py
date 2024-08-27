from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView )

from .forms import AdvertCreateForm
from .models import Advert, Category, Author


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


class AdvertCreateView(CreateView):
    """
    Представление: создание объявления на сайте
    """
    model = Advert
    template_name = 'adverts/adverts_create.html'
    form_class = AdvertCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление объявления на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = Author.objects.get(pk=self.request.user.id)
        form.save()
        return super().form_valid(form)


class AdvertUpdateView(UpdateView):
    """
    Представление: обновление материала на сайте
    """
    model = Advert
    template_name = 'adverts/adverts_update.html'
    context_object_name = 'advert'
    form_class = AdvertCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление объявления: {self.object.title}'
        return context

    def form_valid(self, form):
        advert = form.save(commit=False)
        title_fob = 'Запрет удаления/редактирования объявления'
        curr_user = advert.author.user.username
        if self.request.user.username != curr_user:
            return render(self.request, 'advert_del_upd_restrict.html', {'title': title_fob,
                                                                         'username': curr_user})
        advert.save()
        return super().form_valid(form)


class AdvertDeleteView(DeleteView):
    """
    Представление: удаления материала
    """
    model = Advert
    success_url = reverse_lazy('adverts_home')
    context_object_name = 'advert'
    template_name = 'adverts/adverts_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление объявления: {self.object.title}'
        return context

    def form_valid(self, form):
        advert = Advert.objects.get(slug=self.kwargs['slug'])
        title_fob = 'Запрет удаления/редактирования объявления'
        curr_user = advert.author.user.username
        if self.request.user.username != curr_user:
            return render(self.request, 'advert_del_upd_restrict.html', {'title': title_fob,
                                                                         'username': curr_user})
        return super().form_valid(form)

# Create your views here.
