# from django.shortcuts import render, HttpResponse
# from django.utils.safestring import mark_safe
# import json
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from chat.models import GroupChat
# 
# # Create your views here.
# def index(request):
#     return render(request, 'echo/index.html')
# 
# def echo_image(request):
#     return render(request, 'echo/echo_image.html')
# 
# def join_chat(request, username):
#     return render(request, 'echo/join_chat.html', {'username_json': mark_safe(json.dumps(username))})
# 
# def new_message(request, username):
#     receiver = request.GET['Group_name']
#     text = "<Admin message>" + request.GET['text']
#     channel_layer = get_channel_layer()
#     # group_name = f"chat_{receiver}"
#     group_name = receiver
#     chat = GroupChat.objects.filter(title=receiver).first()
# 
#     async_to_sync(channel_layer.group_send)(
#         f"chat_{chat.unique_code}",
#         {
#             'type': 'chat_activity',
#             # 'message': json.dumps({'type': "join", 'username': "Admin"})
#             'message': json.dumps({'type': "msg", 'sender': "Admin", 'text':text}),
# 
#         }
#     )
# 
#     return HttpResponse('Message Sent in the group named: ')
