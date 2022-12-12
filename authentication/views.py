from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from general_user.models import GeneralUser, RekeningBank

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Redirect to a success page.
            general_user = GeneralUser.objects.get(user=user)
            return JsonResponse({
            "status": True,
            "message": "Successfully Logged In!",
            # Insert any extra data if you want to pass data to Flutter
            "user_username": user.username,
            "user_id": user.id,
            "user_username": user.username,
            "is_user_resipien": general_user.is_resipien,
            "nama_rekening_bank_user": general_user.akun_bank.nama_bank,
            "no_rekening_bank_user": general_user.akun_bank.no_rekening,
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