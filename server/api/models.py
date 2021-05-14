from django.db import models
from django.contrib.auth.models import User


class Object(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='user_objects', on_delete=models.CASCADE)


class Access(models.Model):
    user = models.ForeignKey(User, related_name='user_accesses', on_delete=models.CASCADE)
    object = models.ForeignKey(Object, related_name='object_accesses', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owner_accesses', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'object', 'owner'),)


class AccessOffer(models.Model):
    user = models.ForeignKey(User, related_name='user_access_offers', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owner_access_offers', on_delete=models.CASCADE)
    object = models.ForeignKey(Object, related_name='object_access_offers', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'owner', 'object'),)


class QRCode(models.Model):
    object = models.ForeignKey(Object, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=20)
    status = models.BooleanField()
