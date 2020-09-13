from django.test import TestCase
from model_mommy import mommy
from django.utils.timezone import datetime
from inventory.items.models import Item


class TestItem(TestCase):

    def setUp(self):
        self.item = mommy.make(Item, name='Zinco XX')

    def test_item_creation(self):
        self.assertTrue(isinstance(self.item, Item))
        self.assertEquals(self.item.__str__(), self.item.name)
