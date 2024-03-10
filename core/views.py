
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from .models import Subject, Classes, Teacher, Students
from django.contrib import messages
from django.db.models import Q




# Create your views here.
def home(request):
    return render(request, 'index.html')







# Classes
def classes(request):
    classes = Classes.objects.all()
    context = {
        'classes': classes
    }
    return render(request, '_class/classes.html', context)
    


def add_class(request):
    if request.method == 'POST':
        grade = request.POST.get("grade")
        stream = request.POST.get("stream")
        
        # Check if class already exists
        if Classes.objects.filter(grade=grade, stream=stream).exists():
            messages.error(request, 'Class already exists')
            return redirect('add_class')
        else:
            # If class does not exist, save it
            Classes.objects.create(grade=grade, stream=stream)
            messages.success(request, 'Class added successfully')
            return redirect('add_class')  
        # Redirect to the same page after adding a class

    else:
        return render(request, '_class/add-class.html', {'message': 'Please fill in the class details'})


def saveclass(request, class_id):
    try:
        # Retrieve the class object
        class_obj = Classes.objects.get(class_id=class_id)
    except Classes.DoesNotExist:
        messages.error(request, "Class does not exist.")
        return redirect('classes')  # Redirect to classes page if class does not exist

    if request.method == 'POST':
        # Get form data
        grade = request.POST.get('grade')
        stream = request.POST.get('stream')

        # Check if the submitted class details are unique
        if Classes.objects.exclude(class_id=class_id).filter(grade=grade, stream=stream).exists():
            messages.error(request, "Another class with the same grade and stream already exists.")
            return render(request, 'edit-class.html', {'class': class_obj})  # Render the edit form with error message

        # Update class object
        class_obj.grade = grade
        class_obj.stream = stream
        class_obj.save()

        
        return redirect('classes')  # Redirect to classes page after successful update
    else:
        # If not POST, render edit form
        return render(request, '_class/edit-class.html', {'class': class_obj})
    



def delete_class(request, class_id):
    class_obj = get_object_or_404(Classes, class_id=class_id)
    class_obj.delete()
    return redirect('classes')




# SUBJECT
def addsubject(request):
    classes = Classes.objects.all()  # Retrieve all classes from the database
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        class_id = request.POST.get('subject_class')  # Retrieve class_id from the POST data
        
        # Check if subject_name and subject_class are not empty
        if not subject_name or not class_id:
            messages.error(request, 'Subject name and class are required')
            return redirect('addsubject')  # Redirect back to the addsubject page or handle it appropriately
        
        try:
            # Retrieve the Class object using the class_id
            subject_class = Classes.objects.get(class_id=class_id)
        except Classes.DoesNotExist:
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
        return render(request, 'subjects/add-subject.html', {'classes': classes})
    

def  subjects(request):
    subjects = Subject.objects.all()
    context = {'subjects': subjects}
    return render(request,'subjects/subjects.html',context)
 

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
            subject_class = Classes.objects.get(class_id=subject_class_id)
        except Classes.DoesNotExist:
            messages.error(request, 'Selected class does not exist')
            return redirect('editsubject', subject_id=subject_id)

        # Check if the submitted subject details are unique
        if Subject.objects.exclude(subject_id=subject_id).filter(subject_name=subject_name, subject_class=subject_class).exists():
            messages.error(request, "Another subject with the same name and class already exists.")
            return render(request, 'edit-subject.html', {'subject': subject_obj, 'classes': Classes.objects.all()})  # Pass all classes to the template

        # Update subject object
        subject_obj.subject_name = subject_name
        subject_obj.subject_class = subject_class
        subject_obj.save()

        messages.success(request, 'Subject updated successfully')
        return redirect('subjects')  # Redirect to subjects page after successful update
    else:
        # If not POST, render edit form
        return render(request, 'subjects/edit-subject.html', {'subject': subject_obj, 'classes': Classes.objects.all()})  # Pass all classes to the template



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
        
        if image:
            Teacher.objects.create(identity_number=identity_number, teacher_name=teacher_name, teacher_gender=teacher_gender,
                                        teacher_email=teacher_email, teacher_phone=teacher_phone, age=age, joinin_date=joinin_date,
                                        qualification=qualification, experience=experience, image=image,
                                        address=address, city=city, county=county, country=country, zip_code=zip_code, tsc_no=tsc_no,
                                        subject_combination=subject_combination)
            
        else:

            default_image_path = 'default.jpg'
            Teacher.objects.create(identity_number=identity_number, teacher_name=teacher_name, teacher_gender=teacher_gender,
                                        teacher_email=teacher_email, teacher_phone=teacher_phone, age=age, joinin_date=joinin_date,
                                        qualification=qualification, experience=experience, image=default_image_path,
                                        address=address, city=city, county=county, country=country, zip_code=zip_code, tsc_no=tsc_no,
                                        subject_combination=subject_combination)
        messages.success(request, 'Teacher added successfully')
        return redirect('addteacher')
    else:
        return render(request, 'teachers/add-teacher.html')



