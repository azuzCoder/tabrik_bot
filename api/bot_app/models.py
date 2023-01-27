from django.db import models


class BotUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    joined = models.BooleanField(default=True)


class JoinedGroup(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    joined = models.BooleanField(default=True)


class Birthday(models.Model):
    name = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    congrat = models.TextField()
    date = models.DateField()
    user = models.ForeignKey(BotUser, related_name='birthdays', on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(JoinedGroup, blank=True)
