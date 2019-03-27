from django.db import models

# Create your models here.


class Offer(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    organizer = models.ForeignKey("member.Member", null=True, blank=True, on_delete=models.SET_NULL)
