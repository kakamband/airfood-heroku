from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.





class Restoran(models.Model):
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='image/restoran/' ,default='image/restoran/default.png', null=True)
    tables = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    STATUS_ADMIN = 0
    STATUS_WORKER = 1
    STATUS_USER = 2
    STATUS_ADMINISTRATION = 3

    STATUS_CHOICES = (
        (STATUS_ADMIN, _('admin')),
        (STATUS_WORKER, _('worker')),
        (STATUS_USER, _('user')),
        (STATUS_ADMINISTRATION, _('administration'))
    )

    WAGE_HOUR = 0
    WAGE_DAY = 1
    WAGE_MONTH = 2

    WAGE_CHOICES = (
        (WAGE_HOUR, _('hour')),
        (WAGE_DAY, _('day')),
        (WAGE_MONTH, _('month')),
    )

    DUTY_1 = 0
    DUTY_2 = 1
    DUTY_3 = 2
    DUTY_4 = 3
    DUTY_5 = 4

    DUTY_CHOICES = (
        (DUTY_1, _('security')),
        (DUTY_2, _('Chef')),
        (DUTY_3, _('cashier')),
        (DUTY_4, _('manager')),
        (DUTY_5, _('waitress')),
    )  

    mobile = models.IntegerField(_('phone number'), null=True)
    avatar = models.ImageField(upload_to='image/avatar/worker' ,default='image/avatar/worker/default.png', null=True)
    status = models.SmallIntegerField(_("Status"),choices=STATUS_CHOICES, null=True)
    wage = models.IntegerField(_("Wage"), null=True)
    wage_type = models.SmallIntegerField(_("Wage type"), choices=WAGE_CHOICES, null=True)
    duty = models.SmallIntegerField(_("Duty"), choices=DUTY_CHOICES, null=True)
    restoran = models.ForeignKey(Restoran, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='image/restoran/' ,default='image/restoran/default.png', null=True)
    restoran = models.ForeignKey(Restoran, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_PORTION = 1
    STATUS_PIECES = 2
    STATUS_LITER = 3
    STATUS_CUP =4

    STATUS_CHOICES = (
        (STATUS_PORTION, _('порция')),
        (STATUS_PIECES, _('штук')),
        (STATUS_LITER, _('литр')),
        (STATUS_CUP, _('стакан')),
    )

    name = models.CharField(max_length=150, blank=True)
    body = models.TextField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES, blank=True)
    unit = models.SmallIntegerField(blank=True)
    price = models.IntegerField(blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/restoran/' ,default='image/restoran/default.png', null=True)

    def __str__(self):
        return self.name


class ImageProduct(models.Model):
    image = models.ImageField(upload_to='image/restoran/' ,default='image/restoran/default.png', null=True)
    product_image = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.url


class Table(models.Model):
    STATUS_CHOICES = (
        ('empty', _('empty')),  # ешқандай тапсырыс болмаса
        ('scanned', _('scanned')),  # 
        ('ordered', _('ordered')), # клиент тапсырыс берген кезде
        ('reordered', _('reordered')), # клиент бір тапсырыс бергеннен кейін тағы да тапсырыс берген кезде
        ('order_accepted', _('order_accepted')),  # админ клиенттің тапсырысын қабыл алған кезде
        ('order_cancelled', _('order_cancelled')), # админ клиенттің тапсырысын қайтарған кезде
        ('reorder_accepted', _('reorder_accepted')),  # админ клиенттің жаңа тапсырысын қабыл алған кезде
        ('reorder_cancelled', _('reorder_cancelled')),  # админ клиенттің жаңа тапсырысын қайтарған кезде
        ('bill_requested', _('bill_requested')),  # клиент счетты жабу үшін счек сұратқанда
        ('bill_closed', _('bill_closed')), # админ счетты жабқан кезде
    )

    number = models.SmallIntegerField(blank=True)
    restoran = models.ForeignKey(Restoran, blank=True, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, choices=STATUS_CHOICES, blank=True, default='empty')
    user = models.SmallIntegerField(null=True)
    waiter = models.SmallIntegerField(null=True)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.number)


class WorkTimes(models.Model):
    WEEK_1 = 1
    WEEK_2 = 2
    WEEK_3 = 3
    WEEK_4 = 4
    WEEK_5 = 5
    WEEK_6 = 6 
    WEEK_7 = 7

    WEEK_CHOICES = (
        (WEEK_1, _('Monday')),
        (WEEK_2, _('Tuesday')),
        (WEEK_3, _('Wednesday')),
        (WEEK_4, _('Thursday')),
        (WEEK_5, _('Friday')),
        (WEEK_6, _('Saturday')),
        (WEEK_7, _('Sunday')),   
    )

    worker = models.ForeignKey(UserProfile, blank=True, on_delete=models.CASCADE)
    week = models.SmallIntegerField(choices=WEEK_CHOICES, blank=True)
    status = models.SmallIntegerField(blank=True, default=0)
    hour_begin = models.TimeField(null=True)
    hour_end = models.TimeField(null=True)

    def save_days(self, b, e):
        self.status = 1
        self.hour_begin = b
        self.hour_end = e
        self.save()