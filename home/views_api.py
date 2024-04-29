from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .helpers import *
from django.contrib.auth import authenticate, login


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = request.POST

            if data.get('loginUsername') is None:
                raise Exception('Username is required')
            if data.get('loginPassword') is None:
                raise Exception('Password is required')

            check_user = User.objects.filter(username=data.get('loginUsername')).first()

            if check_user is None:
                raise Exception('Invalid username, user not found')

            if not Profile.objects.filter(user=check_user).first().is_verified:
                raise Exception('Your profile is not verified')

            user_obj = authenticate(username=data.get('loginUsername'), password=data.get('loginPassword'))
            if user_obj:
                login(request, user_obj)
                # Redirect to the root page after successful login
                return redirect('/')
            else:
                raise Exception('Invalid password')

        except Exception as e:
            return JsonResponse({'status': 500, 'message': str(e)})

    # If the request method is not POST, render the login HTML template
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username:
                raise Exception('Username is required')
            if not password:
                raise Exception('Password is required')

            check_user = User.objects.filter(username=username).first()
            if check_user:
                raise Exception('Username already taken')

            user_obj = User.objects.create_user(username=username, email=username, password=password)
            token = generate_random_string(20)
            Profile.objects.create(user=user_obj, token=token, is_verified=True)

            # Set success message
            messages.success(request, 'Registration successful. Please log in.')

            return redirect('login')  # Redirect to login page after registration
        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'register.html')

    return render(request, 'register.html')
