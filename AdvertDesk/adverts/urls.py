from django.urls import path

from .models import Response
from .views import (AdvertsListView, AdvertsDetailView, AdvertsByCategoryListView, AdvertCreateView, AdvertUpdateView,
                    AdvertDeleteView, ResponseCreateView,
                    )

urlpatterns = [
    path('', AdvertsListView.as_view(), name='adverts_home'),
    path('adverts/create/', AdvertCreateView.as_view(), name='adverts_create'),
    path('adverts/<str:slug>/update/', AdvertUpdateView.as_view(), name='adverts_update'),
    path('adverts/<str:slug>/delete/', AdvertDeleteView.as_view(), name='adverts_delete'),
    path('adverts/<str:slug>/', AdvertsDetailView.as_view(), name='adverts_detail'),
    path('adverts/<int:pk>/responses/create/', ResponseCreateView.as_view(), name='response_create_view'),
    path('category/<str:slug>/', AdvertsByCategoryListView.as_view(), name='adverts_by_category'),
]
