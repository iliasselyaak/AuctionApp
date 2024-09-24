#messages, upload, 

from django.http.response import HttpResponseBadRequest, JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import User, Profile, Item, Messages
from django.contrib.auth.decorators import login_required

@login_required
def change_image(request):
    user = request.user
    print("hello1")
    if 'image' in request.FILES:
        image = request.FILES['image']
        if not user.Profile:
            print("hello2")
            profile = Profile(bio='')
            profile.save()
            user.Profile = profile
            user.save()
        #assumes profile has already been created before user can run this
        print("hello3")
        user.Profile.image = image
        user.Profile.save()
        return HttpResponse(user.Profile.image.url)
    else:
        print("hello4")
        raise Http404('No image received')


#@login_required
def addItemImage(request, item_id : int):
    item = get_object_or_404(Item, id=item_id)
    print(request.FILES)
    if 'image' in request.FILES:
        image = request.FILES['image']
        item.image = image
        item.save()
        return HttpResponse(item.image.url)
    else:
        raise Http404('No image received')


@login_required
def messages_api(request):
    user = request.user
    view = request.GET['view'] if 'view' in request.GET else user.username

    if request.method == 'POST':
        receiver = User.objects.get(username=request.POST['receiver'])
        question_message = request.POST['question_message']
        Messages.objects.create(
            sender=user,
            receiver=receiver,
            question_message=question_message,
        )

    if user.username != view:
        view_user = get_object_or_404(User, username=view)
        messages = user.messages_senrec(view_user)
    else:
        messages = user.messages

    return JsonResponse({
        'messages': [message.to_dict() for message in messages]
    })

#do we want delete message?