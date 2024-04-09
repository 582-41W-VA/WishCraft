"""
This file contains views for the admin panel in a Django application.

Functions:
- panel(request): Displays statistics about users and cards.
- user_list(request): Renders a list of all users.
- user_detail(request, pk): Shows details of a specific user and their associated cards.
- user_new(request): Handles creating a new user.
- user_edit(request, pk): Allows editing an existing user's information.
- user_delete(request, pk): Deletes a user.
- card_edit(request, pk): Edits a specific card's information.
- card_delete(request, pk): Deletes a card.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from ..models import Card
from ..admin_panel_forms import UserForm, CardForm


# User Views
def panel(request):
    """
    Renders the admin panel template with user and card statistics.

    This view displays various statistics about users and cards on the platform.
    It calculates the total number of users and cards, as well as the number of new
    users and cards created in the last day, week, and month.

    Returns:
        render(request, "admin/panel.html", context): The rendered admin panel
        template with the context data.
    """
    print("PING")
    now = timezone.now()
    one_day_ago = now - timedelta(days=1)
    one_week_ago = now - timedelta(weeks=1)
    one_month_ago = now - timedelta(days=30)

    total_users = User.objects.count()
    total_cards = Card.objects.count()

    new_users_last_day = User.objects.filter(date_joined__gte=one_day_ago).count()
    new_users_last_week = User.objects.filter(date_joined__gte=one_week_ago).count()
    new_users_last_month = User.objects.filter(date_joined__gte=one_month_ago).count()

    new_cards_last_day = Card.objects.filter(date_created__gte=one_day_ago).count()
    new_cards_last_week = Card.objects.filter(date_created__gte=one_week_ago).count()
    new_cards_last_month = Card.objects.filter(date_created__gte=one_month_ago).count()

    context = {
        "total_users": total_users,
        "total_cards": total_cards,
        "new_users_last_day": new_users_last_day,
        "new_users_last_week": new_users_last_week,
        "new_users_last_month": new_users_last_month,
        "new_cards_last_day": new_cards_last_day,
        "new_cards_last_week": new_cards_last_week,
        "new_cards_last_month": new_cards_last_month,
    }

    return render(request, "admin/panel.html", context)


def user_list(request):
    """
    Renders a list of all users on the platform.

    This view retrieves all users from the database and renders them in a
    template.

    Returns:
        render(request, "admin/user-list.html", {"users": users}): The
        rendered user list template with the list of users.
    """
    users = User.objects.all()
    return render(request, "admin/user-list.html", {"users": users})


def user_detail(request, pk):
    """
    Renders the detail page of a specific user.

    This view retrieves a user by their primary key (`pk`) and displays their
    information along with a list of cards associated with them.

    Args:
        request: The Django HTTP request object.
        pk: The primary key of the user to retrieve.

    Returns:
        render(request, "admin/user-detail.html", {"user": user, "cards": cards}):
        The rendered user detail template with user and card data.
    """
    user = get_object_or_404(User, pk=pk)
    cards = Card.objects.filter(user=user)
    return render(request, "admin/user-detail.html", {"user": user, "cards": cards})


def user_new(request):
    """
    Creates a new user on the platform.

    This view handles the creation of new users. It allows users to submit a
    form with user information, validates the data, saves the user to the
    database, and redirects to the user detail page.

    Returns:
        redirect("user_detail", pk=user.pk): A redirect to the newly created
        user's detail page after successful form submission.
        render(request, "admin/user-edit.html", {"form": form}): The rendered
        user edit template with the form object for creating a new user.
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            return redirect("user_detail", pk=user.pk)
    else:
        form = UserForm()
    return render(request, "admin/user-edit.html", {"form": form})


def user_edit(request, pk):
    """
    Edits an existing user on the platform.

    This view retrieves a user by their primary key (`pk`) and allows users
    to edit their information through a form. It validates the data, saves
    changes to the database, and redirects to the user detail page.

    Args:
        request: The Django HTTP request object.
        pk: The primary key of the user to edit.

    Returns:
        redirect("user_detail", pk=user.pk): A redirect to the edited user's
        detail page after successful form submission.
        render(request, "admin/user-edit.html", {"form": form}): The rendered
        user edit template with the populated form object for the user being edited.
    """
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            if password:
                user.set_password(password)
            user.save()
            return redirect("user_detail", pk=user.pk)
    else:
        form = UserForm(instance=user)
    return render(request, "admin/user-edit.html", {"form": form})


def user_delete(request, pk):
    """
    Deletes a user from the platform.

    This view retrieves a user by their primary key (`pk`) and deletes them
    from the database. It then redirects to the user list page.

    Args:
        request: The Django HTTP request object.
        pk: The primary key of the user to delete.

    Returns:
        redirect("user_list"): A redirect to the user list page after
        successful deletion.
    """
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect("user_list")


# Card Views
def card_edit(request, pk):
    """
    Edits an existing card on the platform.

    This view retrieves a card by its primary key (`pk`) and allows users
    to edit its information through a form. It validates the data, saves
    changes to the database, and redirects to the user detail page of the
    card's owner.

    Args:
        request: The Django HTTP request object.
        pk: The primary key of the card to edit.

    Returns:
        redirect("user_detail", pk=card.user.pk): A redirect to the card
        owner's detail page after successful form submission.
        render(request, "admin/card-edit.html", {"form": form}): The rendered
        card edit template with the populated form object for the card being edited.
    """
    card = get_object_or_404(Card, pk=pk)
    if request.method == "POST":
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save()
            return redirect("user_detail", pk=card.user.pk)
    else:
        form = CardForm(instance=card)
    return render(request, "admin/card-edit.html", {"form": form})


def card_delete(request, pk):
    """
    Deletes a card from the platform.

    This view retrieves a card by its primary key (`pk`) and deletes it
    from the database. It stores the card owner's primary key (`user_pk`)
    before deletion and redirects to the user detail page of the card's owner
    afterwards.

    Args:
        request: The Django HTTP request object.
        pk: The primary key of the card to delete.

    Returns:
        redirect("user_detail", pk=user_pk): A redirect to the card owner's
        detail page after successful deletion.
    """
    card = get_object_or_404(Card, pk=pk)
    user_pk = card.user.pk
    if request.method == "POST":
        card.delete()
        return redirect("user_detail", pk=user_pk)
