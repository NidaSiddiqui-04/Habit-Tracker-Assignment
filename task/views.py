from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Task
from .form import TaskForm,TaskStatus
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
# Create your views here.
@login_required
def create_task(request):

    form=TaskForm(request.POST or None , )
    if request.method=='POST':
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('habit:dashboard')
            
    return render(request,'task/create_task.html',{'form':form})         

def task_view(request):
    view=Task.objects.filter(user=request.user,status='Done').order_by('due_date')
    return render (request,'task/task.html',{'view':view})

def edit_task(request,id):
    form=TaskForm(request.POST or None ,instance=Task.objects.get(id=id))
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect('habit:dashboard')
        
    return render(request,'task/edit_task.html',{'form':form})

def delete_task(request,id):
    form=Task.objects.get(id=id)
    form.delete()
    return redirect('habit:dashboard')


def task_as_done(request,id):
    task=get_object_or_404(Task,id=id,user=request.user)
    if request.method=="POST":
        form=TaskStatus(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('task:task')
    form=TaskStatus(instance=task)
    return render(request,'task/update_task_status.html',{'form':form,'task':task})
       