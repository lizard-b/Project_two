from django.urls import path
from .views import (AdvertsListView,
                    )

urlpatterns = [
    path('', AdvertsListView.as_view(), name='adverts_home'),
]
