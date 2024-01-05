from django.db import models



class Classes(models.Model):
    class_id = models.AutoField(primary_key=True)
    grade = models.IntegerField()
    stream = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.grade} {self.stream}"

class Subject(models.Model):
    
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    subject_class = models.ForeignKey(Classes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject_id}: {self.subject_name} - {self.subject_class}"


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    identity_number = models.CharField(max_length=20)
    teacher_name = models.CharField(max_length=100)
    teacher_gender = models.CharField(max_length=10)
    teacher_email = models.EmailField()
    teacher_phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='teacher_images', default='default.jpg')
    age = models.IntegerField()
    joinin_date = models.CharField(max_length=20) 
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    tsc_no = models.CharField(max_length=20)
    subject_combination = models.CharField(max_length=255)

   
    def __str__(self):
        return self.teacher_name
    
class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=10)
    joining_date = models.DateField()
    admission_no = models.CharField(max_length=20, unique=True)
    blood_group = models.CharField(max_length=5)
    religion = models.CharField(max_length=50)
    age = models.IntegerField()
    student_class = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True, default=None)
    session = models.CharField(max_length=50)
    image = models.ImageField(upload_to='student_photos/', default='default.jpg')
    parent_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=15)
    parent_address = models.TextField()
    parent_relationship = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
