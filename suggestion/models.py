from django.db import models

# Create your models here.


class Suggestion(models.Model):
    member_offer = models.ForeignKey(
        "offer.MemberOffer", null=True, blank=True, on_delete=models.SET_NULL, related_name="suggestions")
    datetime_from = models.DateTimeField(null=True, blank=True, verbose_name="Zeitpunkt von")
    datetime_to = models.DateTimeField(null=True, blank=True, verbose_name="Zeitpunkt bis")
