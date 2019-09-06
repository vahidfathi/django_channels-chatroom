from django.utils.safestring import mark_safe
from django.contrib.auth import login, logout
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import ChatroomForm
from .models import Chatrooms, Messages, MessageFiles, Profiles
import json
from django.http import JsonResponse



def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_id):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_id))
    })

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('chat:index'))
        else:
            print(form.errors)
    return render(request, 'chat/login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(reverse('chat:log_in'))

def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('chat:log_in'))
        else:
            print(form.errors)
    return render(request, 'chat/signup.html', {'form': form, "errors": form.errors})

def upload_file(request):
    data = {"result": False}
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        msg_obj = Messages(
            sender = request.user.profile,
            message="",
            reciever_id = request.POST["chat_id"], # validate and authorize
            reciever_type = 1,
            message_type = 2
        )
        msg_obj.save()
        file_obj = MessageFiles(file=myfile, message=msg_obj)
        file_obj.save()

        data["result"] = True
        data["name"] = myfile.name
    return JsonResponse(data)

class ChatroomLists(ListView):
    model = Chatrooms
    queryset = Chatrooms.objects.all()
    context_object_name = 'chatroom_list'
    template_name = 'chat/chatroom/index.html'

class ChatroomCreate(CreateView):
    model = Chatrooms
    form_class = ChatroomForm
    template_name = 'chat/chatroom/create.html'

class ChatroomEdit(UpdateView):
    model = Chatrooms
    form_class = ChatroomForm
    template_name = 'chat/chatroom/edit.html'

class ChatroomDelete(DeleteView):
    model = Chatrooms
    template_name = 'chat/chatroom/delete.html'
    success_url = '/'