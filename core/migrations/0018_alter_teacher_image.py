# Generated by Django 5.0.2 on 2024-03-01 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_teacher_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='teacher_images'),
        ),
    ]
