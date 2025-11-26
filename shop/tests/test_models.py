from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime, date

class ProductModelTests(TestCase):
    """Тесты для модели Product"""
    def setUp(self):
        """Создание нескольких товаров для тестов"""
        Product.objects.create(name="Книга", price=740)
        Product.objects.create(name="Карандаш", price=50)

    def test_fields_types(self):
        """Проверка типов полей name и price для созданных товаров"""
        for product in Product.objects.all():
            self.assertIsInstance(product.name, str)
            self.assertIsInstance(product.price, int)

    def test_price_values(self):
        """Проверка корректности значений цены у товаров"""
        book = Product.objects.get(name="Книга")
        pencil = Product.objects.get(name="Карандаш")
        self.assertEqual(book.price, 740)
        self.assertEqual(pencil.price, 50)


class PurchaseModelTests(TestCase):
    """Тесты для модели Purchase"""

    def setUp(self):
        """Создание продукта и покупки с сегодняшним днем рождения"""
        self.product = Product.objects.create(name="Книга", price=740)
        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)
        Purchase.objects.create(
            product=self.product,
            person="Ivanov",
            address="Svetlaya St.",
            birthday=self.today
        )

    def test_purchase_field_types(self):
        """Проверка типов полей person, address и date"""
        purchase = Purchase.objects.get(product=self.product)
        self.assertIsInstance(purchase.person, str)
        self.assertIsInstance(purchase.address, str)
        self.assertIsInstance(purchase.date, datetime)

    def test_date_auto_set(self):
        """Проверка автоматического выставления даты создания покупки"""
        purchase = Purchase.objects.get(product=self.product)
        self.assertIsNotNone(purchase.date)

    def test_purchase_creation_without_birthday_fails(self):
        """Проверка, что покупка без обязательного поля birthday невозможна"""
        with self.assertRaises(Exception):
            Purchase.objects.create(
                product=self.product,
                person="Ivanov",
                address="Svetlaya St."
                # дня рождения нету тут
            )
