from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from accounts.models import default_account, Accounts
from bkash.models import BkashTransaction

DAYS = [
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
]


class TimeTable(models.Model):
    time_table_name = models.CharField(max_length=10, default='Day Time', unique=True)
    in_time = models.TimeField(default='09:00')
    out_time = models.TimeField(default='17:00')
    weekend = models.CharField(choices=DAYS, default=DAYS[0], max_length=20)

    def __str__(self):
        return str(self.time_table_name)


class Employee(models.Model):
    employee_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50, default='Worker')
    fathers_name = models.CharField(max_length=50, null=True, blank=True)
    mothers_name = models.CharField(max_length=50, null=True, blank=True)
    spouse_name = models.CharField(max_length=50, null=True, blank=True)
    NID = models.CharField(max_length=25, null=True, blank=True, unique=True)
    phone_no = models.CharField(max_length=11, null=True, blank=True)
    hourly_rate = models.FloatField()
    time_table = models.ForeignKey(TimeTable, null=True, on_delete=models.Empty, blank=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    joining_date = models.DateField(default=now)
    photo = models.ImageField(upload_to='employee_photo', default='default.jpg')

    def __str__(self):
        return str(self.employee_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    @staticmethod
    def get_absolute_url():
        return reverse('person-list')


class Day(models.Model):
    date = models.DateField(default=now, unique=True)

    def __str__(self):
        return str(self.date)


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.ForeignKey(Day, on_delete=models.CASCADE)
    in_time = models.TimeField(default=now)
    out_time = models.TimeField(default=now)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'date',)

    def __str__(self):
        return '%s %s ' % (self.employee, self.date)


MONTHS = [
    ('JAN', 'Friday'),
    ('FEB', 'Saturday'),
    ('MAR', 'Sunday'),
    ('APR', 'Monday'),
    ('MAY', 'Tuesday'),
    ('JUN', 'Wednesday'),
    ('JUL', 'Thursday'),
    ('AUG', 'Thursday'),
    ('SEP', 'Thursday'),
    ('OCT', 'Thursday'),
    ('NOV', 'Thursday'),
]

PAYMENT_MODE_CHOICES = [
    ('CQ', 'Cheque'),
    ('CA', 'Cash'),
    ('ONL', 'Online'),
    ('PO', 'Pay Order'),
    ('BK', 'Bkash')
]


class SalaryPayment(models.Model):
    Employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    month = models.CharField(choices=MONTHS, max_length=20)
    amount = models.FloatField()
    date = models.DateField(auto_now=True)
    date_time = models.DateTimeField(auto_now=True)
    payed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, default=PAYMENT_MODE_CHOICES[1], max_length=10)
    cheque_PO_ONL_no = models.IntegerField(null=True, blank=True)
    cheque_date = models.DateField(default=now, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    payment_from_account = models.ForeignKey(Accounts, default=default_account, null=True, on_delete=models.CASCADE)
    transaction = models.ForeignKey(BkashTransaction, on_delete=models.CASCADE, null=True)
    remarks = models.CharField(max_length=200)
