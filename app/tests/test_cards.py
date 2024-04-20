"""
This module contains tests for the views in the cards module.
"""

from django.test import TestCase, Client
from django.urls import reverse
from app.models import Card, Tag, Comment, Like
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from app.views.cards import get_filtered_cards


class TestCards(TestCase):
    """
    Test cases for the views in the cards module.
    """

    def setUp(self):
        """
        Set up the test environment by creating a test user, tags, card, and comment.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.tag1 = Tag.objects.create(name="Tag 1")
        self.tag2 = Tag.objects.create(name="Tag 2")
        with open(
            "media/images/UtensilCrocks_HERO_120621_24372_V1_final.webp", "rb"
        ) as f:
            image_data = f.read()
        image_file = BytesIO(image_data)
        image_file.name = "test_image.webp"
        self.card = Card.objects.create(
            title="Test Card", user=self.user, image=File(image_file)
        )
        self.card.tag.add(self.tag1, self.tag2)
        self.comment = Comment.objects.create(
            content="Test Comment", user=self.user, card=self.card
        )

    def test_get_filtered_cards(self):
        """
        Test the get_filtered_cards function with a specific set of filters.
        Checks if the function correctly filters cards based on tags, search query, and sorting order.
        """
        response = self.client.get(
            "", {"tags": [self.tag1.id], "search": "Card", "sort": "latest"}
        )
        filtered_cards = get_filtered_cards(response.wsgi_request)
        self.assertEqual(filtered_cards.count(), 1)
        self.assertEqual(filtered_cards.first(), self.card)

    def test_home_view(self):
        """
        Test the home view.
        Checks if the home page is rendered correctly and if the necessary context variables are present.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/home.html")
        self.assertIn("selected_cards", response.context)
        self.assertIn("tags", response.context)
        self.assertIn("selected_tags", response.context)
        self.assertIn("sort_by", response.context)

    def test_card_detail_view(self):
        """
        Test the card detail view.
        Checks if the card detail page is rendered correctly and if the necessary context variables are present.
        """
        Like.objects.create(user=self.user, card=self.card)
        response = self.client.get(reverse("card_detail", args=[self.card.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/card-detail.html")
        self.assertIn("card", response.context)
        self.assertIn("comments", response.context)
        self.assertIn("tags", response.context)
        self.assertIn("has_liked", response.context)
        self.assertEqual(response.context["card"], self.card)
        self.assertIn(self.comment, response.context["comments"])
        self.assertIn(self.tag1, response.context["tags"])
        self.assertIn(self.tag2, response.context["tags"])
        self.assertTrue(response.context["has_liked"])

    def test_add_comment_view(self):
        """
        Test the add comment view.
        Checks if a new comment can be successfully added to a card.
        """
        initial_comment_count = Comment.objects.count()
        response = self.client.post(
            reverse("add_comment", args=[self.card.id]), {"content": "New Comment"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), initial_comment_count + 1)
        new_comment = Comment.objects.last()
        self.assertEqual(new_comment.content, "New Comment")
        self.assertEqual(new_comment.user, self.user)
        self.assertEqual(new_comment.card, self.card)

    def test_increment_likes_view(self):
        """
        Test the increment likes view.
        Checks if the likes of a card are incremented by 1 when the increment_likes view is accessed.
        """
        initial_likes = self.card.likes
        response = self.client.get(reverse("increment_likes", args=[self.card.id]))
        updated_card = Card.objects.get(id=self.card.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_card.likes, initial_likes + 1)

    def test_decrement_likes_view(self):
        """
        Test the decrement likes view.
        Checks if the likes of a card are decremented by 1 when the decrement_likes view is accessed.
        """
        Like.objects.create(user=self.user, card=self.card)
        initial_likes = self.card.likes
        response = self.client.get(reverse("decrement_likes", args=[self.card.id]))
        updated_card = Card.objects.get(id=self.card.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_card.likes, initial_likes - 1)

    def test_create_card_view(self):
        """
        Test the create card view.
        Checks if a new card is created successfully when the create_card view is accessed with valid data.
        """
        initial_card_count = Card.objects.count()

        with open(
            "media/images/custom-nike-dunk-high-by-you-shoes_aX1ryzF.png", "rb"
        ) as f:
            image_data = f.read()
        image_file = BytesIO(image_data)
        image_file.name = "new_image.png"

        response = self.client.post(
            reverse("create_card"),
            {
                "title": "New Card",
                "image": "new_image.png",
                "tags": [self.tag1.id, self.tag2.id],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), initial_card_count + 1)
        new_card = Card.objects.last()
        self.assertEqual(new_card.title, "New Card")
        self.assertEqual(new_card.user, self.user)
        self.assertIn(self.tag1, new_card.tag.all())
        self.assertIn(self.tag2, new_card.tag.all())

    def test_user_wishlist_view(self):
        """
        Test the user wishlist view.
        Checks if the user's wishlist is displayed correctly with the expected cards when the user_wishlist view is accessed.
        """
        response = self.client.get(reverse("user_wishlist"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/user-wishlist.html")
        self.assertIn("user_wishlists", response.context)
        self.assertIn("searched_cards", response.context)
        self.assertEqual(list(response.context["user_wishlists"]), [self.card])
        self.assertEqual(list(response.context["searched_cards"]), [self.card])

    def test_edit_card_view(self):
        """
        Test the edit card view.
        Checks if the card is successfully updated with the new title, image and tag when the edit_card view is accessed.
        """
        with open(
            "media/images/custom-nike-dunk-high-by-you-shoes_aX1ryzF.png", "rb"
        ) as f:
            image_data = f.read()
        image_file = BytesIO(image_data)
        image_file.name = "new_image.png"

        response = self.client.post(
            reverse("edit_card", args=[self.card.id]),
            {
                "title": "Updated Title",
                "image": "new_image.png",
                "tags": [self.tag1.id],
            },
        )
        updated_card = Card.objects.get(id=self.card.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_card.title, "Updated Title")
        self.assertIn(self.tag1, updated_card.tag.all())
        self.assertNotIn(self.tag2, updated_card.tag.all())

    def test_delete_card_view(self):
        """
        Test the delete card view.
        Checks if the card is successfully deleted when the delete_card view is accessed.
        """
        initial_card_count = Card.objects.count()
        response = self.client.post(reverse("delete_card", args=[self.card.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), initial_card_count - 1)
        with self.assertRaises(Card.DoesNotExist):
            Card.objects.get(id=self.card.id)
