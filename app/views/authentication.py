from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


def create_user_if_not_exists(username, email, password, request):
    if User.objects.filter(username=username).exists():
        messages.error(request, "Username already exists")
        return False
    else:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        print("User created")
        return True


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "app/register.html")

        # Attempt to create the user
        if create_user_if_not_exists(username, email, password, request):
            return redirect("login")
        else:
            return redirect(register)
    else:
        return render(request, "app/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("User logged in")
            if request.user.is_superuser:
                return render(request, "app/admin.html")
            return redirect("user_list")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    else:
        return render(request, "app/login.html")


def logout(request):
    auth.logout(request)
    return redirect("home")