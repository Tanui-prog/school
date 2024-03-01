
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from .models import Subject, Class, Teacher, Students
from django.contrib import messages




# Create your views here.
def home(request):
    return render(request, 'index.html')







# Classes
def classes(request):
    classes = Class.objects.all()
    context = {
        'classes': classes
    }
    return render(request, 'classes.html', context)
    


def add_class(request):
    if request.method == 'POST':
        grade = request.POST.get("grade")
        stream = request.POST.get("stream")
        
        # Check if class already exists
        if Class.objects.filter(grade=grade, stream=stream).exists():
            messages.error(request, 'Class already exists')
            return redirect('add_class')
        else:
            # If class does not exist, save it
            Class.objects.create(grade=grade, stream=stream)
            messages.success(request, 'Class added successfully')
            return redirect('add_class')  
        # Redirect to the same page after adding a class

    else:
        return render(request, 'add-class.html', {'message': 'Please fill in the class details'})


def saveclass(request, class_id):
    try:
        # Retrieve the class object
        class_obj = Class.objects.get(class_id=class_id)
    except Class.DoesNotExist:
        messages.error(request, "Class does not exist.")
        return redirect('classes')  # Redirect to classes page if class does not exist

    if request.method == 'POST':
        # Get form data
        grade = request.POST.get('grade')
        stream = request.POST.get('stream')

        # Check if the submitted class details are unique
        if Class.objects.exclude(class_id=class_id).filter(grade=grade, stream=stream).exists():
            messages.error(request, "Another class with the same grade and stream already exists.")
            return render(request, 'edit-class.html', {'class': class_obj})  # Render the edit form with error message

        # Update class object
        class_obj.grade = grade
        class_obj.stream = stream
        class_obj.save()

        
        return redirect('classes')  # Redirect to classes page after successful update
    else:
        # If not POST, render edit form
        return render(request, 'edit-class.html', {'class': class_obj})
    



def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, class_id=class_id)
    class_obj.delete()
    return redirect('classes')




# SUBJECT
def addsubject(request):
    classes = Class.objects.all()  # Retrieve all classes from the database
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        class_id = request.POST.get('subject_class')  # Retrieve class_id from the POST data
        
        # Check if subject_name and subject_class are not empty
        if not subject_name or not class_id:
            messages.error(request, 'Subject name and class are required')
            return redirect('addsubject')  # Redirect back to the addsubject page or handle it appropriately
        
        try:
            # Retrieve the Class object using the class_id
            subject_class = Class.objects.get(class_id=class_id)
        except Class.DoesNotExist:
            # Handle the case where the class does not exist
            messages.error(request, 'Selected class does not exist')
            return redirect('addsubject')  # Redirect back to the addsubject page or handle it appropriately
        
        # Check if a subject with the same name and class already exists
        if Subject.objects.filter(subject_name=subject_name, subject_class=subject_class).exists():
            messages.error(request, 'A subject with the same name and class already exists')
            return redirect('addsubject')  # Redirect back to the addsubject page or handle it appropriately
        
        # Create and save the Subject instance
        subject = Subject(subject_name=subject_name, subject_class=subject_class)
        subject.save()
        
        messages.success(request, 'Subject added successfully')
        return redirect('addsubject')
    else:
        return render(request, 'add-subject.html', {'classes': classes})
    

def  subjects(request):
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request,'subjects.html',context)
 

def editsubject(request, subject_id):
    try:
        # Retrieve the subject object
        subject_obj = Subject.objects.get(subject_id=subject_id)
    except Subject.DoesNotExist:
        messages.error(request, "Subject does not exist.")
        return redirect('subjects')  # Redirect to subjects page if subject does not exist

    if request.method == 'POST':
        # Get form data
        subject_name = request.POST.get('subject_name')
        subject_class_id = request.POST.get('subject_class')

        try:
            # Retrieve the Class object using the class_id
            subject_class = Class.objects.get(class_id=subject_class_id)
        except Class.DoesNotExist:
            messages.error(request, 'Selected class does not exist')
            return redirect('editsubject', subject_id=subject_id)

        # Check if the submitted subject details are unique
        if Subject.objects.exclude(subject_id=subject_id).filter(subject_name=subject_name, subject_class=subject_class).exists():
            messages.error(request, "Another subject with the same name and class already exists.")
            return render(request, 'edit-subject.html', {'subject': subject_obj, 'classes': Class.objects.all()})  # Pass all classes to the template

        # Update subject object
        subject_obj.subject_name = subject_name
        subject_obj.subject_class = subject_class
        subject_obj.save()

        messages.success(request, 'Subject updated successfully')
        return redirect('subjects')  # Redirect to subjects page after successful update
    else:
        # If not POST, render edit form
        return render(request, 'edit-subject.html', {'subject': subject_obj, 'classes': Class.objects.all()})  # Pass all classes to the template



def  delete_subject(request, subject_id):
    subject_obj = get_object_or_404(Subject, subject_id=subject_id)
    subject_obj.delete()
    return redirect('subjects')



#teachers



