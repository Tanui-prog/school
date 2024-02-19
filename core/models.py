from django.db import models


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    grade = models.IntegerField()
    stream = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.grade} {self.stream}"

class Subject(models.Model):
    
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    subject_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject_id}: {self.subject_name} - {self.subject_class}"
