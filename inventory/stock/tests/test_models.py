from django.test import TestCase
from model_mommy import mommy
from django.utils.timezone import datetime
from inventory.items.models import Item
from inventory.stock.models import Stock, StockItem


class TestStock(TestCase):

    def setUp(self):
        self.stock = mommy.make(Stock, nf=101010)
    
    def test_stock_criation(self):
        self.assertTrue(isinstance(self.stock, Stock))
        self.assertEquals(self.stock.__str__(), str(self.stock.nf))


class TestStockItem(TestCase):

    def setUp(self):
        self.stock = mommy.make(Stock, nf='101010')
        self.item = mommy.make(Item, name='Ninho Leite')
        self.stock_item = mommy.make(StockItem, qtd=3)

    def test_stock_item_creation(self):
        self.assertTrue(isinstance(self.stock_item, StockItem))
        self.assertEquals(self.stock_item.__str__(), 'Stock: {} - com quantidade: {}'.format(self.stock_item.pk, self.stock_item.qtd))
            
