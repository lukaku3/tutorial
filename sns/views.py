from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message,Friend,Group,Good
from .forms import GroupCheckForm,GroupSelectForm,SearchForm,CreateGroupForm,PostForm
# Create your views here.
