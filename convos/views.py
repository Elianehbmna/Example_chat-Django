from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Message, Convo
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

import pyrebase

config = {
  "apiKey": "AIzaSyA4_1_tLOwAvNdzMOat8DE-4CLy9Rg5anw",
  "authDomain": "eliane-chat.firebaseapp.com",
  "databaseURL": "https://eliane-chat.firebaseio.com",
  "storageBucket": "eliane-chat.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.child("chats")

def index(request):
    return HttpResponse('Welcome to convos app')

def get_convos(request, user_id):
    user = User.objects.filter(id=user_id).first()

    convos = Convo.objects.filter(members=user)

    response = []

    for convo in convos:
        convo_data = {
            "uuid": convo.uuid,
            "id": convo.id,
            "created_at": convo.created_at.isoformat(),
        }
        members = []

        for member in convo.members.all():
            memeber_data = {
                "username": member.username
            }

            members.append(memeber_data)
        convo_data['members'] = members
        response.append(convo_data)
    return JsonResponse(response, safe=False)



def get_messages(request, convo_uuid):
    convo = Convo.objects.filter(uuid=convo_uuid).first()
    messages = Message.objects.filter(convo=convo)

    response = []

    for message in messages:
        message_data = {
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }

        response.append(message_data)

    return JsonResponse(response, safe=False)


@csrf_exempt
def create_message(request):

    print(request.POST)

    """
    Get sent data
    """
    sender = request.POST.get('sender')
    receiver = request.POST.get('receiver')
    content = request.POST.get('content')
    convo_uuid = request.POST.get('convo_uuid')

    """
    Preparing required instances
    """

    if not convo_uuid:
        import time
        millis = round(time.monotonic() * 1000)
        convo_uuid = str(millis)

    convo = Convo.objects.filter(uuid=convo_uuid).first()
    sender = User.objects.filter(id=sender).first()
    receiver = User.objects.filter(id=receiver).first()

    if not convo:
        convo = Convo(
            uuid=convo_uuid
        )
        convo.save()
        convo.members.add(sender)
        convo.members.add(receiver)

    """
    Saving message
    """
    message = Message(
        sender=sender,
        receiver=receiver,
        convo=convo,
        content=content
    )

    message.save()

    message_data = {
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "created_at": message.created_at.isoformat(),
    }


    return JsonResponse(message_data, safe=False)



@csrf_exempt
def create_message_fb(request):
    db.child("chats")

    """
    Get sent data
    """
    sender = request.POST.get('sender')
    receiver = request.POST.get('receiver')
    content = request.POST.get('content')
    convo_uuid = request.POST.get('convo_uuid')

    """
    Preparing required instances
    """

    if not convo_uuid:
        import time
        millis = round(time.monotonic() * 1000)
        convo_uuid = str(millis)

    sender = User.objects.filter(id=sender).first()
    receiver = User.objects.filter(id=receiver).first()

    """
    Saving message
    """

    import time
    millis = round(time.monotonic() * 1000)
    created_at = str(millis)

    message_data = {
        "sender": sender.username,
        "receiver": receiver.username,
        "content": content,
        "created_at": created_at,
    }

    db.child(convo_uuid).child(created_at).set(message_data)


    return JsonResponse(message_data, safe=False)
