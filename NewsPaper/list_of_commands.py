from news.models import *

sweet_baby = User.objects.create_user(username='sweet_baby')
aut = Author.objects.create(user=sweet_baby)
aut.user.save()

deep_sea = User.objects.create_user(username='deep_sea')
aut_1 = Author.objects.create(user=deep_sea)
aut.user.save()

wild_fox = User.objects.create_user(username='wild_fox')
aut_1 = Author.objects.create(user=wild_fox)
aut.user.save()

bob_tail = User.objects.create_user(username='bob_tail')
aut_4 = Author.objects.create(user=bob_tail)
aut_4.user.save()

Category.objects.create(name='Soft')
Category.objects.create(name='Hardware')
Category.objects.create(name='DataScience')
Category.objects.create(name='Design')
Category.objects.create(name='Python')
