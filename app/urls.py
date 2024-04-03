from django.urls import path
from .views import authentication, cards

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
    path("create_card/", cards.create_card, name="create_card"),
    path("your_wish_list/", cards.user_list, name="user_list"),
    path("edit_card/<int:card_id>/", cards.edit_card, name="edit_card"),
    path("delete_card/<int:card_id>/", cards.delete_card, name="delete_card"),
]
