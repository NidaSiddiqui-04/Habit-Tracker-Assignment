from django.urls import path
from . import views
from django.views.generic import View as a_views


app_name='task'
urlpatterns=[
    path('add_task/',views.create_task,name='add_task'),
    path('tasks/',views.task_view,name='task'),
    path('edit_task/<int:id>/',views.edit_task,name='edit_task'),
    path('delete_task/<int:id>',views.delete_task,name='delete_task'),
    path('done/<int:id>/',views.task_as_done,name='done'),
    
]