# Generated by Django 5.0.2 on 2024-02-14 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='grade',
            field=models.IntegerField(),
        ),
    ]