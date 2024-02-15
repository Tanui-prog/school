from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from .models import Subject, Class
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Classes

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

def classes(request):
    classes = Class.objects.all()
    context = {
        'classes': classes
    }
    return render(request, 'classes.html', context)
    

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


def addsubject(request):
    if request.method == 'POST':
        subject_name = request.POST['subject_name']
        subject_id = request.POST['subject_id']
        subject_class = request.POST['subject_class']
        
        subject = Subject(subject_name=subject_name, subject_id=subject_id, subject_class=subject_class)
        subject.save()
        messages.success(request, 'Subject added successfully')
        return redirect('addsubject')
    else:
        
        return render(request, 'add-subject.html', {'message': 'Please fill in the subject details'})
