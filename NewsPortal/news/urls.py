from django.urls import path
from .views import (NewsList, PostDetail, NewsSearch, PostCreate, PostUpdate, PostDelete)


urlpatterns = [

   path('', NewsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('news/search/', NewsSearch.as_view(), name='search'),
   path('news/create/', PostCreate.as_view(), name='create'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='edit'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='delete'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
]
