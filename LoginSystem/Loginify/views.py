from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SignupForm, LoginForm
from .models import UserDetails
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

def hello_world(request):
    return HttpResponse("Hello, world!")

def sign_up(request):
    if request.method == "POST":
        try:
            form = SignupForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                form.instance.password = make_password(password)
                form.save()
                messages.success(request, "Successfully signed up! Please login.")
                return redirect("login")

                # return render(request, "Loginify/login.html", {"message": "You have successfully Signed Up. Please Login!", "form":form})
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    else:
        form = SignupForm()
    
    return render(request, "Loginify/signup.html", {"form":form})

def login(request):
    if request.method == "POST":
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                user = UserDetails.objects.filter(email=email).first()
                if user and check_password(password, user.password):
                    return render(request, "Loginify/success.html", {"username": user.username})
                else:
                    form.add_error(None, "Invalid email or password.")

        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
    else:
        form = LoginForm()
    
    return render(request, "Loginify/login.html", {"form":form})