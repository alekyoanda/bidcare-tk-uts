from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return JsonResponse({
            "status": True,
            "message": "Successfully Logged In!"
            # Insert any extra data if you want to pass data to Flutter
            }, status=200)
        else:
            return JsonResponse({
            "status": False,
            "message": "Failed to Login, Account Disabled."
            }, status=401)

    else:
        return JsonResponse({
        "status": False,
        "message": "Failed to Login, check your email/password."
        }, status=401)