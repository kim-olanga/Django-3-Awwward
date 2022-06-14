from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):

    return render(request,'index.html')

def new_post(request):

    return render(request,'new-post.html')