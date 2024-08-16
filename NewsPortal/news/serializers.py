from .models import Post, Author, Category, User
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id',
                  'post_time_in',
                  'title_en_US',
                  'title',
                  'post_text_en_US',
                  'post_text',
                  'post_type',
                  'author',
                  'categories',
                  ]


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id',
                  'user',
                  'user_rating',
                  ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'date_joined',
                  ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  'name_en_US',
                  ]

