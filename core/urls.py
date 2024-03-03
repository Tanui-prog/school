from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='dashboard'), 
    path('home', views.home, name='dashboard'),
   


    path('add_class', views.add_class, name='add_class'),
    path('classes', views.classes, name='classes'),
    path('saveclass/<int:class_id>/', views.saveclass, name='saveclass'),
    path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),

    path('addsubject', views.addsubject, name='addsubject'),
    path('subjects', views.subjects, name='subjects'),
    path('editsubject/<int:subject_id>/', views.editsubject, name='editsubject'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    path('teachers', views.teachers, name='teachers'),
    path('addteacher', views.addteacher, name='addteacher'),
    path('editteacher/<int:teacher_id>/', views.editteacher, name='editteacher'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('teachers_grid', views.teachers_grid, name='teachers_grid'),
    path('teacher_details/<int:teacher_id>/', views.teacher_details, name='teacher_details'),
    

    path('students', views.students, name='students'),
    path('addstudent', views.addstudent, name='addstudent'),
    path('editstudent', views.editstudent, name='editstudent'),
    path('delete-student', views.delete_student, name='delete_student'),
    path('students_grid', views.students_grid, name='students_grid'),
    path('student_details', views.student_details, name='student_details'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)