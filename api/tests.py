from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Company, KBEntry, QueryLog


class TeamBoardAPITests(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client_test",
            email="client@example.com",
            password="TestPass123!"
        )
        self.client_company = self.client_user.company
        self.client_company.company_name = "Client Test Company"
        self.client_company.role = Company.Role.CLIENT
        self.client_company.save()

        self.admin_user = User.objects.create_user(
            username="admin_test",
            email="admin@example.com",
            password="AdminPass123!"
        )
        self.admin_company = self.admin_user.company
        self.admin_company.company_name = "Admin Test Company"
        self.admin_company.role = Company.Role.ADMIN
        self.admin_company.save()

        self.entry = KBEntry.objects.create(
            question="What is Django?",
            answer="Django is a Python web framework.",
            category=KBEntry.Category.FRAMEWORK
        )

        self.knowledge_url = reverse("knowledge-list")
        self.query_url = reverse("kb-query")
        self.usage_url = reverse("usage-summary")
        self.register_url = reverse("register")

    def authenticate(self, user):
        token = str(RefreshToken.for_user(user).access_token)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_user_registration(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "new_user",
                "email": "new@example.com",
                "password": "NewPass123!",
                "company_name": "New Test Company"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="new_user").exists())
        self.assertTrue(
            Company.objects.filter(
                user__username="new_user",
                company_name="New Test Company"
            ).exists()
        )

    def test_knowledge_list_requires_authentication(self):
        response = self.client.get(self.knowledge_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_knowledge(self):
        self.authenticate(self.client_user)

        response = self.client.get(self.knowledge_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_authenticated_user_can_create_knowledge(self):
        self.authenticate(self.client_user)

        response = self.client.post(
            self.knowledge_url,
            {
                "question": "What is REST?",
                "answer": "REST is an architectural style.",
                "category": "api"
            },
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            KBEntry.objects.filter(question="What is REST?").exists()
        )

    def test_authenticated_user_can_retrieve_knowledge(self):
        self.authenticate(self.client_user)

        response = self.client.get(
            reverse("knowledge-detail", args=[self.entry.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["question"], "What is Django?")

    def test_authenticated_user_can_update_knowledge(self):
        self.authenticate(self.client_user)

        response = self.client.patch(
            reverse("knowledge-detail", args=[self.entry.id]),
            {"answer": "Django is a high-level Python web framework."},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.entry.refresh_from_db()
        self.assertEqual(
            self.entry.answer,
            "Django is a high-level Python web framework."
        )

    def test_authenticated_user_can_delete_knowledge(self):
        self.authenticate(self.client_user)

        response = self.client.delete(
            reverse("knowledge-detail", args=[self.entry.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(KBEntry.objects.filter(id=self.entry.id).exists())

    def test_search_requires_authentication(self):
        response = self.client.post(
            self.query_url,
            {"search": "Django"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_returns_results_and_logs_query(self):
        self.authenticate(self.client_user)

        response = self.client.post(
            self.query_url,
            {"search": "Django"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["search"], "Django")
        self.assertEqual(
            QueryLog.objects.filter(
                company=self.client_company,
                search_term="Django",
                results_count=1
            ).count(),
            1
        )

    def test_empty_search_returns_bad_request(self):
        self.authenticate(self.client_user)

        response = self.client.post(
            self.query_url,
            {"search": "   "},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["error"],
            "Search term is required."
        )

    def test_admin_can_view_usage_summary(self):
        self.authenticate(self.admin_user)

        response = self.client.get(self.usage_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_queries", response.data)
        self.assertIn("total_results", response.data)
        self.assertIn("company_usage", response.data)

    def test_client_cannot_view_usage_summary(self):
        self.authenticate(self.client_user)

        response = self.client.get(self.usage_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

# Create your tests here.
