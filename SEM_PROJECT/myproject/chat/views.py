from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from pedal.models import User


# Create your views here.
def home(request):
    return render(request, "home.html")


def room(request, room):
    username = request.GET.get("username")
    room_details = Room.objects.get(name=room)
    return render(
        request,
        "room.html",
        {"username": username, "room": room, "room_details": room_details},
    )


def checkview(request):
    # room = request.POST["room_name"]
    # username = request.POST["username"]

    cycle_id = request.POST["cycle_id"]
    room = request.POST["cycle_id"] + str(request.POST["user_id"])
    username = request.POST["user_name"]
    # appUser = User.objects.get(id=username)
    if Room.objects.filter(name=room).exists():
        return redirect("/chat/" + room + "/?username=" + username)
    else:
        new_room = Room.objects.create(
            name=room, cycle_id=cycle_id, user_id=request.user.id
        )
        new_room.save()
        return redirect("/chat/" + room + "/?username=" + username)


def checkview_owner(request):
    # room = request.POST["room_name"]
    # username = request.POST["username"]

    room = request.POST["room_name"]
    username = request.POST["seller_name"]

    if Room.objects.filter(name=room).exists():
        return redirect("/chat/" + room + "/?username=" + username)
    # else:
    #     new_room = Room.objects.create(name=room, cycle_id=cycle_id)
    #     new_room.save()
    #     return redirect("/chat/" + room + "/?username=" + username)


def send(request):
    message = request.POST["message"]
    username = request.POST["username"]
    room_id = request.POST["room_id"]

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse("Message sent successfully")


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
