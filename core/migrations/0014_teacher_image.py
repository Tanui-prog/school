# Generated by Django 5.0.2 on 2024-02-26 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_students_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='teacher_photos'),
        ),
    ]
