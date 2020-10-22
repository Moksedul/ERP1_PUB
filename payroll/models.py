from PIL import Image
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


WEEKENDS = [
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
    weekend = models.CharField(choices=WEEKENDS, default=WEEKENDS[0], max_length=20)

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


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.ForeignKey(Day, on_delete=models.CASCADE)
    in_time = models.TimeField(default=now)
    out_time = models.TimeField(default=now)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'date',)