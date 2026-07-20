from django.contrib.auth import get_user_model
from django.test import TestCase

from users.serializers import UserSerializer

User = get_user_model()


class UserSerializerTests(TestCase):
    def test_create_user_hashes_password(self):
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "John",
            "last_name": "Doe",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        print(serializer.errors)
        user = serializer.save()

        self.assertNotEqual(user.password, "testpass123")
        self.assertTrue(user.check_password("testpass123"))

    def test_update_user_with_password(self):
        user = User.objects.create_user(email="test@example.com", password="oldpass123")
        serializer = UserSerializer(
            instance=user,
            data={"password": "newpass123"},
            partial=True,
        )
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user.check_password("newpass123"))

    def test_update_user_without_password_keeps_old_password(self):
        user = User.objects.create_user(email="test@example.com", password="oldpass123")
        old_password_hash = user.password

        serializer = UserSerializer(
            instance=user,
            data={"first_name": "Jane"},
            partial=True,
        )
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.password, old_password_hash)
        self.assertEqual(updated_user.first_name, "Jane")

    def test_is_staff_is_read_only(self):
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "is_staff": True,
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertFalse(user.is_staff)

    def test_password_not_in_representation(self):
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        serializer = UserSerializer(user)
        self.assertNotIn("password", serializer.data)
