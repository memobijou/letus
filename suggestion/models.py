from django.db import models

# Create your models here.


class Suggestion(models.Model):
    member_offer = models.ForeignKey(
        "offer.MemberOffer", null=True, blank=False, on_delete=models.SET_NULL, related_name="suggestions")
    datetime_from = models.DateTimeField(null=True, blank=False, verbose_name="Zeitpunkt von")
    datetime_to = models.DateTimeField(null=True, blank=False, verbose_name="Zeitpunkt bis")


class MemberSuggestionResponse(models.Model):
    member = models.ForeignKey(
        "member.Member", null=True, blank=False, on_delete=models.SET_NULL, related_name="responses")
    suggestion = models.ForeignKey(
        "suggestion.Suggestion", null=True, blank=True, verbose_name="Terminvorschlag", on_delete=models.SET_NULL,
        related_name="responses"
    )
    accepted = models.NullBooleanField(blank=True, verbose_name="Zustimmung")
