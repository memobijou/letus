# Generated by Django 2.1.7 on 2019-04-02 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suggestion', '0008_suggestion_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='member_offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_suggestions', to='offer.MemberOffer'),
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_suggestions', to='offer.Offer', verbose_name='Angebot'),
        ),
    ]
