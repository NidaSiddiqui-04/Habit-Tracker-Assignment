from . import views
from django.urls import path


app_name='habit'
urlpatterns=[
    path('create_habit/',views.create_habit,name='create_habit'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/habit_status/<int:id>/',views.habit_done_for_day,name='habit_status'),
    path('admin_dashboard/',views.admin_user_list,name='admin_dashboard'),
    path('deactivate/<int:id>',views.deactivate_user,name='deactivate_user'),
    path('weekly_report/',views.weekly_report,name='weekly_report'),
    path('habit_view/<int:id>/',views.view_habit,name='habit_view'),
    path('task_view/<int:id>/',views.view_task,name='task_view')
 ]
