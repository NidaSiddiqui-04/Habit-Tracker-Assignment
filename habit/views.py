from django.shortcuts import render, redirect,get_object_or_404
from .models import Habit,HabitCompletion
from .forms import HabitForm
import datetime
from task.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Count
# Create your views here.
User=get_user_model()

def create_habit(request):
    form= HabitForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            user=form.save(commit=False)
            user.user=request.user
            user.save()
            return redirect('habit:dashboard')
        
    return render(request,'habit/create_habit.html',{'form':form})

@login_required(login_url='user_profile:login')
def dashboard(request):
    habit=None
    streak=0
    today = datetime.date.today()
    yesterday=today-datetime.timedelta(days=1)
    habits= Habit.objects.filter(user=request.user)

    daily_habits = []
    for habit in habits.filter(frequency='Daily'):
        completed = habit.completion.filter(date=today).exists()
        daily_habits.append((habit, completed))
        
    
    weekly_habits = []
    for habit in habits.filter(frequency='Weekly'):
        completed=habit.completion.filter(date=today).exists()
        weekly_habits.append((habit,completed))


    
    if habit is not None:
          completion = habit.completion.filter(date=today).exists()
          
    else:
             completion = None 
             
              
    task=Task.objects.filter(user=request.user,status='Pending').order_by('due_date') 
    return render(request, 'habit/habits.html', {
        'habits':habits,
        'daily_habits': daily_habits,
        'weekly_habits': weekly_habits,
        'today': today,
        'task':task,
        'completion':completion,
        'habit':habit,
        'streak':streak
        
         
       })

def habit_done_for_day(request, id):
    today = datetime.date.today()
    habit = get_object_or_404(Habit, id=id, user=request.user)
    HabitCompletion.objects.get_or_create(name=habit, date=today)
    return redirect('habit:dashboard')



def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def admin_user_list(request):
    users=User.objects.all()
    
    return render(request,'habit/admin_dashboard.html',{'users':users})

@user_passes_test(is_admin)
def view_habit(request,id): 
    user=get_object_or_404(User,id=id)
    habits=Habit.objects.filter(user=user)

    return render(request,'habit/view_habit.html',{'user':user,'habits':habits})


@user_passes_test(is_admin)
def view_task(request,id):
    user=get_object_or_404(User,id=id)
    tasks=Task.objects.filter(user=user)
    return render(request,'habit/view_task.html',{'user':user,'tasks':tasks})


@user_passes_test(is_admin)
def deactivate_user(requqest,id):
    user=get_object_or_404(User,id=id)
    user.is_active=False
    user.save()
    return redirect('habit:admin_dashboard')




 

def weekly_report(request):
    
    
    today = datetime.date.today()
    yesterday=today-datetime.timedelta(days=1)
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    
    # Tasks
    tasks = Task.objects.filter(user=request.user, due_date__range=[start_of_week, end_of_week])
    completed_tasks = tasks.filter(status='Done')
    pending_tasks = tasks.filter(status='Pending')

    # Tasks per day for Chart.js
    tasks_per_day = []
    for i in range(7):
        day = start_of_week + datetime.timedelta(days=i)
        count = completed_tasks.filter(due_date=day).count()
        tasks_per_day.append({'day': day.strftime('%a'), 'count': count})
       
    # Habits
    habits = Habit.objects.filter(user=request.user)

    completions = HabitCompletion.objects.filter( date__range=[start_of_week, end_of_week])

    habit_report = []
    for habit in habits:
    
        count = habit.completion.filter(date__range=[start_of_week,end_of_week]).count()
    
        if habit.frequency == 'Daily':
             weekly_target=habit.target*7
             percentage=((count*habit.target)/weekly_target)*100
        else:
             weekly_target=habit.target
             
             percentage = (count / weekly_target) * 100 
       # streak 
        completion = habit.completion.filter(date=today).exists()
        yesterday_=habit.completion.filter(date=yesterday).exists()
          
        if completion and yesterday_:
            habit.streaks+=1
        
                  
        elif completion and not yesterday_:
            habit.streaks=1
            
            
        elif yesterday_ and not completion:
            habit.streaks  
            
        else:
            habit.streaks=0
            
              
                 
        habit_report.append({
            'habit': habit.title,
            'completed': count,
            'target': weekly_target,
            'percentage': round(percentage, 2),
            'streaks':habit.streaks
            
        })

    context = {
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'habit_report': habit_report,
        'tasks_per_day': tasks_per_day,
        
        
    }
    return render(request, 'habit/weekly_report.html', context)