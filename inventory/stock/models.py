from django.db import models
from inventory.core.models import Base
from inventory.items.models import Item
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _


MOVEMENT_CHOICES = [
    ("0", "Entrada"),
    ("1", "Saída")
]

class Stock(Base):
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movement = models.CharField(max_length=1, choices=MOVEMENT_CHOICES)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.pk)


class StockItems(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qtd = models.DecimalField(_("Estoque atual"), max_digits=16,
        decimal_places=2, default=Decimal('1'))
    balance = models.DecimalField(_("Estoque atual"), max_digits=16,
        decimal_places=2, default=Decimal('1'))

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.stock.pk, self.item)
