from django.db import models
from account.models import User

# Create your models here.


class Equipment(models.Model):
    name = models.CharField(max_length=128, unique=True)
    key = models.CharField(max_length=16, unique=True)
    descript = models.CharField(max_length=256, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"


class Data(models.Model):
    value = models.FloatField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    descript = models.CharField(max_length=256, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.value)

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "Data"
        verbose_name_plural = "Datas"
