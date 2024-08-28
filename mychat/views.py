from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')
 
def register(request):
    
    if request.method == 'POST': 
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not email or not username or not password:
            return JsonResponse({"error": "Missing fields"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return JsonResponse({"success": "User created successfully"}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        if (request.user.is_authenticated):
            return JsonResponse({'error': 'Already logged in'})
        else:
            user = authenticate(request, email=email, password=password)
            print (user)
            if not email or not password:
                return JsonResponse({"error": "Missing fields"}, status=400)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'success': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid credentials'})
    return JsonResponse({"error": "Invalid request method"}, status=405)

def friendlist(request):
    friends = User.objects.all().exclude(username=request.user.username)
    return render(request, 'friends.html', {'friends': friends})

@login_required
@csrf_exempt
def chat(request, id):
    current_user_id = request.user.id
    other_user_id = id
    room_name = generate_room_name(current_user_id, other_user_id)
    return render(request, 'chat.html', {
        'room_name': room_name
    })

def generate_room_name(user_id1, user_id2):
    # Ensure that the smaller ID is always first to keep room names consistent
    sorted_ids = sorted([user_id1, user_id2])
    return f"room-{sorted_ids[0]}-{sorted_ids[1]}"


@csrf_exempt
def send_message(request, id):
    print(request.POST)
    if request.method == 'POST':
        message = request.POST['message']
        user = request.user
        receiver = User.objects.get(id=id)

        # Create the Chat object with the message
        Chat.objects.create(sender=user, receiver=receiver, chat=message)

        return JsonResponse({'success': 'Message sent successfully'})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
