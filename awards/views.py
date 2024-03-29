from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/accounts/login/")
def index(request):
    projectss = Projects.objects.all()

    return render(request, "index.html", locals())

def home (request):
    
    return render(request, "index.html", locals())

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            return render(request, "registration/login.html/")
    else:
        form = SignupForm()
    return render(request, "registration/registration_form.html", {"form": form})


def profile(request):
    images = Profile.objects.all()
    current_user = request.user
    profile = Profile.objects.all()
    posts = Profile.objects.all()
    image_form = ProfileForm()
    if request.method == "POST":
        image_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
        else:
            image_form = ProfileForm()

    return render(request, "profile.html", {"image_form": image_form, "profile": profile, "images": images},)


def upload(request):
    current_user = request.user
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            projects = form.save(commit=False)
            projects.poster = current_user
            projects.save()
        return redirect("index")

    else:
        form = ProjectForm()
    return render(request, "upload.html", {"form": form})


@login_required(login_url="/accounts/login/")
def project(request, project_id):
    projects = Projects.objects.get(id=project_id)
    form_ = VoteForm()
    return render(request, "project.html", locals())
