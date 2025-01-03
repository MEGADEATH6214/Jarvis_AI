from django.shortcuts import render, HttpResponse
import google.generativeai as genai
from .models import Chats
from datetime import datetime
import json, ast
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def set_chat_id(request):
    if request.method == "POST":
        data = json.loads(request.body)
        chat_id = data.get('chat_id')  # Get the chat ID

        if chat_id:
            # Store or update the chat_id as needed, for example, in the session
            request.session['chat_id'] = chat_id
            return JsonResponse({'status': 'success', 'chat_id': chat_id})
        return JsonResponse({'status': 'failure', 'message': 'No chat ID provided'})
    return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})

# Create your views here.
def index(request):
    genai.configure(api_key="AIzaSyD8UlDn-Ks0l9HckW7Y7VqYSO4GvVU5500")
    model = genai.GenerativeModel("gemini-1.5-flash")
    context_data = {}
    chat_pk = request.session.get('chat_id')
    print("chat_pk", chat_pk)
    chat = Chats.objects.filter(pk=chat_pk).last()
    if not chat:
        payload = {
            "data": [{'text': "Ask me anything you want...", 'from': 'bot', 'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}]}
        chat = Chats.objects.create(name="Blank Question", **payload)
        print("i am here", chat)
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get('message', '')

        chat_old_data = eval(chat.data) or []
        chat_old_data.append(
            {'text': user_message, 'from': 'user', 'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
        chat.data = chat_old_data
        if chat.name == "Blank Question":
            chat.name = user_message[:150]
        chat.save(update_fields=["data", "name"])

        response = model.generate_content(user_message)
        chat_old_data = chat.data or []
        chat_old_data.append(
            {'text': response.text, 'from': 'bot', 'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
        chat.data = chat_old_data
        chat.save(update_fields=["data"])
    print(chat, chat.data)
    context_data = {"previous_chat": Chats.objects.all(), "current_chat": ast.literal_eval(str(chat.data))}
    return render(request, "index.html", context=context_data)
