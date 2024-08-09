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


from .filters import NewsFilter
from .forms import PostForm
from django.core.cache import cache

from .models import Post, Author, Category
from .tasks import notify_about_new_post
from django.utils.translation import gettext as _


class NewsList(ListView):

    model = Post
    ordering = 'post_time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news')


class PostDetail(DetailView):

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context['is_author'] = self.request.user.username in post.author.user.username
        return context


class NewsSearch(ListView):
    model = Post
    ordering = '-post_time_in'
    template_name = 'news_search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    context_object_name = 'create'

    def form_valid(self, form):
        post = form.save(commit=False)
        today = datetime.date.today()
        post_limit = Post.objects.filter(author=post.author, post_time_in__date=today).count()
        if post_limit >= 3:
            return render(self.request, 'post_limit.html', {'author': post.author})
        if self.request.path == '/news/create/':
            post.post_type = 'NEW'
        post.save()
        notify_about_new_post.delay(post.pk)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'edit'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.user.username != post.author.user.username:
            return render(self.request, 'post_del_upd_restrict.html')
        post.save()
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'delete'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs['pk'])
        if self.request.user.username != post.author.user.username:
            return render(self.request, 'post_del_upd_restrict.html')
        return super().form_valid(form)


class PersonalPage(LoginRequiredMixin, TemplateView):
    template_name = 'news/personal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        if not Author.objects.filter(user=user).exists():
            Author.objects.create(user=user)
    return redirect('/')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-post_time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = _('Now you are subscribed to this category!')

    return render(request, 'subscribe.html', {'category': category, 'message': message})


# Create your views here.
