from django.shortcuts import render,redirect
from .models import AddProjectForm, Project
from django.contrib import messages

# Create your views here.
def homepage(request):

    return render(request,'index.html')

def new_post(request):
    project=Project.objects.all()
    if request.method=='POST':
        current_user=request.user
        form=AddProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.user=current_user
            project.save()
            messages.success(request,('Project was posted successfully!'))
            return redirect('home')
    else:
            form=AddProjectForm()

    return render(request,'new-post.html')