# Generated by Django 3.1.3 on 2020-12-09 20:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0004_spideridentifyrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='spideridentifyrequest',
            name='ticket',
            field=models.CharField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
    ]