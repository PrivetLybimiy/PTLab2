from django.test import TestCase, Client
from shop.models import Product, Purchase
from datetime import date

class IndexViewTests(TestCase):
    """Тесты для функции представления index"""

    def setUp(self):
        Product.objects.create(name="Что то", price=500)
        self.client = Client()

    def test_index_page_status_code(self):
        """Проверка доступности главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_page_context_contains_products(self):
        """Проверка, что в контексте есть список продуктов"""
        response = self.client.get('/')
        self.assertIn('products', response.context)
        self.assertTrue(len(response.context['products']) > 0)


class PurchaseCreateViewTests(TestCase):
    """Тесты для класса PurchaseCreate CreateView"""

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Книга", price=740)
        self.url = f'/buy/{self.product.id}/'

    def test_get_purchase_form(self):
        """GET-запрос должен отдавать статус 200 и передавать корректный контекст"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product)
        self.assertIn('price', response.context)
        self.assertEqual(response.context['price'], self.product.price)

    def test_post_creates_purchase_with_discount(self):
        """POST с датой рождения сегодня должен получить скидку"""
        response = self.client.post(self.url, data={
            'person': 'Ivanov',
            'birthday': date.today().isoformat(),
            'address': 'Moscow',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Применена скидка')
        self.assertContains(response, 'Итоговая цена')

        purchase = Purchase.objects.latest('id')
        self.assertEqual(purchase.person, 'Ivanov')
        self.assertEqual(purchase.product, self.product)

    def test_post_creates_purchase_without_discount(self):
        """POST с датой рождения не сегодня не получает скидку("""
        birthday = date(1990, 1, 1)
        response = self.client.post(self.url, data={
            'person': 'Petrov',
            'birthday': birthday.isoformat(),
            'address': 'Tver',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Применена скидка')
        self.assertContains(response, 'Итоговая цена')

        purchase = Purchase.objects.latest('id')
        self.assertEqual(purchase.birthday, birthday)

    def test_post_missing_required_fields(self):
        """POST без обязательных полей должен возвращать ошибку формы"""
        response = self.client.post(self.url, data={
            'person': '',
            'birthday': '',
            'address': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'person', 'This field is required.')
        self.assertFormError(response, 'form', 'birthday', 'This field is required.')
        self.assertFormError(response, 'form', 'address', 'This field is required.')
