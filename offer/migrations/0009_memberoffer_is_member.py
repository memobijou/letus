# Generated by Django 2.1.7 on 2019-03-28 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0008_auto_20190327_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberoffer',
            name='is_member',
            field=models.NullBooleanField(verbose_name='Mitglied'),
        ),
    ]