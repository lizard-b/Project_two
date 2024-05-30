from news.models import *

User.objects.create_user('sweet_baby')

User.objects.create_user('wild_fox')

Author.objects.create()

Author.objects.create()

Category.objects.create(name='Soft')
Category.objects.create(name='Hardware')
Category.objects.create(name='DataScience')
Category.objects.create(name='Design')
