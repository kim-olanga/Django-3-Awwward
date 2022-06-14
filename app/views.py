from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

def new_post(request):

    return render(request,'new-post.html')