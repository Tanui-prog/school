from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Subject, Class
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Classes

def add_class(request):
    if request.method == 'POST':
        form = Class(request.POST)
        if form.is_valid():
            grade = request.POST["grade"]
            stream = request.POST["stream"]
        
            Class = Class(grade=grade, stream=stream)
            Class.save()
        
            messages.success(request, 'Class added successfully')
            return redirect('add_class')
    
    else:
        return render(request, 'add-class.html', {'message': 'Please fill in the class details'})



def classes(request):
    classes = Class.objects.all()
    context = {
        'classes': classes
    }
    return render(request, 'classes.html', context)
    




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
