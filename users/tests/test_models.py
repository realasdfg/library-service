from unittest import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class UserTests(TestCase):
    def tearDown(self):
        User.objects.all().delete()

    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpass123"
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
        ]
        for email, expected in sample_emails:
            user = User.objects.create_user(email=email, password="pass123")
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="pass123")

        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="pass123")

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com", password="pass123"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_with_is_staff_false_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com",
                password="pass123",
                is_staff=False,
            )

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com",
                password="pass123",
                is_superuser=False,
            )

    def test_create_user_default_flags(self):
        user = User.objects.create_user(email="user@example.com", password="pass123")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
