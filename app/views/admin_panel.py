from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from ..models import Card
from ..admin_panel_forms import UserForm, CardForm


# User Views
def panel(request):
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
    users = User.objects.all()
    return render(request, "admin/user-list.html", {"users": users})


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    cards = Card.objects.filter(user=user)
    return render(request, "admin/user-detail.html", {"user": user, "cards": cards})


def user_new(request):  # originally same as user_edit
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
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect("user_list")


# Card Views
def card_edit(request, pk):
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
    card = get_object_or_404(Card, pk=pk)
    user_pk = card.user.pk
    if request.method == "POST":
        card.delete()
        return redirect("user_detail", pk=user_pk)
