from .models import Post
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'post_time_in', 'title', 'post_text', 'post_type',
                  'author__user__username', 'categories__category__name', ]
