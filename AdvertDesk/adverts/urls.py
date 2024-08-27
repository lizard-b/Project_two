from django.urls import path
from .views import (AdvertsListView, AdvertsDetailView, AdvertsByCategoryListView, AdvertCreateView, AdvertUpdateView,
                    AdvertDeleteView,
                    )

urlpatterns = [
    path('', AdvertsListView.as_view(), name='adverts_home'),
    path('adverts/create/', AdvertCreateView.as_view(), name='adverts_create'),
    path('adverts/<str:slug>/update/', AdvertUpdateView.as_view(), name='adverts_update'),
    path('adverts/<str:slug>/delete/', AdvertDeleteView.as_view(), name='adverts_delete'),
    path('adverts/<str:slug>/', AdvertsDetailView.as_view(), name='adverts_detail'),
    path('category/<str:slug>/', AdvertsByCategoryListView.as_view(), name='adverts_by_category'),
]
