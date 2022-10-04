from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from bill_board.models import Advert


class AdvertListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author = User.objects.create_user('TestUser', 'test@email.com', '123qwerty456')
        number_of_advert = 15
        for author_num in range(number_of_advert):
            Advert.objects.create(
                author=author,
                title=f'Test title #{author_num}',
                text=f'Test text for advert #{author_num}',
                category='spellcasters'
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('bill_board:advert'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('bill_board:advert'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'advertising.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('bill_board:advert'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['advert']) == 10)