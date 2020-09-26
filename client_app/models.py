from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.models import *
# Create your models here.


class TableProducts(models.Model):
    STATUS_PROCCES = 1
    STATUS_DONE = 2
    STATUS_CHOICES = (
        (STATUS_PROCCES, _('Жасалуда')),
        (STATUS_DONE, _('Дайын')),
    )

    STATUS_SHOW = 1
    STATUS_NONE = 2
    STATUS_DISPLAY = (
        (STATUS_SHOW, _('display')),
        (STATUS_NONE, _('none')),
    )

    STATUS_NO = 1
    STATUS_YES = 2
    STATUS_RECD = (
        (STATUS_NO, _('кабылданбады')),
        (STATUS_YES, _('кабылданды')),
    )
    table = models.IntegerField(blank=True)    # Table id
    code_order = models.CharField(max_length=150, null=True)
    product = models.ForeignKey(Product, blank=True, on_delete=models.SET_NULL, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, blank=True, default=1)
    unit = models.SmallIntegerField(blank=True)
    display = models.SmallIntegerField(choices=STATUS_DISPLAY, blank=True, default=1)
    data = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(UserProfile, blank=True, on_delete=models.CASCADE)
    recd = models.SmallIntegerField(choices=STATUS_RECD, blank=True, default=1)

    def __str__(self):
        return str(self.table)
        