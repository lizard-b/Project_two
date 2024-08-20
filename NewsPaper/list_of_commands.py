from news.models import *

sweet_baby = User.objects.create_user(username='sweet_baby')
aut = Author.objects.create(user=sweet_baby)

deep_sea = User.objects.create_user(username='deep_sea')
aut_1 = Author.objects.create(user=deep_sea)

wild_fox = User.objects.create_user(username='wild_fox')
aut_2 = Author.objects.create(user=wild_fox)

bob_tail = User.objects.create_user(username='bob_tail')
aut_3 = Author.objects.create(user=bob_tail)

cat1 = Category.objects.create(name='Soft')
cat2 = Category.objects.create(name='Hardware')
cat3 = Category.objects.create(name='DataScience')
cat4 = Category.objects.create(name='Design')
cat5 = Category.objects.create(name='Python')
cat6 = Category.objects.create(name='Games')

post1 = Post.objects.create(post_type=True,
                            title='Python 3.13.0 beta 1 released',
                            post_text='Python 3.13 is still in development. This release,'
                                      ' 3.13.0b1, is the first of four beta release previews '
                                      'of 3.13. Beta release previews are intended to give the'
                                      ' wider community the opportunity to test new features and'
                                      ' bug fixes and to prepare their projects to support the new'
                                      ' feature release. We strongly encourage maintainers of third-party'
                                      ' Python projects to test with 3.13 during the beta phase and report'
                                      ' issues found to the Python bug tracker as soon as possible.'
                                      ' While the release is planned to be feature complete entering'
                                      ' the beta phase, it is possible that features may be modified or,'
                                      ' in rare cases, deleted up until the start of the release candidate'
                                      ' phase (Tuesday 2024-07-30). Our goal is to have no ABI changes'
                                      ' after beta 4 and as few code changes as possible after'
                                      ' 3.13.0rc1, the first release candidate. To achieve that,'
                                      ' it will be extremely important to get as much exposure'
                                      ' for 3.13 as possible during the beta phase. Please keep in mind'
                                      ' that this is a preview release and its use is not recommended'
                                      ' for production environments.',
                            author=aut_3)

post2 = Post.objects.create(title='Анонсирована ПК-версия God of War Ragnarok',
                            post_text='На презентации State of Play анонсировали PC-порт God of War Ragnarok.'
                                      ' Высокооцененная игра выйдет на персональных компьютерах уже 19 сентября 2024-го.'
                                      ' О планах Sony презентовать проект в конце мая ранее сообщали инсайдеры.'
                                      ' Экшен был эксклюзивом PlayStation с момента релиза в ноябре 2022-го.'
                                      ' God of War Ragnarok — прямое продолжение God of War 2018 года.'
                                      ' Сюжет рассказывает о новом приключении Кратоса и Атрея. Журналисты и геймеры'
                                      ' остались в восторге от игры — ее средний рейтинг на Metacritic'
                                      ' сейчас равен 94 из 100 и 8,1 из 10 соответственно.'
                                      ' В декабре 2023-го для God of War Ragnarok вышло бесплатное дополнение Valhalla.'
                                      ' Оно добавило «роуглайт»-режим с пятью уровнями сложности.',
                            author=aut)