def teachers(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers/teachers.html',context)


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
        image = request.FILES.get('profile_picture', None)  # Get the new image or None
        city = request.POST.get('city')
        county = request.POST.get('county')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        tsc_no = request.POST.get('tsc_no')
        subject_combination = request.POST.get('subject_combination')

        # Update teacher object with new data
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
        if image:  # If a new image is uploaded
            teacher.image = image
        teacher.city = city
        teacher.county = county
        teacher.zip_code = zip_code
        teacher.country = country
        teacher.tsc_no = tsc_no
        teacher.subject_combination = subject_combination
        teacher.save()

        messages.success(request, "Teacher details updated successfully.")
        return redirect('editteacher', teacher_id=teacher_id)

    # For GET requests, populate form fields with existing data
    return render(request, 'teachers/edit-teacher.html', {'teacher': teacher})



def  teachers_grid(request):
    teachers = Teacher.objects.all()
    context = {'teachers': teachers}
    return render(request, 'teachers/teachers-grid.html', context)


def teacher_details(request,teacher_id):
    teacher_obj= Teacher.objects.get(teacher_id=teacher_id)
    context = {'teacher': teacher_obj}
    return render(request, 'teachers/teacher-details.html', context)



# students



def addstudent(request):
    classes = Classes.objects.all()
    
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_gender = request.POST.get('gender')
        joining_date = request.POST.get('joining_date')
        admission_no = request.POST.get('admission_no')
        blood_group = request.POST.get('blood_group')
        religion = request.POST.get('religion')
        age = request.POST.get('age')
        student_class = request.POST.get('student_class')  # Assuming this is the class ID
        session = request.POST.get('session')
        image = request.FILES.get('profile_picture') 
        parent_name = request.POST.get('parent_name')
        parent_email = request.POST.get('parent_email')
        parent_phone = request.POST.get('parent_phone')
        parent_address = request.POST.get('address')
        parent_relationship = request.POST.get('relationship')

        # Get the Classes instance corresponding to the class ID
        student_class = Classes.objects.get(class_id=student_class)



        if image:
        # Create the Students instance
            student = Students(
                first_name=first_name,
                last_name=last_name,
                student_gender=student_gender,
                joining_date=joining_date,
                admission_no=admission_no,
                blood_group=blood_group,
                religion=religion,
                age=age,
                student_class=student_class,  # Assign the Classes instance
                session=session,
                image=image,
                parent_name=parent_name,
                parent_email=parent_email,
                parent_phone=parent_phone,
                parent_address=parent_address,
                parent_relationship=parent_relationship
            )
            student.save()
            messages.success(request, 'Student added successfully')
            return redirect('addstudent')
        
        else:
            default_image_path = 'default.jpg'
            student = Students(
                first_name=first_name,
                last_name=last_name,
                student_gender=student_gender,
                joining_date=joining_date,
                admission_no=admission_no,
                blood_group=blood_group,
                religion=religion,
                age=age,
                student_class=student_class,  
                session=session,
                image=default_image_path,
                parent_name=parent_name,
                parent_email=parent_email,
                parent_phone=parent_phone,
                parent_address=parent_address,
                parent_relationship=parent_relationship
            )
            student.save()
            messages.success(request, 'Student added successfully')
            return redirect('addstudent')


    else:
        return render(request, 'students/add-student.html', {'classes': classes})




def students(request):
    students = Students.objects.all()
    context = {'students': students}

    return render(request, 'students/students.html', context)

def student_details(request, student_id):
    student =get_object_or_404(Students,student_id = student_id)
    context = {"student":student}
    return render(request, 'students/student-details.html', context )

def students_grid(request):
    students = Students.objects.all()
    context = {'students' : students}
    return render(request, 'students/students-grid.html',context)

def editstudent(request, student_id):
    try:
        # Retrieve the student object
        student = get_object_or_404(Students, student_id=student_id)
        classes = Classes.objects.all()

    except Students.DoesNotExist:
        messages.error(request, "Student does not exist.")
        return redirect('students')  # Redirect to students page if student does not exist

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_gender = request.POST.get('gender')
        joining_date = request.POST.get('joining_date')
        admission_no = request.POST.get('admission_no')
        blood_group = request.POST.get('blood_group')
        religion = request.POST.get('religion')
        age = request.POST.get('age')
        student_class = request.POST.get('student_class')  
        session = request.POST.get('session')
        image = request.FILES.get('profile_picture') 
        parent_name = request.POST.get('parent_name')
        parent_email = request.POST.get('parent_email')
        parent_phone = request.POST.get('parent_phone')
        parent_address = request.POST.get('address')
        parent_relationship = request.POST.get('relationship')

        # get class instance
        student_class = get_object_or_404(Classes, class_id=student_class)

        # update details
        student.first_name =first_name
        student.last_name = last_name
        student.student_gender = student_gender
        student.joining_date = joining_date
        student.admission_no = admission_no
        student.blood_group = blood_group
        student.religion = religion
        student.age = age
        student.student_class = student_class
        student.session = session
        student.parent_name = parent_name
        student.parent_email = parent_email
        student.parent_phone = parent_phone
        student.parent_address = parent_address
        student.parent_relationship = parent_relationship
        if image:
            student.image = image
        student.save()
        messages.success(request, "Student details updated successfully.")
        return redirect('editstudent', student_id=student_id)



        
def searchteacher(request):
    if request.method == 'POST':
        searchbyid = request.POST.get('teacher_id')
        full_name = request.POST.get('teacher_name')
        phone = request.POST.get('phone_number')

        search_by_id = None
        search_by_name = None
        search_by_phone = None


       
        

        # Search by admission number (exact match)
        search_by_id = Teacher.objects.filter(tsc_no = searchbyid)
        # search by phone number
        search_by_phone = Teacher.objects.filter(teacher_phone = phone)

        # Search by full name
        search_by_name =Teacher.objects.filter(teacher_name=full_name)
        
        context = {"teachers": search_by_id,
                   "teachers":search_by_name,
                   "teachers":search_by_phone}

        return render(request, 'teachers/teachers.html', context)

    else:
        
        return render(request, 'teachers/teacher.html', {'teachers': teachers , 'classes': classes})



def delete_student(request):
    
    return render(request, 'students/delete-student.html')


def search(request):
    if request.method == 'POST':
        searchbyadm = request.POST.get('admission_no')
        full_name = request.POST.get('name')

        search_by_adm = None
        search_by_name = None

        if searchbyadm:
            # Search by admission number (exact match)
            search_by_adm = Students.objects.filter(admission_no=searchbyadm)

        # If admission number is empty, use name for search
        elif full_name:
            # Split full name into first name and last name
            names = full_name.split()
            first_name = names[0] if names else ""
            last_name = names[-1] if len(names) > 1 else first_name  # Use first name if last name is not provided
            
            # Search by full name
            search_by_name = Students.objects.filter(
                first_name=first_name, last_name=last_name
            )

            if not search_by_name:
                messages.error(request, "No student found with the provided name.")
                search_by_name = Students.objects.filter(
                    Q(first_name__icontains=first_name) | Q(last_name__icontains=last_name)
                )

        # If both admission number and name are empty, fall back to using admission number
        elif not search_by_adm:
            messages.error(request, "Please provide admission number or name for search.")
            search_by_adm = Students.objects.none()

        context = {"student": search_by_adm, "students": search_by_name}

        return render(request, 'students/students.html', context)