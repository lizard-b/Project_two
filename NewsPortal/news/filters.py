from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput


class NewsFilter(FilterSet):
    creation_date = DateFilter(
        field_name='post_time_in',
        widget=DateInput(attrs={'type': 'date'}),
        label='Date',
        lookup_expr='date__gte'
    )

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'title': ['icontains'],

        }
