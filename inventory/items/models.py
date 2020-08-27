from django.db import models
from inventory.core.models import Base
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _


UNIT_CHOICES = [
    ("0", "UND"),
    ("1", "G"),
    ("2", "MG"),
    ("3", "L"),
    ("4", "ML"),
    ("5", "KL")
]


class Item(Base):

    name = models.CharField(_("Nome do Item"), max_length=100)
    unit = models.CharField(_("Unidade"), max_length=1, choices=UNIT_CHOICES)
    brand = models.CharField(_("Marca"), max_length=100)
    current_inventory = models.DecimalField(_("Estoque atual"), max_digits=16,
        decimal_places=2, default=Decimal('1'))
    minimum_stock = models.DecimalField(_("Estoque minímo"),  max_digits=16,
        decimal_places=2, default=Decimal('1'))
    validaty = models.DateField(_("Data de Validade"), auto_now=False, auto_now_add=False)

    class meta:
        db_table = 'tb_item'
    
    def __str__(self):
        return self.name
    
