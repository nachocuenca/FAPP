from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Cliente


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



@override_settings(ROOT_URLCONF="test_urls")
class ClienteLoginRequiredTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user2", password="pass")
        self.cliente = Cliente.objects.create(usuario=self.user, nombre="Cli")

    def assert_login_redirect(self, url, method="get"):
        client_method = getattr(self.client, method)
        response = client_method(url)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={url}",
            fetch_redirect_response=False,
        )

    def test_login_required_views(self):
        urls = [
            reverse("clientes:cliente_create"),
            reverse("clientes:cliente_edit", args=[self.cliente.pk]),
            reverse("clientes:cliente_delete", args=[self.cliente.pk]),
            reverse("clientes:cliente_export_csv"),
            reverse("clientes:cliente_export_pdf"),
            reverse("clientes:cliente_print"),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assert_login_redirect(url)

