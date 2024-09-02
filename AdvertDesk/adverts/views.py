from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)

from .forms import AdvertCreateForm, ResponseCreateForm
from .models import Advert, Category, Author, Response
from modules.services.mixins import AuthorRequiredMixin, EmailConfirmedMixin


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
        context['form'] = ResponseCreateForm
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


class AdvertCreateView(LoginRequiredMixin, EmailConfirmedMixin, CreateView):
    """
    Представление: создание объявления на сайте
    """
    model = Advert
    template_name = 'adverts/adverts_create.html'
    form_class = AdvertCreateForm
    login_url = 'adverts_home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление объявления на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = Author.objects.get(pk=self.request.user.id)
        form.save()
        return super().form_valid(form)


class AdvertUpdateView(AuthorRequiredMixin, SuccessMessageMixin, EmailConfirmedMixin, UpdateView):
    """
    Представление: обновление материала на сайте
    """
    model = Advert
    template_name = 'adverts/adverts_update.html'
    context_object_name = 'advert'
    form_class = AdvertCreateForm
    login_url = 'adverts_home'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление объявления: {self.object.title}'
        return context

    def form_valid(self, form):
        advert = form.save(commit=False)
        title_fob = 'Запрет удаления/редактирования объявления'
        curr_user = advert.author.user.username
        if self.request.user.username != curr_user:
            return render(self.request, 'adverts/advert_del_upd_restrict.html', {'title': title_fob,
                                                                                 'username': curr_user})
        advert.save()
        return super().form_valid(form)


class AdvertDeleteView(AuthorRequiredMixin, EmailConfirmedMixin, DeleteView):
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
            return render(self.request, 'adverts/advert_del_upd_restrict.html', {'title': title_fob,
                                                                                 'username': curr_user})
        return super().form_valid(form)


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = form.save(commit=False)
        response.article_id = self.kwargs.get('pk')
        response.author = self.request.user
        response.parent_id = form.cleaned_data.get('parent')
        response.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': response.is_child_node(),
                'id': response.id,
                'author': response.author.username,
                'parent_id': response.parent_id,
                'time_create': response.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                'avatar': response.author.profile.avatar.url,
                'response_text': response.content,
                'get_absolute_url': response.author.profile.get_absolute_url()
            }, status=200)

        return redirect(response.article.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления откликов'}, status=400)

# Create your views here.
