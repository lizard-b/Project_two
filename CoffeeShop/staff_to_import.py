cashier1 = Staff.objects.create(full_name="Смоляная Юлия Андреевна",
                                duty=Staff.cashier,
                                labor_contract=1754)
cashier2 = Staff.objects.create(full_name="Лукьяненко Василий Иванович",
                                duty=Staff.cashier,
                                labor_contract=4355)
direct = Staff.objects.create(full_name="Дубовицкий Андрей Юрьевич",
                                duty=Staff.director,
                                labor_contract=1254)
