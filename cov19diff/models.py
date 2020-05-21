from django.db import models
from datetime import datetime

# Create your models here.
class DailyCsv(models.Model):
    day = models.CharField(max_length=10,primary_key=True)
    data = models.CharField(max_length=1000000)

    def dayDate(self):
        return datetime.strptime(self.day,'%m-%d-%Y')