def addteacher(request):
    if request.method == 'POST':
        identity_number = request.POST.get('identity_number')
        teacher_name = request.POST.get('teacher_name')
        teacher_gender = request.POST.get('teacher_gender')
        teacher_email = request.POST.get('teacher_email')
        teacher_phone = request.POST.get('phone_number')
        image = request.FILES.get('profile_picture')
        age = request.POST.get('age')
        joinin_date = request.POST.get('joining_date')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        city = request.POST.get('city')
        county = request.POST.get('county')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')
        tsc_no = request.POST.get('tsc_no')
        subject_combination = request.POST.get('subject_combinations')

        if Teacher.objects.filter(identity_number=identity_number, tsc_no=tsc_no).exists():
            messages.error(request, 'Teacher with the same identity number already exists')
            return redirect('addteacher')
            
        else:

            default_image_path = os.path.join(settings.MEDIA_ROOT, 'default.jpg')
            Teacher.objects.create(identity_number=identity_number, teacher_name=teacher_name, teacher_gender=teacher_gender,
                                        teacher_email=teacher_email, teacher_phone=teacher_phone, age=age, joinin_date=joinin_date,
                                        qualification=qualification, experience=experience, image=default_image_path,
                                        address=address, city=city, county=county, country=country, zip_code=zip_code, tsc_no=tsc_no,
                                        subject_combination=subject_combination)
        messages.success(request, 'Teacher added successfully')
        return redirect('addteacher')
    else:
        return render(request, 'add-teacher.html')



def teachers(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers.html',context)


def  delete_teacher(request, teacher_id):
    teacher_obj = get_object_or_404(Teacher, teacher_id=teacher_id)
    teacher_obj.delete()
    return redirect('teachers')


def editteacher(request, teacher_id):

    try:
        # Retrieve the teacher object
        teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher does not exist.")
        return redirect('teachers')  # Redirect to teachers page if teacher does not exist

    if request.method == 'POST':
        # Get form data
        identity_number = request.POST.get('identity_number')
        teacher_name = request.POST.get('teacher_name')
        teacher_gender = request.POST.get('teacher_gender')
        age = request.POST.get('age')
        teacher_phone = request.POST.get('phone_number')
        joinin_date = request.POST.get('joining_date')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        teacher_email = request.POST.get('teacher_email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        county = request.POST.get('county')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        tsc_no = request.POST.get('tsc_no')
        subject_combination = request.POST.get('subject_combination')

        # Check if the submitted teacher details are unique
        if Teacher.objects.exclude(teacher_id=teacher_id).filter(identity_number=identity_number).exists():
            messages.error(request, "Another teacher with the same identity number already exists.")
            return render(request, 'edit-teacher.html', {'teacher': teacher})  # Render the edit form with error message

        # Update teacher object
        teacher.identity_number = identity_number
        teacher.teacher_name = teacher_name
        teacher.teacher_gender = teacher_gender
        teacher.age = age
        teacher.teacher_phone = teacher_phone
        teacher.joinin_date = joinin_date
        teacher.qualification = qualification
        teacher.experience = experience
        teacher.teacher_email = teacher_email
        teacher.address = address
        teacher.city = city
        teacher.county = county
        teacher.zip_code = zip_code
        teacher.country = country
        teacher.tsc_no = tsc_no
        teacher.subject_combination = subject_combination
        teacher.save()

        messages.success(request, "Teacher details updated successfully.")
        return redirect('editteacher', teacher_id=teacher_id) 

    else:
        # If not POST, render edit form
        return render(request, 'edit-teacher.html', {'teacher': teacher})
    

def  teachers_grid(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers-grid.html', context)


def teacher_details(request,teacher_id):
    teacher_obj= Teacher.objects.get(teacher_id=teacher_id)
    context = {'teacher': teacher_obj}
    return render(request, 'teacher-details.html', context)



# students



def addstudent(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_gender = request.POST.get('gender')
        joining_date = request.POST.get('joining_date')
        admission_no = request.POST.get('admission_no')
        blood_group = request.POST.get('blood_group')
        religion = request.POST.get('religion')
        age = request.POST.get('age')
        Class = request.POST.get('classstream')
        session = request.POST.get('session')

        image = request.FILES.get('profile_picture') 
        parent_name = request.POST.get('parent_name')
        parent_email = request.POST.get('parent_email')
        parent_phone = request.POST.get('parent_phone')
        parent_address = request.POST.get('address')
        parent_reltionship = request.POST.get('relationship')

        if Students.objects.filter(admission_no=admission_no).exists():
            messages.error(request, 'Student with the same admission number already exists')
            return redirect('addstudent')
        
        else:
            
            student = Students(first_name=first_name, last_name=last_name, student_gender=student_gender,
            joining_date=joining_date, admission_no=admission_no, blood_group=blood_group, religion=religion, age=age, Class=Class, session=session, image=image, parent_name=parent_name, parent_email=parent_email, parent_phone=parent_phone, parent_address=parent_address, parent_relationship=parent_reltionship)
            student.save()
            
            messages.success(request, 'Student added successfully')
            return redirect('addstudent')
    
    
    else:
        return render(request, 'add-student.html')
    
        
def students(request):
    students = Students.objects.all()
    context = {'students': students}
    return render(request, 'students.html', context)

def student_details(request):
    return render(request, 'student-details.html')

def students_grid(request):
    return render(request, 'students-grid.html')

def editstudent(request):
    return render(request, 'edit-student.html')

def delete_student(request):
    return render(request, 'delete-student.html')

