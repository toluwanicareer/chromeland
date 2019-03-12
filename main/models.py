from django.db import models
from django.urls import reverse
# Create your models here.


class Converter(models.Model):
    title=models.CharField(max_length=200)
    image_file=models.CharField(max_length=200, null=True)
    slug=models.CharField(null=True, max_length=200)
    tag_line=models.TextField(null=True)
    convert_from=models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('converter-detail', args=[str(self.slug)])


class subtotpic(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    converter=models.ForeignKey(Converter, on_delete=models.CASCADE)

    def __str__(self):
        return self.converter.title

