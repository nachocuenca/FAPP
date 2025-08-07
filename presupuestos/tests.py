from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Cliente, Presupuesto


class PresupuestoCRUDTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.force_login(self.user)
        self.cliente = Cliente.objects.create(usuario=self.user, nombre="Cliente")

    def test_create_presupuesto(self):
        response = self.client.post(
            reverse("presupuesto_create"),
            {
                "cliente": self.cliente.pk,
                "fecha": "2024-01-01",
                "concepto": "Trabajo",
                "total": 100,
            },
        )
        self.assertRedirects(response, reverse("presupuesto_list"), fetch_redirect_response=False)
        self.assertEqual(Presupuesto.objects.count(), 1)

    def test_update_presupuesto(self):
        presupuesto = Presupuesto.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            concepto="Viejo",
            total=100,
        )
        response = self.client.post(
            reverse("presupuesto_update", args=[presupuesto.pk]),
            {
                "cliente": self.cliente.pk,
                "fecha": "2024-01-02",
                "concepto": "Nuevo",
                "total": 200,
            },
        )
        self.assertRedirects(response, reverse("presupuesto_list"), fetch_redirect_response=False)
        presupuesto.refresh_from_db()
        self.assertEqual(presupuesto.concepto, "Nuevo")
        self.assertEqual(presupuesto.total, 200)

    def test_delete_presupuesto(self):
        presupuesto = Presupuesto.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            concepto="Borrar",
            total=100,
        )
        response = self.client.post(
            reverse("presupuesto_delete", args=[presupuesto.pk])
        )
        self.assertRedirects(response, reverse("presupuesto_list"), fetch_redirect_response=False)
        self.assertEqual(Presupuesto.objects.count(), 0)

    def test_list_presupuestos(self):
        Presupuesto.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            concepto="Listado",
            total=100,
        )
        response = self.client.get(reverse("presupuesto_list"))
        self.assertContains(response, "Cliente")

    def test_export_csv(self):
        Presupuesto.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            concepto="CSV",
            total=100,
        )
        response = self.client.get(reverse("presupuesto_export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cliente", response.content)

    def test_export_pdf(self):
        Presupuesto.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            concepto="PDF",
            total=100,
        )
        response = self.client.get(reverse("presupuesto_export_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))


class PresupuestoPermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.cliente1 = Cliente.objects.create(usuario=self.user1, nombre="Cliente1")
        self.cliente2 = Cliente.objects.create(usuario=self.user2, nombre="Cliente2")
        self.presupuesto_ajeno = Presupuesto.objects.create(
            usuario=self.user2,
            cliente=self.cliente2,
            fecha="2024-01-01",
            concepto="Ajeno",
            total=100,
        )
        self.client.force_login(self.user1)

    def test_list_only_user_presupuestos(self):
        Presupuesto.objects.create(
            usuario=self.user1,
            cliente=self.cliente1,
            fecha="2024-01-02",
            concepto="Propio",
            total=50,
        )
        response = self.client.get(reverse("presupuesto_list"))
        self.assertContains(response, "Cliente1")
        self.assertNotContains(response, "Cliente2")

    def test_cannot_update_other_users_presupuesto(self):
        response = self.client.get(
            reverse("presupuesto_update", args=[self.presupuesto_ajeno.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_cannot_delete_other_users_presupuesto(self):
        response = self.client.post(
            reverse("presupuesto_delete", args=[self.presupuesto_ajeno.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_export_csv_excludes_other_users_presupuestos(self):
        Presupuesto.objects.create(
            usuario=self.user1,
            cliente=self.cliente1,
            fecha="2024-01-02",
            concepto="Propio",
            total=50,
        )
        response = self.client.get(reverse("presupuesto_export_csv"))
        content = response.content.decode()
        self.assertIn("Cliente1", content)
        self.assertNotIn("Cliente2", content)
