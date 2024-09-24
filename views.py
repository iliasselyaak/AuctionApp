from django.http import HttpResponse,HttpRequest,JsonResponse
import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import User, Profile,Item, Messages
from .forms import Login, SignupForm

# Create your views here.

@login_required
def spa_view(request):
    return render(request, "auctionapp/spa/index.html")

def base_index(request):
    return HttpResponse("Hello, world. You're at the base index.")

def sign_up(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            dob = form.cleaned_data['date_of_birth']
            newUser = User.objects.create(email = email,username = username,date_of_birth = dob)
            newUser.set_password(password)
            newUser.save()

            user =auth.authenticate(username=username, password =password)

            if user is not None:
                auth.login(request,user)
                print("Signed in")
                return redirect('auctionapp:app') #FILL IN
    
    return render(request, 'auctionapp/auth/signup.html', {'form': SignupForm})

def login_view(request):
    form = Login()
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                username = User.objects.get(email=email).username
            except User.DoesNotExist:
                return HttpResponse("User does not exist")
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user is not None:
                auth.login(request,user)
                print("Logged in")
                return redirect('auctionapp:app')
            # return render(request, 'error.html', {
            #     'error': 'User not registered. Sign up first.'
            # })

        # invalid form
    return render(request, 'auctionapp/auth/login.html', {
        'form': form
    })


def GET_User(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        # print(request.user.date_of_birth)
        return JsonResponse({"id": request.user.id, "username": request.user.username, "email": request.user.email, "dob":request.user.date_of_birth})
    else:
        return JsonResponse({"id": "user is not authenticated", "username": "user is not authenticated","email": "user is not authenticated", "dob":"user is not authenticated"})

def Change_User_Profile(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if request.method == 'PUT':
            body = json.loads(request.body)
            request.user.email = body['email']
            request.user.date_of_birth = body['dob']
        request.user.save()
        return JsonResponse(dict(email=request.user.email))
    else:
        return JsonResponse({"email": "user is not authenticated", "dob":"user is not authenticated"})

def fetch_profile_image(request : HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user = request.user
        if user.Profile:
            if not user.Profile.image:
                return JsonResponse(dict(url="/static/profile-image.jpg"))
            return JsonResponse(dict(url=user.Profile.image.url))
        else:
            return JsonResponse(dict(url="/static/profile-image.jpg"))
    else:
        return JsonResponse({"image":"user is authenticated"})

@login_required
def Item_api(request: HttpRequest)->HttpResponse:
    if request.method == 'GET':
        return JsonResponse({
            'items': [
                item.to_dict()
                for item in Item.objects.all()
            ]
        })
        
    if  request.method == 'POST':
        body = json.loads(request.body)
        # Define the format of the datetime string
        datetime_format = '%Y-%m-%d'

        # Convert the datetime string to a datetime object using the defined format
        datetime_obj = datetime.strptime(body['bid_time_finish'], datetime_format)
        print(body['owner'])
        
        item = Item.objects.create(
                    start_bid = body['start_bid'],
                    bid = body['start_bid'],
                    title=body['title'],
                    description = body['description'],
                    bid_time_finish = datetime_obj,
                    bought = False,
                    owner = User.objects.get(id=body['owner']),
                    last_bidder = User.objects.get(id=body['owner'])
                )
        item.save()
        return JsonResponse(dict(id=item.id))
    if  request.method == 'PUT':
        body = json.loads(request.body)
        Item.objects.filter(id=body['id']).update(
                    bid = body['bid'],
                    title=body['title'],
                    description = body['description'],
                    bid_time_finish = body['bid_time_finish'],
                    bought = body['bought'],
                    last_bidder = User.objects.get(id=body['last_bidder_id'])
            )
        return JsonResponse(dict(id=body['id']))

@login_required
def GET_ItemSearch(request: HttpRequest, profile_id: int)-> HttpResponse:
    #We might change to work serilizers
    item = get_object_or_404(Item, id=profile_id) 
    if request.method =='GET':
        return JsonResponse(item.to_dict())

@login_required
def profile_GET(request: HttpRequest, profile_id: int)-> HttpResponse:
    profile = get_object_or_404(Profile, id=profile_id) 
    if request.method =='GET':
        return JsonResponse(profile.to_dict())
    
    if request.method == 'PUT':
        profile = get_object_or_404(Profile, id=profile_id)
        request=request.body
        change = json.loads(request)
        profile.bio = change['bio']
        profile.save()
        return JsonResponse({
            'profile': [
                profile.to_dict()
                for profile in Profile.objects.all()
            ]
        })


@login_required
def profile_POST(request):
    user = request.user
    if 'bio' in request.POST and request.POST['bio']:
        bio = request.POST['bio']
        if user.profile:
            user.profile.bio = bio
            user.profile.save()
        else:
            profile = Profile(bio=bio)
            profile.save()
            user.profile = profile
        user.save()
    return JsonResponse({
        'profile':[
            profile.to_dict()
            for profile in Profile.objects.all()
        ]
    })


@login_required
#needs fixing
def messages_api(request: HttpRequest)->HttpResponse:

    if request.method == 'GET':
        return JsonResponse({
            'messages': [
                messages.to_dict()
                for messages in Messages.objects.all()
            ]
        })
    
    if request.method == 'POST':
        print("here->",request.body)
        body = json.loads(request.body)
        print("here!")
        message = Messages.objects.create(
                    question_message=body['text'],
                    sender=User.objects.get(id=body['sender']),
                    receiver=User.objects.get(id=body['receiver']),
                    item=Item.objects.get(id=body['item'])
                    )
        return JsonResponse({
            'messages': [
                messages.to_dict()
                for messages in Messages.objects.all()
            ]
        })


@login_required
def logout(request):
    auth.logout(request)
    return redirect('auctionapp/auth/login.html')



@login_required
def message_winner(request):
    #cron job
    return