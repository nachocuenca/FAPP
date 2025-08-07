from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from .models import Cliente, Pedido, Factura


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


class PedidoEditTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user", password="pass")
        self.cliente = Cliente.objects.create(usuario=self.user, nombre="Cliente")
        self.pedido = Pedido.objects.create(
            usuario=self.user,
            cliente=self.cliente,
            fecha="2024-01-01",
            descripcion="Pedido inicial",
            total=100,
        )

    def test_edit_pedido(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("pedido_editar", args=[self.pedido.pk]),
            {
                "cliente": self.cliente.pk,
                "presupuesto": "",
                "fecha": "2024-02-01",
                "descripcion": "Pedido actualizado",
                "total": 200,
            },
        )
        self.assertRedirects(response, reverse("pedidos_list"))
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.descripcion, "Pedido actualizado")
        self.assertEqual(self.pedido.total, 200)

