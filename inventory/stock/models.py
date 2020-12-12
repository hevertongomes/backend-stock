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
        return str(self.nf)


class StockItem(Base):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stocks')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qtd = models.DecimalField(_("Quantidade"), max_digits=16,
        decimal_places=2, default=Decimal('1'))
    balance = models.DecimalField(_("Quantidade Final"), max_digits=16,
        decimal_places=2, default=Decimal('1'), blank=True, null=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return 'Stock: {} - com quantidade: {}'.format(self.pk, self.qtd)
