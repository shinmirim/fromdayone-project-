from django.db import models

# Create your models here.
class Fashion(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    rgb = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)
    shape = models.CharField(max_length=255)
    season = models.CharField(max_length=255)
    average = models.CharField(max_length=255)
    style = models.CharField(max_length=255)
    total = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "fashion"

    def __str__(self):
        return self.name
