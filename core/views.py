from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from .models import Subject, Class
from django.contrib import messages




# Create your views here.
def index(request):
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

def teachers(request):
    return render(request, 'teachers.html')


def addteacher(request):
    return render(request, 'add-teacher.html')