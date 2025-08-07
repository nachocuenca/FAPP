from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from types import SimpleNamespace

from .models import Cliente, Pedido, Factura, Actuacion
from .utils import export_csv


class FacturaTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.cliente = Cliente.objects.create(usuario=self.user, nombre="Cliente")
        self.pedido = Pedido.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            descripcion="Pedido de prueba",
            total=100,
        )

    def test_total_calculation(self):
        factura = Factura.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            pedido=self.pedido,
            fecha="2024-01-01",
            numero="F001",
            base_imponible=100,
            iva=21,
            irpf=0,
        )
        self.assertEqual(factura.total, 121)

    def test_export_csv(self):
        Factura.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            pedido=self.pedido,
            fecha="2024-01-01",
            numero="F001",
            base_imponible=100,
            iva=21,
            irpf=0,
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("factura_export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"F001", response.content)


class PedidoCRUDTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.force_login(self.user)
        self.cliente = Cliente.objects.create(usuario=self.user, nombre="Cliente")

    def test_create_pedido(self):
        response = self.client.post(
            reverse("pedido_nuevo"),
            {
                "cliente": self.cliente.pk,
                "presupuesto": "",
                "fecha": "2024-01-01",
                "descripcion": "Pedido nuevo",
                "total": 100,
            },
        )
        self.assertRedirects(response, reverse("pedidos_list"), fetch_redirect_response=False)
        self.assertEqual(Pedido.objects.count(), 1)

    def test_edit_pedido(self):
        pedido = Pedido.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            descripcion="Pedido inicial",
            total=100,
        )
        response = self.client.post(
            reverse("pedido_editar", args=[pedido.pk]),
            {
                "cliente": self.cliente.pk,
                "presupuesto": "",
                "fecha": "2024-02-01",
                "descripcion": "Pedido actualizado",
                "total": 200,
            },
        )
        self.assertRedirects(response, reverse("pedidos_list"), fetch_redirect_response=False)
        pedido.refresh_from_db()
        self.assertEqual(pedido.descripcion, "Pedido actualizado")
        self.assertEqual(pedido.total, 200)

    def test_export_csv(self):
        Pedido.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            descripcion="Export CSV",
            total=100,
        )
        response = self.client.get(reverse("pedido_export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cliente", response.content)

    def test_export_pdf(self):
        Pedido.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            descripcion="Export PDF",
            total=100,
        )
        response = self.client.get(reverse("pedido_export_pdf"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))


class ActuacionCRUDTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.force_login(self.user)
        self.cliente = Cliente.objects.create(usuario=self.user, nombre="Cliente")
        self.pedido = Pedido.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            descripcion="Pedido",
            total=100,
        )

    def test_create_actuacion(self):
        response = self.client.post(
            reverse("actuacion_nueva"),
            {
                "cliente": self.cliente.pk,
                "pedido": self.pedido.pk,
                "fecha": "2024-01-02",
                "descripcion": "Trabajo",
                "coste": 50,
            },
        )
        self.assertRedirects(response, reverse("actuaciones_list"), fetch_redirect_response=False)
        self.assertEqual(Actuacion.objects.count(), 1)

    def test_edit_actuacion(self):
        act = Actuacion.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            pedido=self.pedido,
            fecha="2024-01-02",
            descripcion="Vieja",
            coste=50,
        )
        response = self.client.post(
            reverse("actuacion_editar", args=[act.pk]),
            {
                "cliente": self.cliente.pk,
                "pedido": self.pedido.pk,
                "fecha": "2024-01-03",
                "descripcion": "Nueva",
                "coste": 80,
            },
        )
        self.assertRedirects(response, reverse("actuaciones_list"), fetch_redirect_response=False)
        act.refresh_from_db()
        self.assertEqual(act.descripcion, "Nueva")
        self.assertEqual(act.coste, 80)

    def test_delete_actuacion(self):
        act = Actuacion.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            pedido=self.pedido,
            fecha="2024-01-02",
            descripcion="Borrar",
            coste=50,
        )
        response = self.client.post(
            reverse("actuacion_eliminar", args=[act.pk])
        )
        self.assertRedirects(response, reverse("actuaciones_list"), fetch_redirect_response=False)
        self.assertEqual(Actuacion.objects.count(), 0)

    def test_export_csv(self):
        Actuacion.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            pedido=self.pedido,
            fecha="2024-01-02",
            descripcion="Export",
            coste=50,
        )
        response = self.client.get(reverse("actuaciones_export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Export", response.content)


class UtilsExportCsvTests(TestCase):
    def test_missing_field_logs_and_blanks(self):
        obj = SimpleNamespace(name="Foo")
        queryset = [obj]
        fields = ["name", "missing"]
        with self.assertLogs("core.utils", level="ERROR") as cm:
            response = export_csv(queryset, fields)
        content = response.content.decode().splitlines()
        self.assertEqual(content[0], "name,missing")
        self.assertEqual(content[1], "Foo,")
        self.assertEqual(len(cm.output), 1)
        self.assertIn("missing", cm.output[0])
