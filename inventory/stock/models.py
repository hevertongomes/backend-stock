from django.db import models
from inventory.core.models import Base
from inventory.items.models import Item
from django.utils.translation import ugettext_lazy as _


MOVEMENT = [
    ("e", "Entrada")
    ("s", "Saída")
]

class Stock(Base):
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movement = models.CharField(max_length=1, choices=MOVEMENT)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.pk)


class StockItens(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qtd = models.PositiveIntegerField()
    balance = models.PositiveIntegerField()

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.stock.pk, self.item)
