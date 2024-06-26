from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    clientType = models.CharField(max_length=200, null=False, default="Ordinary")

    def __str__(self):
        return f'Client {self.user}'

class Doctor(models.Model):
    clientType = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=200, null=True)

    def __repr__(self):
        return f'Doctor {self.clientType}'

class PatientSpecial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start = models.DateField()

    def __repr__(self):
        return f'PatientSpecial {self.user}'



class MaternCalendar(models.Model):
    week = models.TextField()
    body = models.TextField()
    babydev = models.TextField()
    symptoms = models.TextField()
    tips = models.TextField()

    def __str__(self):
        return f'MaternCalendar {self.week}'


class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    payment_date = models.DateField()
    expiry_date = models.DateField()
    amount = models.IntegerField(default=20)

    def __str__(self):
        return f'Subscriptions {self.user}'

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(default=False)
    age = models.CharField(max_length=200, null=True)
    systolicBP = models.CharField(max_length=200, null=True)
    diastolicBP = models.CharField(max_length=200, null=True)
    bs = models.CharField(max_length=200, null=True)
    bodytemp = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'Report {self.user}'

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    message = models.CharField(max_length=1000, null=True)
    date = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment {self.user}'
    

class Settings(models.Model):

    ngroklink = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'Settings {self.ngroklink}'



    


