from django.contrib.auth.models import User
from django.test import TestCase

from bill_board.models import Advert, Resp


class AdvertListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author_for_advert = User.objects.create_user(
            'TestUser', 'test@email.com', '123qwerty456'
        )
        author_for_resp = User.objects.create_user(
            'TestUserResp', 'test_resp@email.com', '123qwerty456'
        )
        advert = Advert.objects.create(
            author=author_for_advert,
            title='Test title',
            text='Test text for test',
            category='tanks'
        )
        Resp.objects.create(
            author=author_for_resp,
            post=advert,
            text='Test text for resp',
        )

    def test_author_label(self):
        resp = Resp.objects.get(pk=1)
        field_label = resp._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_post_label(self):
        resp = Resp.objects.get(pk=1)
        field_label = resp._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'Объявление')

    def test_text_label(self):
        resp = Resp.objects.get(pk=1)
        field_label = resp._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Текст отклика')

    def test_text_value(self):
        resp = Resp.objects.get(pk=1)
        field_value = resp.text
        self.assertEquals(field_value, 'Test text for resp')

    def test_status_label(self):
        resp = Resp.objects.get(pk=1)
        field_label = resp._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'Принято')

    def test_status_value(self):
        resp = Resp.objects.get(pk=1)
        field_value = resp.status
        self.assertFalse(field_value)

    def test_get_absolute_url(self):
        resp = Resp.objects.get(id=1)
        self.assertEquals(resp.get_absolute_url(), '/1/')