post3 = Post.objects.create(title='Сколько сегодня стоит мощный игровой ПК для 2К на 5 лет, и почему раньше было дешевле',
                            post_text='Десять лет назад, когда вы покупали мощный игровой компьютер, то тратили'
                                      ' на него порядка 1500 долларов. Бодрый середняк, который вытягивал все новинки в 1080р,'
                                      ' стоил до1000 долларов, ну а сегодня за развлечения приходится платить намного больше.'
                                      ' Это плохая новость, которая так или иначе касается каждого геймера.'
                                      ' К счастью, есть и вторая новость, которая точно придётся по душе любителям компьютерных игр.'
                                      ' Всё дело в том, что технологический прогресс сильно замедлился. Если раньше видеокарты'
                                      ' могли за 10 лет стать в 10 раз быстрее, то сегодня за 3 поколения можно получить'
                                      ' скромный двукратный прирост. Флагманы развиваются быстрее, но цены в данном сегменте заоблачные.'
                                      ' Аналитики полагают, что причин такого явления несколько. Прежде всего виновато обесценивание американской валюты.'
                                      ' Не стоит забывать о возросших аппетитах производителей комплектующих. Кроме того,'
                                      ' свою долю выручки хочет получить и TSMC, монополизировавшая рынок полупроводников и'
                                      ' постоянно повышающая стоимость собственных услуг. Что же, если 15 лет назад вы покупали компьютер за 1500 долларов,'
                                      ' то уже через 2 года он начинал быстро устаревать. Через 4 года ваш процессор казался сродни улитке,'
                                      ' ну а видеокарта отказывалась тянуть новые игры. Сегодня ничего подобного нет, ведь игры медленно наращивают требования,'
                                      ' графика там почти не меняется, ну а видеокарты прибавляют по 30% за 2 года.'
                                      ' Наиболее популярные сегменты и вовсе топчутся на месте, а всё это позволяет нам с вами продлить'
                                      ' жизненный цикл нового компьютера. Новость неоднозначная, но ничего изменить мы с вами не можем,'
                                      ' поэтому остаётся только подобрать такие комплектующие, которые могли бы прослужить вам 5 лет.'
                                      ' Прежде всего отметим, что в 2024 году выйдет две новые линейки процессоров и видеокарт.'
                                      ' Если у вас есть нормальный компьютер, которые терпит замены ещё полгода, то самое время набраться терпения.'
                                      ' Все остальные, уставшие томиться у монитора, могут купить именно такую сборку,'
                                      ' которая останется актуальной даже спустя 5 лет. Остановимся на разрешении 2К,'
                                      ' для которого и будет создан наш компьютер. Пожалуй, единственный процессор,'
                                      ' который мы можем порекомендовать для такой сборки – это Ryzen 7 7800X3D.'
                                      ' Он способен тягаться с флагманами, но имеет невысокие требования.'
                                      ' Ничего более быстрого за эти деньги вы не купите, ну а более мощные решения'
                                      ' потребуют совершенно другой системы охлаждения и материнской платы за 300-500 долларов.'
                                      ' Ну а в данном случае мы можем обратить внимание на продукцию Asrock, построенную на чипсете B650.'
                                      ' Материнская плата не предлагает ничего лишнего. Здесь нет беспроводной связи мощной системы питания,'
                                      ' как нет и массы настроек для диванных оверклокеров. Помните, что разгон Ryzen 7 7800X3D невозможен,'
                                      ' ну а настроить тайминги оперативной платы вы можете при помощи системного приложения.'
                                      ' В итоге вы заплатите немного, но получите отличное решение с потенциалом для апгрейда.'
                                      ' Обычно Asrock в первых рядах выпускает обновления BIOS, что позволит установить'
                                      ' более мощный процессор одного из следующих поколений. Вообще, потенциала Ryzen 7 7800X3D вам точно будет достаточно,'
                                      ' но иногда просто хочется побаловать себя чем-то более современным. Если вы не планируете разгонять оперативную память,'
                                      ' то можете взять линейки попроще, ну а для тех, кто не против экспериментов,'
                                      ' в наличии две линейки по 16 Гб производства Team Group. DDR5-6000 порадует вас отличными скоростными показателями'
                                      ' и низкими для своего класса таймингами. Это не самая лучшая ОЗУ в своём классе, но для тех,'
                                      ' кто не ставит перед собой слишком сложных задач, она точно подойдёт. Мы предлагаем покупать сразу 32 Гб,'
                                      ' поскольку речь идёт о перспективном компьютере, которые будет актуален целых 5 лет.'
                                      ' SSD Kingston SNV2S не понравится тем, кто привык смотреть на комплектующие через призму синтетических тестов.'
                                      ' По своим скоростным показателям этот твердотельный накопитель уступает многим более дорогим моделям в 3-4 раза,'
                                      ' но всё это становится неважно, когда дело доходит до обычных игр. Здесь 2100 МБ/с чтения и'
                                      ' 1700 МБ/с на запись отлично справляются с поставленными задачами и в большинстве случаев оказываются даже излишними.'
                                      ' При желании можно купить SSD на 10 тысяч дороже, но мы не видим в этом никакого смысла,'
                                      ' поскольку реальной пользы от такого накопителя вы не увидите. Куда логичнее потратить эти деньги на жёсткий диск.'
                                      ' HGST – это представитель легендарной серии Hitachi. После поглощения со стороны Western Digital'
                                      ' производственные линии остались без изменений, что позволяет говорить о высоком качестве продукции.'
                                      ' Ёмкости в 10 Тб будет достаточно для записи сюда домашнего видео и популярных сериалов,'
                                      ' тогда как Kingston SNV2S лучше подходит для игр и программного обеспечения. Если подходить к вопросу без фанатизма,'
                                      ' то единственный разумный выбор, который прослужит нам 5 лет и не опустошит кошелёк – это Radeon RX 7900 XT.'
                                      ' Видеокарта предложит 20 Гб скоростной памяти и сможет запускать любые игры даже в 4К.'
                                      ' Со временем придётся переходить в 2К, ну а наш перспективный компьютер прослужит максимально долго.'
                                      ' К сожалению, у NVIDIA аналогичные по скорости решения стоят больше 120 тысяч рублей,'
                                      ' поэтому мы не видим смысла переплачивать за бренд. Согласно тестам,'
                                      ' Radeon RX 7900 XT отлично справляется с трассировкой лучей, ну а активное распространение технологии FSR 3'
                                      ' позволяет надеяться на действительно длительный жизненный цикл. Пытаться экономить на блоке питания в сложившейся ситуации'
                                      ' было бы неразумно, но это не значит, что мы будем бросаться на первое попавшееся решение за 20 тысяч рублей.'
                                      ' Отнюдь, ведь в продаже есть Deepcool PM800D, мощности которого хватит для обеспечения стабильной работы всех компонентов.'
                                      ' Блок питания обладает высокой энергоэффективностью и поддерживает стандарт 80 PLUS Gold.'
                                      ' Даже с нашей видеокартой он не будет работать на максимуме возможностей, а это хорошая информация,'
                                      ' ведь это гарантирует стабильность и тишину. Все выбранные нами комплектующие'
                                      ' можно поместить в корпус Msi MAG FORGE M100R. Это на самый впечатляющий системный блок,'
                                      ' который нам доводилось видеть. Если вам нравится что-то необычное, то приготовьтесь заплатить не менее 30 тысяч рублей.'
                                      ' Мы не видим в этом никакого смысла, ведь главная задача заключалась в том,'
                                      ' чтобы получить быстрый и максимально недорогой компьютер, который будет тянуть все игры в 2К даже спустя 5 лет.'
                                      ' Внутри корпуса вы найдёте 4 кулера, которые охладят нрав видеокарты Radeon RX 7900 XT, выводя горячий воздух наружу.'
                                      ' После учёта всех комплектующих выяснилось, что мы потратили на сборку 210 тысяч рублей.'
                                      ' Это примерно 2400 долларов, а значит сумма действительно серьёзная. Как уже было сказано выше,'
                                      ' 10 лет назад за перспективную сборку вы бы заплатили 1500 долларов,'
                                      ' но сегодня аппетиты производителей комплектующих значительно выросли. Если вам действительно был нужен ПК на 5 лет,'
                                      ' то ничего лучше за эту сумму вы не найдёте. Ну или можно подождать до конца года.'
                                      ' В теории, ведь на практике новинки могут оказаться намного дороже, что вынудит вас не только сидеть в ожидании,'
                                      ' но потратить ещё больше денег. ',
                            author=aut)

