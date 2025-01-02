from django.shortcuts import render, HttpResponse
import google.generativeai as genai
from .models import Chats
from datetime import datetime
import json, ast


# Custom evaluation with datetime handling
def eval_with_datetime(string):
    return 

# Create your views here.
def index(request):
    genai.configure(api_key="AIzaSyD8UlDn-Ks0l9HckW7Y7VqYSO4GvVU5500")
    model = genai.GenerativeModel("gemini-1.5-flash")
    context_data = {}
    chat_pk = 12
    chat_exists = True
    try:
        chat = Chats.objects.filter(pk=chat_pk).last()
    except Chats.DoesNotExist:
        chat_exists = False
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if chat_exists:
            chat_old_data = eval(chat.data) or []
            chat_old_data.append(
                {'text': user_message, 'from': 'user', 'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
            chat.data = chat_old_data
            chat.save(update_fields=["data"])
        else:
            payload = {
                "data": [{'text': user_message, 'from': 'user', 'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}]}
            chat = Chats.objects.create(name=user_message[:150], **payload)

        response = model.generate_content(user_message)
        chat_old_data = chat.data or []
        chat_old_data.append(
            {'text': response.text, 'from': 'bot', 'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')})
        chat.data = chat_old_data
        chat.save(update_fields=["data"])
    context_data = {"previous_chat": Chats.objects.all(), "current_chat": ast.literal_eval(chat.data)}
    return render(request, "index.html", context=context_data)
