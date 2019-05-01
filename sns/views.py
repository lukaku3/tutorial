from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message,Friend,Group,Good
from .forms import GroupCheckForm,GroupSelectForm,SearchForm,CreateGroupForm,PostForm

from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/admin/login/')
def index(request):

    pass

def groups(request):

    pass

def add(request):

    pass

def post(request):

    pass

def creategroup(request):

    pass

def share(request):

    pass

def good(request):

    pass
