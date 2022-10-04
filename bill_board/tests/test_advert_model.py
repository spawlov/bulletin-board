from django.contrib.auth.models import User
from django.test import TestCase

from bill_board.models import Advert


class AdvertListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create_user('TestUser', 'test@email.com', '123qwerty456')
        Advert.objects.create(
            author=author,
            title='Test title',
            text='Test text for test',
            category='tanks'
        )

    def test_author_label(self):
        advert = Advert.objects.get(pk=1)
        field_label = advert._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_title_label(self):
        advert = Advert.objects.get(pk=1)
        field_label = advert._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Название объявления')

    def test_title_max_length(self):
        advert = Advert.objects.get(id=1)
        max_length = advert._meta.get_field('title').max_length
        self.assertEquals(max_length, 128)

    def test_title_value(self):
        advert = Advert.objects.get(id=1)
        value = advert.title
        self.assertEquals(value, 'Test title')

    def test_text_label(self):
        advert = Advert.objects.get(pk=1)
        field_label = advert._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Текст объявления')

    def test_text_value(self):
        advert = Advert.objects.get(id=1)
        value = advert.text
        self.assertEquals(value, 'Test text for test')

    def test_category_label(self):
        advert = Advert.objects.get(pk=1)
        field_label = advert._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'Категория')

    def test_category_max_length(self):
        author = Advert.objects.get(id=1)
        max_length = author._meta.get_field('category').max_length
        self.assertEquals(max_length, 12)

    def test_category_value(self):
        advert = Advert.objects.get(id=1)
        value = advert.get_category_display()
        self.assertEquals(value, 'Танки')

    def test_create_label(self):
        advert = Advert.objects.get(pk=1)
        field_label = advert._meta.get_field('create').verbose_name
        self.assertEquals(field_label, 'Дата создания')

    def test_attach_label(self):
        advert = Advert.objects.get(pk=1)
        field_label = advert._meta.get_field('attach').verbose_name
        self.assertEquals(field_label, 'Вложение')

    def test_get_absolute_url(self):
        author = Advert.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/1/')

