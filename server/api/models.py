from django.db import models


class Object(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class QRCode(models.Model):
    object = models.ForeignKey(Object, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=20)
    status = models.BooleanField()
