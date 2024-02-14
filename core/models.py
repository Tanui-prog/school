from django.db import models


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    subject_id = models.CharField(max_length=10, unique=True)
    subject_class = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.subject_id}: {self.subject_name}"
class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    grade = models.IntegerField(max_length=10)
    stream = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.grade} {self.stream}"
