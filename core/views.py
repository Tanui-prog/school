from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Subject
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')


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
