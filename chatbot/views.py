from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if request.user.is_authenticated:
            chat = Chat(user=request.user, message=message, created_at=timezone.now())
        else:
            chat = Chat(message=message, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message})
    else:
        chats = Chat.objects.order_by('created_at')
        return render(request, 'chatbot.html', {'chats': chats, 'current_user': request.user})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error = 'Username or password is wrong'
            return render(request, 'login.html', {'error_message': error})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error = 'Error creating account'
                return render(request, 'register.html', {'error_message': error})
        else:
            error = 'Passwords don\'t match'
            return render(request, 'register.html', {'error_message': error})

    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
