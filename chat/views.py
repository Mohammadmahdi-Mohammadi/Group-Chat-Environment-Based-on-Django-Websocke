from chat.forms import UserRegisterForm
from chat.models import Member, GroupChat

from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout

import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chat:index')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'chat/register.html', {'form': form})


@login_required
def index(request):
    current_user = request.user
    all_group = GroupChat.objects.all()
    return render(request, 'chat/index.html', {'members': current_user.member_set.all(), 'all_Groups': all_group})


@login_required
def create_chat(request):
    current_user = request.user
    title = request.POST['group_name']
    chat = GroupChat.objects.create(creator_id=current_user.id, title=title)
    Member.objects.create(chat_id=chat.id, user_id=current_user.id)
    return redirect(reverse('chat:chat', args=[chat.unique_code]))


@login_required
def chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(unique_code=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, 'chat/404.html')
    if request.method == "GET":
        if Member.objects.filter(chat_id=chat.id, user_id=current_user.id).count() == 0:
            return render(request, 'chat/join_chat.html', {'chatObject': chat})
        return render(request, 'chat/chat.html', {'chatObject': chat, 'chat_id_json': mark_safe(json.dumps(chat.unique_code))})
    elif request.method == "POST":
        try:
            check_value = Member.objects.get(chat_id=chat.id, user_id=current_user.id)
        except:
            check_value = None
        print("Check value: ", check_value)

        if check_value is None:
            Member.objects.create(chat_id=chat.id, user_id=current_user.id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{chat.unique_code}",
                {
                    'type': 'chat_activity',
                    'message': json.dumps({'type': "join", 'username': current_user.username})
                }
            )
            return render(request, 'chat/chat.html', {'chatObject': chat, 'chat_id_json': mark_safe(json.dumps(chat.unique_code))})
        return redirect('chat:index')


@login_required
def leave_chat(request, chat_id):
    current_user = request.user
    try:
        chat = GroupChat.objects.get(unique_code=chat_id)
    except GroupChat.DoesNotExist:
        return render(request, 'chat/404.html')
    if chat.creator_id == current_user.id:
        chat.delete()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "delete"})
            }
        )
    else:
        Member.objects.filter(chat_id=chat.id, user_id=current_user.id).delete()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.unique_code}",
            {
                'type': 'chat_activity',
                'message': json.dumps({'type': "leave", 'username': current_user.username})
            }
        )
    return redirect('chat:index')


def new_message(request):
    receiver = request.GET['Group_name']
    text = request.GET['text']
    channel_layer = get_channel_layer()
    chat = GroupChat.objects.filter(title=receiver).first()
    async_to_sync(channel_layer.group_send)(
        f"chat_{chat.unique_code}",
        {
            'type': 'chat_activity',
            'message': json.dumps({'type': "msg", 'sender': "Admin", 'text':text}),
        }
    )
    return HttpResponse(f'Message: " {text} " Sent in the group named: "{receiver}" from Administrator', status=200)