from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('addsubject', views.addsubject, name='addsubject'),
    path('add_class', views.add_class, name='add_class'),
    path('classes', views.classes, name='classes'),
]