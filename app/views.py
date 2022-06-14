from email import message
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import Project, UserUpdateForm, ProfileUpdateForm, SignUpForm, NewProjectForm
from django.contrib import messages
from .models import Profile, Project

# Create your views here.
@login_required(login_url='/accounts/login/')
def homepage(request):
    project= Project.all_projects()
    json_projects = []
    for project in project:

        pic = Profile.objects.filter(user=project.user.id).first()
        if pic:
            pic = pic.profile_pic.url
        else:
            pic =''
        obj = dict(
            title=project.title,
            image=project.image,
            link=project.link,
            description=project.description,
            avatar=pic,
            date_craeted=project.date_craeted,
            author=project.user.username  
        )
        json_projects.append(obj)
    return render(request,'index.html',{"json_projects":json_projects})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request,'registration/register.html', {'form': form})

@login_required(login_url='/accounts/login/')
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f'Your account has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request,'profile.html',context)

@login_required(login_url='/accounts/login/')
def update_profile(request):
    if request.method == 'POST':
    
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('homepage')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
    return render(request,'update_profile.html',context)

def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()    
        return redirect('homepage')
    else:
        form = NewProjectForm()
    return render(request,'new_post.html',{"form":form})

def search_results(request):
    if 'project' in request.GET and request.GET['project']:
        search_term =request.GET.get('project')
        searched_project = Project.search_by_title(search_term)
        message = f'{search_term}'
        return render(request, 'search.html',{"message":message,"projects":searched_project})
    else:
        message = "You haven't searched for any term"
    return render(request,'search.html',{'message':message})