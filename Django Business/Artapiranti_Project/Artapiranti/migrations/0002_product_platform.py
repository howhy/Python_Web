# Generated by Django 2.0 on 2018-01-08 02:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Artapiranti', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='platform',
            field=models.CharField(default=django.utils.timezone.now, max_length=256),
            preserve_default=False,
        ),
    ]
