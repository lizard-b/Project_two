from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Для удаления всех новостей определенной категории команда имеет вид delnewsfromcat category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы точно хотите удалить все статьи в категории {options["category"]}? yes/no: ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Удалены все новости в категории {category.name}.'))
            # в случае неправильного подтверждения говорим, что в доступе отказано
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория {options["category"]} не найдена.'))
