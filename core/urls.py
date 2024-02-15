from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('addsubject', views.addsubject, name='addsubject'),
    path('add_class', views.add_class, name='add_class'),
    path('classes', views.classes, name='classes'),
    path('saveclass/<int:class_id>/', views.saveclass, name='saveclass'),
    path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),
]