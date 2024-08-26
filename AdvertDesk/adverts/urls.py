from django.urls import path
from .views import (AdvertsListView, AdvertsDetailView, AdvertsByCategoryListView,
                    )

urlpatterns = [
    path('', AdvertsListView.as_view(), name='adverts_home'),
    path('adverts/<str:slug>/', AdvertsDetailView.as_view(), name='adverts_detail'),
    path('category/<str:slug>/', AdvertsByCategoryListView.as_view(), name='adverts_by_category'),
]