post4 = Post.objects.create(post_type=True,
                            title='Релиз Little Nightmares 3 перенесли на 2025 год',
                            post_text='Студия Supermassive Games перенесла релиз Little Nightmares 3.'
                                      ' Теперь выход платформера намечен на 2025 год — изначально игру планировали выпустить в 2024-м.'
                                      'Представители Supermassive Games добавили, что им потребуется больше времени,'
                                      ' чтобы добиться наилучшего качества игры. Разработчики также пообещали поделиться деталями проекта'
                                      ' летом 2024-го, возможно, во время презентаций, запланированных на июнь.',
                            author=aut_3)

c1 = Category.objects.all()[4]
c2 = Category.objects.all()[5]
c3 = Category.objects.all()[1]

post1.categories.add(c1)
post2.categories.add(c2)
post3.categories.add(c2)
post3.categories.add(c3)
post4.categories.add(c2)

comm1 = Comment.objects.create(comment_text='Отличная новость, уже давно жду, не терпится увидеть, что там'
                                            'сделали разработчики:)',
                               post_id=post1,
                               user_id=bob_tail)
comm2 = Comment.objects.create(comment_text='Обожаю эту игру, жду когда уже портируют на ПК.',
                               post_id=post2,
                               user_id=bob_tail)
comm3 = Comment.objects.create(comment_text='Класс, как раз собрался собирать новый комп себе...',
                               post_id=post3,
                               user_id=bob_tail)
comm4 = Comment.objects.create(comment_text='А я играю на консолях, комп чисто для работы у меня:)',
                               post_id=post3,
                               user_id=wild_fox)
comm5 = Comment.objects.create(comment_text='Ну что ж господа, ждем-с...',
                               post_id=post4,
                               user_id=wild_fox)
comm1.like()
comm2.like()
comm3.like()
comm4.dislike()
comm3.like()
comm2.like()
comm3.like()
comm5.like()

post1.like()
post1.like()
post2.like()
post2.like()
post2.like()
post2.like()
post3.like()
post3.like()
post3.like()
post3.dislike()
post4.like()

# Post.objects.filter(author_id=aut).values('post_rating')
# aut = Author.objects.get(pk=2)
# aut_3.update_rating()
# aut_3 = Author.objects.get(pk=5)
# Comment.objects.filter(user_id=aut2.user_id).values('comment_rating')
# wild_fox = User.objects.get(pk=7)
# aut.update_rating()
# aut_1.update_rating()
# aut_2.update_rating()
# aut = Author.objects.get(pk=2)
# aut_1 = Author.objects.get(pk=3)
# aut_2 = Author.objects.get(pk=4)

best_user = Author.objects.order_by('-user_rating').values('user_rating', 'user__username').first()
best_user

best_post = Post.objects.order_by('-post_rating').values('post_time_in', 'author__user__username', 'post_rating', 'title', 'post_text'[:124]).first()
best_post

best_post1 = Post.objects.order_by('-post_rating').first()
best_post_comm = Comment.objects.filter(post_id=best_post1).values('comm_time_in', 'user_id__username', 'comment_rating', 'comment_text')
best_post_comm
# Author.objects.get(pk=2).user.username
# Author.objects.aggregate(Max('user_rating'))