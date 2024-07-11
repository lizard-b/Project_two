from django.urls import path
from .views import (NewsList, PostDetail, NewsSearch, PostCreate, PostUpdate,
                    PostDelete, PersonalPage, CategoryListView, subscribe, upgrade_me)
from allauth.account.views import LogoutView, LoginView
from django.views.decorators.cache import cache_page

urlpatterns = [

   path('', NewsList.as_view(), name='post_list'),
   path('news/', cache_page(60*5)(NewsList.as_view()), name='post_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='post'),
   path('news/search/', cache_page(60*5)(NewsSearch.as_view()), name='search'),
   path('news/create/', PostCreate.as_view(), name='create'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='edit'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='delete'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   # path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_edit'),
   # path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
   path('personal/', cache_page(60*1)(PersonalPage.as_view()), name='personal_page'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('logout/', LogoutView.as_view(template_name='news/logout.html'), name='logout'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
