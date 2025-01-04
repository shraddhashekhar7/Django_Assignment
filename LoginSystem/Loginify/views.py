from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SignupForm, LoginForm
from .models import UserDetails
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import json
from .serializer import UserSerializer
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def all_data(request):
    if request.method == "GET":
        try:
            alldata = UserDetails.objects.all()  
            serialized_data = UserSerializer(alldata, many=True)  
            return JsonResponse(serialized_data.data, safe=False)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
        
    if request.method == "POST":
        try:
            data = json.loads(request.body) 
            serialized_data = UserSerializer(data = data) 
            if serialized_data.is_valid():
                serialized_data.save()
                return JsonResponse({"message":"Data saved successfully!"},status=201)
            else:
                return JsonResponse(serialized_data.errors, status=400)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
        
@csrf_exempt        
def single_user_data(request, email):
    if request.method == "GET":
        try:
            userdata = UserDetails.objects.get(email=email) 
            serialized_data = UserSerializer(userdata) 
            return JsonResponse({
                "data":serialized_data.data}, status=200)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
        
    if request.method == "PUT":
        try:
            user_data = json.loads(request.body)
            user = UserDetails.objects.get(email=email)
            serialized_data = UserSerializer(user, data=user_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return JsonResponse({"message":"Data updated successfully"}, status=200)
            else:
                return JsonResponse(serialized_data.errors, status=400)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
    
    if request.method == "DELETE":
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({"message":"User deleted successfully"},status=200)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
        
    if request.method == "PATCH":
        try:
            user_data = json.loads(request.body)
            user = UserDetails.objects.get(email=email)
            serialized_data = UserSerializer(user, data=user_data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return JsonResponse({"message":"Data patched successfully"}, status=200)
            else:
                return JsonResponse(serialized_data.errors, status=400)
        except UserDetails.DoesNotExist:
            return JsonResponse({"error":"User not found"},status=404)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
