"""
This module contains views for the home page, card detail page, adding comments, incrementing likes, creating cards, and user list page.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Card, Tag, Comment, Like


def get_filtered_cards(request):
    """
    Helper function to filter cards based on selected tags, search query, and sort order.
    Return:
    - cards: QuerySet of filtered cards.
    """
    cards = Card.objects.all().order_by("-date_created")
    selected_tags = request.GET.getlist("tags")
    search_query = request.GET.get("search")
    sort_by = request.GET.get("sort")

    if selected_tags:
        cards = cards.filter(tag__id__in=selected_tags)

    if search_query:
        cards = cards.filter(title__icontains=search_query)

    if sort_by == "latest":
        cards = cards.order_by("-date_created")
    elif sort_by == "oldest":
        cards = cards.order_by("date_created")
    elif sort_by == "likes":
        cards = cards.order_by("-likes")
    elif sort_by == "alphabetical":
        cards = cards.order_by("title")
    return cards


def home(request):
    """
    View for displaying the home page.
    Displays all cards, tags, selected cards, selected tags, and sort order.

    Args:
    - request: HttpRequest object.

    Return:
    - HttpResponse object with the rendered home.html template.
    """
    tags = Tag.objects.all()
    selected_cards = get_filtered_cards(request)
    selected_tags = request.GET.getlist("tags")
    sort_by = request.GET.get("sort")

    context = {
        "selected_cards": selected_cards,
        "tags": tags,
        "selected_tags": selected_tags,
        "sort_by": sort_by,
    }
    return render(request, "app/home.html", context)


def card_detail(request, card_id):
    """
    View for displaying the details of a card.
    Displays the specified card, comments, and tags.

    Args:
    - request: HttpRequest object.
    - card_id: ID of the card to display.

    Return:
    - HttpResponse object with the rendered card-detail.html template.
    """
    card = get_object_or_404(Card, pk=card_id)
    comments = Comment.objects.filter(card=card).order_by("-id")
    tags = card.tag.all()
    user = request.user
    has_liked = Like.objects.filter(user=user, card=card).exists()
    context = {
        "card": card,
        "comments": comments,
        "tags": tags,
        "has_liked": has_liked,
        "card_id": card_id,
    }
    return render(request, "app/card-detail.html", context)


@login_required(login_url="/app/login/")
def add_comment(request, card_id):
    """
    View for adding a comment to a card.
    Adds a comment to the specified card.

    Args:
    - request: HttpRequest object.
    - card_id: ID of the card to add a comment to.

    Return:
    - HttpResponseRedirect object that redirects to the card_detail view for the specified card.
    """
    card = get_object_or_404(Card, pk=card_id)
    if request.method == "POST":
        content = request.POST.get("content")
        comment = Comment(content=content, user=request.user, card=card)
        comment.save()
        return redirect("card_detail", card_id=card_id)


def increment_likes(request, card_id):
    """
    View for incrementing the likes of a card.
    Increments the likes of the specified card.

    Args:
    - request: HttpRequest object.
    - card_id: ID of the card to increment likes for.

    Return:
    - HttpResponseRedirect object that redirects to the card_detail view for the specified card.
    """
    card = get_object_or_404(Card, pk=card_id)
    user = request.user
    has_liked = Like.objects.filter(user=user, card=card).exists()

    if not has_liked:
        card.likes += 1
        card.save()
        Like.objects.create(user=user, card=card)

    return redirect("card_detail", card_id=card_id)


def decrement_likes(request, card_id):
    """
    View for decrementing the likes of a card.
    Decrements the likes of the specified card.

    Args:
    - request: HttpRequest object.
    - card_id: ID of the card to decrement likes for.

    Return:
    - HttpResponseRedirect object that redirects to the card_detail view for the specified card.
    """
    card = Card.objects.get(pk=card_id)
    user = request.user

    has_liked = Like.objects.filter(user=user, card=card).exists()

    if not has_liked:
        return redirect("card_detail", card_id=card_id)

    card.likes -= 1
    card.save()
    Like.objects.filter(user=user, card=card).delete()

    return redirect("card_detail", card_id=card_id)


@login_required(login_url="/app/login/")
def create_card(request):
    """
    View for creating a card.
    Creates a new card with the specified title, image, and tags.

    Args:
    - request: HttpRequest object.

    Return:
    - HttpResponseRedirect object that redirects to the user_wishlist view.
    """
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

        return redirect("user_wishlist")
    else:
        return render(request, "app/create-card.html", context)


@login_required(login_url="/app/login/")
def user_wishlist(request):
    """
    View for displaying the user's wish list.
    Displays all cards created by the user.

    Args:
    - request: HttpRequest object.

    Return:
    - HttpResponse object with the rendered user-wishlist.html template.
    """
    user_wishlists = Card.objects.filter(user=request.user).order_by("-date_created")
    tags = set()
    for card in user_wishlists:
        tags.update(card.tag.all())
    context = {
        "user_wishlists": user_wishlists,
    }
    return render(request, "app/user-wishlist.html", context)


def edit_card(request, card_id):
    """
    View for editing a card.
    Edits the specified card with the new title, image, and tags.

    Args:
    - request: HttpRequest object.
    - card_id: ID of the card to edit.

    Return:
    - HttpResponseRedirect object that redirects to the user_wishlist view.
    """
    card = get_object_or_404(Card, pk=card_id)
    tags = Tag.objects.all()
    context = {"card": card, "tags": tags}
    if request.method == "POST":
        new_tag_name = request.POST.get("new_tag", "")
        tag_ids = request.POST.getlist("tags")
        tags = Tag.objects.filter(id__in=tag_ids)

        if new_tag_name:
            new_tag, _ = Tag.objects.get_or_create(name=new_tag_name)
            tags = list(tags)
            tags.append(new_tag)

        card.title = request.POST.get("title", "")
        image_file = request.FILES.get("image")
        if image_file:
            card.image = image_file
        card.save()
        card.tag.set(tags)

        return redirect("user_wishlist")
    else:
        return render(request, "app/edit-card.html", context)


def delete_card(request, card_id):
    """
    View for deleting a card.
    Deletes the specified card.

    Args:
    - request: HttpRequest object.
    - card_id: ID of the card to delete.

    Return:
    - HttpResponseRedirect object that redirects to the user_wishlist view.
    """
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return redirect("user_wishlist")
