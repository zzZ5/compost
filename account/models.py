from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "User"
        verbose_name_plural = "Users"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
