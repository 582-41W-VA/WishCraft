from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

"""
This module provides functions for user authentication and registration within the application.
It includes functions for user creation, registration, login, logout, and rendering the landing page.
"""


def create_user(username, email, password, request):
    """
    Create a new user if the username doesn't already exist.

    Args:
    - username (str): The username for the new user.
    - email (str): The email for the new user.
    - password (str): The password for the new user.
    - request (HttpRequest): The request object to use for error messages.

    Returns:
    - bool: True if the user was created successfully, False otherwise.
    """
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
    """
    Handle user registration.

    If the request method is POST, attempts to register the user with the provided information.
    Redirects to the login page if registration is successful, or back to the registration page if it fails.
    If the request method is GET, renders the registration page.

    Args:
    - request (HttpRequest): The request object.

    Returns:
    - HttpResponse: Rendered HTML page.
    """
    if request.method == "POST":
        # Extract form data
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # Context for retaining form data
        context = {
            "username": username,
            "email": email,
            "password": "",  # It's a good practice not to send back the password
            "confirm_password": "",  # Same for confirm password
        }

        # Check if any field is empty
        if not (username and email and password and confirm_password):
            messages.error(request, "Please fill in all fields")
            return render(request, "app/register.html", context)

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "app/register.html", context)

        # Attempt to create the user
        if create_user(username, email, password, request):
            return redirect("login")
        else:
            messages.error(request, "Failed to create user")
            return render(request, "app/register.html", context)
    else:
        return render(request, "app/register.html")


def login(request):
    """
    Handle user login.

    If the request method is POST, attempts to authenticate the user.
    Redirects to the appropriate page based on user role.
    If the request method is GET, renders the login page.

    Args:
    - request (HttpRequest): The request object.

    Returns:
    - HttpResponse: Rendered HTML page.
    """
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        # Context for retaining username
        context = {"username": username}

        # Check if any field is empty
        if not (username and password):
            messages.error(request, "Please fill in all fields")
            return render(request, "app/login.html", context)

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("User logged in")
            if request.user.is_superuser or request.user.is_staff:
                return redirect("admin_panel")
            return redirect("user_wishlist")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "app/login.html", context)
    else:
        return render(request, "app/login.html")


def logout(request):
    """
    Log out the current user.

    Args:
    - request (HttpRequest): The request object.

    Returns:
    - HttpResponseRedirect: Redirects to the landing page.
    """
    auth.logout(request)
    return redirect("landing_page")


def landing_page(request):
    """
    Render the landing page.

    Redirects to the user list page if the user is already authenticated.

    Args:
    - request (HttpRequest): The request object.

    Returns:
    - HttpResponse: Rendered HTML page.
    """
    if request.user.is_authenticated:
        return redirect("user_wishlist")
    return render(request, "app/index.html")
