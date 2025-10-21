from django.shortcuts import render,redirect
from .forms import SignUp,ProfileForm
from django.http import HttpResponse
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from . models import CustomUser
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
# Create your views here.


def register(request):
    form=SignUp(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=True
            user.save()
            messages.success(request,f"{user.username} ,you have been successfully signed up. you can login now.")  
            return redirect('user_profile:login')
    print(form.errors)
    return render(request,'user_profile/register.html',{'form':form}) 

class CustomLoginView(LoginView):

     def get_success_url(self):
         user=self.request.user
         if user.is_superuser or user.is_staff:
             return reverse_lazy('habit:admin_dashboard')
         else:
             return reverse_lazy('user_profile:detail_view')
    
def logout_view(request):
    logout(request)

    return render(request,'user_profile/logout.html')

@login_required(login_url='user_profile:login')
def add_user_profile(request):
 
    profile,created=CustomUser.objects.get_or_create(username=request.user.username)
    form=ProfileForm(request.POST or None,instance=profile)
    if request.method=="POST":
     
        if form.is_valid():
            profile=form.save(commit=True)
            profile.user=request.user
            profile.save()
            return redirect('user_profile:detail_view')
        
    return render(request,'user_profile/add_user_profile.html',{'form':form})

@login_required(login_url='user_profile:login ')
def detail_page(request):
    profile=CustomUser.objects.filter(username=request.user.username)
    return render(request,'user_profile/profile_view.html',{'profile':profile})
