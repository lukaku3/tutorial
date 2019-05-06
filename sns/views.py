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
    (public_user, public_group) = get_public()

    if request.method == 'POST':
        if request.POST['mode'] == '__check_form__':
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user, request.POST)
            glist = []
            for item in request.POST.getlist('groups'):
                glist.append(item)
            messages = get_your_group_message(request.user, glist, None)
        
        if request.POST['mode'] == '__search_form__':
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user, request.POST)
            gps = GroupCheckForm(request.user)
            glist = [public_group]
            for item in gps:
                glist.append(item)
            messages = get_your_group_message(request.user, glist, request.POST['search'])

        else:
            searchform = SearchForm()
            checkform = GroupCheckForm(request.user)
            gps = GroupCheckForm(request.user)
            glist = [public_group]
            for item in gps:
                glist.append(item)
            messages = get_your_group_message(request.user, glist, None)

    else:
        searchform = SearchForm()
        checkform = GroupCheckForm(request.user)
        gps = Group.objects.filter(owner=request.user)
        glist = [public_group]
        for item in gps:
            glist.append(item)
        messages = get_your_group_message(request.user, glist, None)

    params = {
        'login_user':request.user,
        'contents':messages,
        'check_form':checkform,
        'search_form':searchform,
    }
    return render(request, 'sns/index.html', params)

@login_required(login_url='/admin/login/')
def groups(request):
    friends = Friend.objects.filter(owner=request.user)
    if request.method == 'POST':
        if request.POST['mode'] == '__groups_form__':
            sel_group = request.POST['groups']
            gp = Group.objects.filter(owner=request.user).filter(title=sel_group).first()
            fds = Friend.objects.filter(owner=request.user).filter(group=gp)
            vlist = []
            for item in fds:
                vlist.append(item.user.username)
            groupsform = GroupSelectForm(request.user, request.POST)
            friendsform = FriendsForm(request.user, friends=friends, vals=vlist)

        if request.POST['mode'] == '__friends_form__':
            sel_group = request.POST['POST']
            group_obj = Group.objects.filter(title=sel_group).first()
            sel_fds = request.POST.getlist('friends')
            sel_users = User.objects.filter(username__in=sel_fds)
            fds = Friend.objects.filter(owner=request.user).filter(user__in=sel_users)
            vlist = []
            for item in fds:
                item.group = group_obj
                item.save()
                vlist.append(item.user.username)
            messages.success(request, 'チェックされたFriendを' + sel_group + 'に登録しました。')
            groupsform = GroupSelectForm(request.user, {'groups':sel_group})
            friendsform = FriendsForm(request.user, frieds=friends, vals=vlist)

    else:
        groupsform = GroupSelectForm(request.user)
        friendsform = FriendsForm(request.user, frieds=friends, vals=[])
        sel_group = '-'

    createform = CreateGroupForm()
    params = {
        'login_user':request.user,
        'groups_form':groupsform,
        'friends_form':friendsform,
        'create_form':createform,
        'group':sel_group,
    }
    return render(request, 'sns/groups.html', params)


def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter(owner=public_user).first()
    return (public_user, public_group)

def add(request):

    pass

@login_required(login_url='/admin/login/')
def post(request):
    if request.method == 'POST':
        gr_name = request.POST['groups']
        content = request.POST['content']
        group = Group.objects.filter(owner=request.user).filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.save()
        messages.success(request, '新しいメッセージを投稿しました。')
        return redirect(to='/sns')
    else:
        form = PostForm(request.user)

    params = {
        'login_user':request.user,
        'form':form
    }
    return render(request, 'sns/post.html', params)

def creategroup(request):

    pass

def share(request):

    pass

def good(request):

    pass

def get_your_group_message(owner, glist, find):
    (public_user,public_group) = get_public()
    group = Group.objects.filter(Q(owner=owner)|Q(owner=public_user)).filter(title__in=glist)
    pass
