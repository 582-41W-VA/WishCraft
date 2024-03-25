from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("card/<int:card_id>/", views.card_detail, name="card_detail"),
    path("card/<int:card_id>/add_comment/", views.add_comment, name="add_comment"),
    path("<int:card_id>/increment_likes/", views.increment_likes, name="increment_likes"),
    path("create_card/", views.create_card, name="create_card"),
    path("your_wish_list/", views.user_list, name="user_list")
]