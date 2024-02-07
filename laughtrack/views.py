from django.db import models
from laughtrack.models import Event, Comedian, Comment
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.template import loader
from django.contrib.auth.models import User
from django.core.checks import Error
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def get_context(event_id, events):
    print(events)
    if events:
        event = events[0]
    if event_id:
        event = Event.objects.get(id=event_id)

    comments = event.comment_set.all().order_by('-pubdate')
    context = {'events':events, 'event':event, 'comments':comments}
    return context


def homepage(request, event_id=None):
    events = Event.objects.annotate(nfollowers=Count('comedian__followers')).order_by('-nfollowers') 
    context = get_context(event_id, events)
    context['page'] = reverse('laughtrack:homepage')
    context['comedians'] = Comedian.objects.all()
    # event = events[0]
    # if event_id:
    #     event = Event.objects.get(id=event_id)

    # comments = event.comment_set.all().order_by('-pubdate')
    # context = {'events':events,'comedians':Comedian.objects.all(), 'event':event, 'comments':comments, 'page':reverse('laughtrack:homepage')}

    return render(request,"laughtrack/homepage.html",context)

def comedianinfo(request, comedian_id, event_id=None):
    comedian = Comedian.objects.get(id=comedian_id)
    events = Event.objects.filter(comedian=comedian)
    
    if events:
        context = get_context(event_id, events)
        context['comedian'] = comedian
    else:
        context = {'comedian':comedian, 'events':events}
    
    context['page'] = reverse('laughtrack:comedian', args=(comedian_id,))

    return render(request,"laughtrack/comedian.html",context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        email = request.POST['Email']
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            print("That username already exists.")
            return render(request, 'laughtrack/signin.html', {'error': 'User Already Exists'})
        if user:
            login(request, user)
            return redirect('/laughtrack/home')
    else:
        return render(request, 'laughtrack/signin.html')
def signin(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('/laughtrack/home')
        else:
            print("Invalid")
    else:
        return render(request,'laughtrack/signin.html')

@login_required
def post_comment(request, event_id):
    currentevent = Event.objects.get(id=event_id)
    usercomment = request.POST['comment_text']
    comment = Comment(comment_text=usercomment,user=request.user,event=currentevent)
    comment.save()

    return redirect(request.META['HTTP_REFERER'])

def show_details(request,  event_id):
    event = Event.objects.get(id=event_id)
    comments = event.comment_set.all().order_by('-pubdate')
    print(request.META['HTTP_REFERER'])
    print("printing http referrer")
    return homepage(request,event,comments)
    
    
@login_required
def following(request, event_id=None):
    comedians = Comedian.objects.filter(followers=request.user)
    print(comedians)
    events = Event.objects.filter(comedian__in=comedians)
    if events:
        context = get_context(event_id, events)
    else:
        context = {}
    
    context['page'] = reverse('laughtrack:following')
    context['comedians'] = comedians


    print(request.user.username)
    return render(request,"laughtrack/following.html",context)

@login_required
def follow(request,comedian_id):
    comedian = Comedian.objects.get(pk=comedian_id)
    comedian.followers.add(request.user)
    comedian.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def unfollow(request,comedian_id):
    comedian = Comedian.objects.get(pk=comedian_id)
    comedian.followers.remove(request.user)
    comedian.save()
    return redirect(request.META['HTTP_REFERER'])

def logout_view(request):
    logout(request)
    return redirect('/laughtrack/home')