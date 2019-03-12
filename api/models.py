from django.db import models
from . import core


# Create your models here.


class Company(models.Model):
    function_name=models.CharField(max_length=200)
    qid=models.IntegerField()

    def scrape(self, tracking_id):
        result=getattr(core, self.function_name)(tracking_id)
        return result

    def __str__(self):
        return self.function_name








