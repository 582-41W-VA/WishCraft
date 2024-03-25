from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Card, Tag, Comment

# Create your views here.

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


# Retrieve all images from the database
# filter, search, and sort
def home(request):
    cards = Card.objects.all()
    tags = Tag.objects.all()
    selected_tags = request.GET.getlist("tags")
    selected_cards = cards

    if selected_tags:
        selected_cards = cards.filter(tag__id__in=selected_tags)

    search_query = request.GET.get("search")
    if search_query:
        selected_cards = cards.filter(title__icontains=search_query)

    sort_by = request.GET.get("sort")
    if sort_by == "latest":
        selected_cards = cards.order_by("date_created")
    elif sort_by == "oldest":
        selected_cards = cards.order_by("-date_created")
    elif sort_by == "likes":
        selected_cards = cards.order_by("-likes")
    elif sort_by == "alphabetical":
        selected_cards = cards.order_by("title")

    context = {
        "cards": cards,
        "tags": tags,
        "selected_tags": selected_tags,
        "sort_by": sort_by,
        "selected_cards": selected_cards,
    }
    return render(request, "app/home.html", context)


def card_detail(request, card_id):
    card_id = get_object_or_404(Card, pk=card_id)
    comments = Comment.objects.filter(card=card_id)
    tags = card_id.tag.all()
    context = {
        "card_id": card_id,
        "comments": comments,
        "tags": tags,
    }
    return render(request, "app/card-detail.html", context)


@login_required(login_url="/app/login/")
def add_comment(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment(
            content=content,
            user=request.user,
            card=card
        )
        comment.save()
        return redirect('card_detail', card_id=card_id)


def increment_likes(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    card.likes += 1
    card.save()
    return redirect("card_detail", card_id=card_id)


@login_required(login_url="/app/login/")
def create_card(request):    
    tags = Tag.objects.all()
    context = {"tags": tags}
    if request.method == "POST":
        new_tag_name = request.POST.get("new_tag", "")
        tag_ids = request.POST.getlist("tags")
        tags = Tag.objects.filter(id__in=tag_ids)
        
        if new_tag_name:
            new_tag, _ = Tag.objects.get_or_create(name=new_tag_name)
            tags = list(tags)
            tags.append(new_tag)

        new_card = Card(
            title=request.POST.get("title", ""),
            image=request.FILES.get("image", ""),
            user=request.user,
        )
        new_card.save()
        new_card.tag.set(tags)

        return redirect("user_list")
    else:
        return render(request, "app/create-card.html", context)


@login_required(login_url="/app/login/")
def user_list(request):
    user_lists = Card.objects.filter(user=request.user)
    tags = set()
    for card in user_lists:
        tags.update(card.tag.all())
    context = {"user_lists": user_lists,}
    return render(request, "app/user-list.html", context)
