from django.urls import path
from .views import authentication, cards, admin_panel

urlpatterns = [
    path("", cards.home, name="home"),
    path("landing/", authentication.landing_page, name="landing_page"),
    path("register/", authentication.register, name="register"),
    path("login/", authentication.login, name="login"),
    path("logout/", authentication.logout, name="logout"),
    path("card/<int:card_id>/", cards.card_detail, name="card_detail"),
    path("card/<int:card_id>/add_comment/", cards.add_comment, name="add_comment"),
    path(
        "<int:card_id>/increment_likes/", cards.increment_likes, name="increment_likes"
    ),
    path(
        "<int:card_id>/decrement_likes/", cards.decrement_likes, name="decrement_likes"
    ),
    path("create_card/", cards.create_card, name="create_card"),
    path("your_wish_list/", cards.user_wishlist, name="user_wishlist"),
    path("edit_card/<int:card_id>/", cards.edit_card, name="edit_card"),
    path("delete_card/<int:card_id>/", cards.delete_card, name="delete_card"),
    # Admin User paths
    path("panel/", admin_panel.panel, name="admin_panel"),
    path("users/", admin_panel.user_list, name="user_list"),
    path("users/<int:pk>/", admin_panel.user_detail, name="user_detail"),
    path("users/new/", admin_panel.user_new, name="user_new"),
    path("users/<int:pk>/edit/", admin_panel.user_edit, name="user_edit"),
    path("users/<int:pk>/delete/", admin_panel.user_delete, name="user_delete"),
    # Admin Card paths
    path("cards/<int:pk>/edit/", admin_panel.card_edit, name="card_edit"),
    path("cards/<int:pk>/delete/", admin_panel.card_delete, name="card_delete"),
]
