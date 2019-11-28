from django.db import models

# Create your models here.
class Meeting(models.Model):
    guestname = models.CharField(max_length=30)
    guestemail = models.CharField(max_length=30)
    guestmobileNo = models.CharField(max_length=15)

    hostname = models.CharField(max_length=30)
    hostemail = models.CharField(max_length=30)
    hostmobileNo = models.CharField(max_length=15)

    checkInTime = models.CharField(max_length=20)
    checkOutTime = models.CharField(max_length=20)
    isCheckOut = models.BooleanField()
