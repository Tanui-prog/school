# Generated by Django 5.0.2 on 2024-03-05 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_rename_classes_students_subject_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='students',
            old_name='subject_class',
            new_name='student_class',
        ),
    ]
