from django.db import models

# Create your models here.


class Offer(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    organizer = models.ForeignKey("member.Member", null=True, blank=True, on_delete=models.SET_NULL)
    is_finished = models.NullBooleanField(blank=True, verbose_name="Abgeschloßen")
    is_canceled = models.NullBooleanField(blank=True, verbose_name="Abgebrochen")
    members = models.ManyToManyField("member.Member", through="offer.MemberOffer", related_name="offers")


class MemberOffer(models.Model):
    offer = models.ForeignKey("offer.Offer", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Angebot",
                              related_name="offer_members")
    member = models.ForeignKey(
        "member.Member", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Mitglied",
        related_name="member_offers")
    is_admin = models.NullBooleanField(blank=True, verbose_name="Administrator")
    is_member = models.NullBooleanField(blank=True, verbose_name="Mitglied")
