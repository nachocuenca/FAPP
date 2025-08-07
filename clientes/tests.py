from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Cliente


@override_settings(ROOT_URLCONF="test_urls")
class ClienteCRUDTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.force_login(self.user)

    def test_create_cliente(self):
        response = self.client.post(
            reverse("clientes:cliente_create"),
            {
                "nombre": "Cliente",
                "email": "cli@example.com",
                "telefono": "123",
                "direccion": "Calle",
            },
        )
        self.assertRedirects(response, reverse("clientes:cliente_list"), fetch_redirect_response=False)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_edit_cliente(self):
        cliente = Cliente.objects.create(usuario=self.user, nombre="Old")
        response = self.client.post(
            reverse("clientes:cliente_edit", args=[cliente.pk]),
            {
                "nombre": "New",
                "email": "",
                "telefono": "",
                "direccion": "",
            },
        )
        self.assertRedirects(response, reverse("clientes:cliente_list"), fetch_redirect_response=False)
        cliente.refresh_from_db()
        self.assertEqual(cliente.nombre, "New")

    def test_delete_cliente(self):
        cliente = Cliente.objects.create(usuario=self.user, nombre="Del")
        response = self.client.post(reverse("clientes:cliente_delete", args=[cliente.pk]))
        self.assertRedirects(response, reverse("clientes:cliente_list"), fetch_redirect_response=False)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_list_filters_by_user(self):
        User = get_user_model()
        Cliente.objects.create(usuario=self.user, nombre="Mine")
        other = User.objects.create_user(username="other", password="pass")
        Cliente.objects.create(usuario=other, nombre="Other")
        response = self.client.get(reverse("clientes:cliente_list"))
        self.assertContains(response, "Mine")
        self.assertNotContains(response, "Other")

    def test_export_csv(self):
        User = get_user_model()
        Cliente.objects.create(usuario=self.user, nombre="CSV")
        other = User.objects.create_user(username="other", password="pass")
        Cliente.objects.create(usuario=other, nombre="OTHER")
        response = self.client.get(reverse("clientes:cliente_export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CSV", response.content)
        self.assertNotIn(b"OTHER", response.content)

    def test_export_pdf(self):
        User = get_user_model()
        Cliente.objects.create(usuario=self.user, nombre="PDF")
        other = User.objects.create_user(username="other", password="pass")
        Cliente.objects.create(usuario=other, nombre="OTHER")
        response = self.client.get(reverse("clientes:cliente_export_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))

    def test_list_shows_only_user_clients(self):
        Cliente.objects.create(usuario=self.user, nombre="Mine")
        other_user = get_user_model().objects.create_user("other")
        Cliente.objects.create(usuario=other_user, nombre="Other")
        response = self.client.get(reverse("clientes:cliente_list"))
        self.assertContains(response, "Mine")
        self.assertNotContains(response, "Other")

    def test_cannot_edit_other_user_cliente(self):
        other_user = get_user_model().objects.create_user("other")
        other_cliente = Cliente.objects.create(usuario=other_user, nombre="Other")
        response = self.client.get(reverse("clientes:cliente_edit", args=[other_cliente.pk]))
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_other_user_cliente(self):
        other_user = get_user_model().objects.create_user("other")
        other_cliente = Cliente.objects.create(usuario=other_user, nombre="Other")
        response = self.client.post(reverse("clientes:cliente_delete", args=[other_cliente.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Cliente.objects.filter(pk=other_cliente.pk).exists())

    def test_export_csv_excludes_other_user_clients(self):
        Cliente.objects.create(usuario=self.user, nombre="Mine")
        other_user = get_user_model().objects.create_user("other")
        Cliente.objects.create(usuario=other_user, nombre="Other")
        response = self.client.get(reverse("clientes:cliente_export_csv"))
        self.assertIn(b"Mine", response.content)
        self.assertNotIn(b"Other", response.content)

    def test_export_pdf_excludes_other_user_clients(self):
        Cliente.objects.create(usuario=self.user, nombre="Mine")
        other_user = get_user_model().objects.create_user("other")
        Cliente.objects.create(usuario=other_user, nombre="Other")
        response = self.client.get(reverse("clientes:cliente_export_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Other", response.content)
