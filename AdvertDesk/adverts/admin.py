from django.contrib import admin
from .models import (Category, Advert, AdvertCategory,
                     Author, Response)


admin.site.register(Author)
admin.site.register(Advert)
admin.site.register(Response)
admin.site.register(Category)
admin.site.register(AdvertCategory)


# Register your models here.
