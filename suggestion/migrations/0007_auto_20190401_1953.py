# Generated by Django 2.1.7 on 2019-04-01 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
        ('suggestion', '0006_auto_20190401_1939'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MemberResponse',
            new_name='MemberSuggestionResponse',
        ),
    ]
