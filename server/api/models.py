from django.db import models


class Object(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='objects', on_delete=models.CASCADE)


class QRCode(models.Model):
    object = models.ForeignKey(Object, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=20)
    status = models.BooleanField()
