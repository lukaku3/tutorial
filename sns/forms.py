from django import forms
from .models import Message,Group,Friend,Good
from django.contrib.auth.models import User

class MassageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['owner','group','content']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['owner','title']

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['owner','user','group']

class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['owner','message']
