from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch

from clientes.models import Cliente
from pedidos.models import Pedido
from facturas.models import Factura
from actuaciones.models import Actuacion
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

    @patch("core.views.export_csv", side_effect=Exception("boom"))
    def test_export_csv_error(self, mock_export):
        self.client.force_login(self.user)
        response = self.client.get(reverse("factura_export_csv"))
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Error al generar CSV", response.content)


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

    @patch("core.views.export_csv", side_effect=Exception("boom"))
    def test_export_csv_error(self, mock_export):
        response = self.client.get(reverse("pedido_export_csv"))
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Error al generar CSV", response.content)

    @patch("core.views.export_pdf", side_effect=Exception("boom"))
    def test_export_pdf_error(self, mock_export):
        response = self.client.get(reverse("pedido_export_pdf"))
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Error al generar PDF", response.content)


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

@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": False,
            "OPTIONS": {
                "loaders": [
                    (
                        "django.template.loaders.locmem.Loader",
                        {
                            "pedidos/pedidos_list.html": "{% for p in pedidos %}{{ p.descripcion }}{% endfor %}",
                            "actuaciones/actuaciones_list.html": "{% for a in actuaciones %}{{ a.descripcion }}{% endfor %}",
                            "facturas/facturas_list.html": "{% for f in facturas %}{{ f.numero }}{% endfor %}",
                        },
                    )
                ]
            },
        }
    ]
)
class AccessControlTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")

        self.cliente1 = Cliente.objects.create(usuario=self.user1, nombre="Cliente1")
        self.cliente2 = Cliente.objects.create(usuario=self.user2, nombre="Cliente2")

        self.pedido1 = Pedido.objects.create(
            usuario=self.user1,
            cliente=self.cliente1,
            fecha="2024-01-01",
            descripcion="Pedido1",
            total=100,
        )
        self.pedido2 = Pedido.objects.create(
            usuario=self.user2,
            cliente=self.cliente2,
            fecha="2024-01-01",
            descripcion="Pedido2",
            total=200,
        )

        self.actuacion1 = Actuacion.objects.create(
            usuario=self.user1,
            cliente=self.cliente1,
            pedido=self.pedido1,
            fecha="2024-01-02",
            descripcion="Act1",
            coste=50,
        )
        self.actuacion2 = Actuacion.objects.create(
            usuario=self.user2,
            cliente=self.cliente2,
            pedido=self.pedido2,
            fecha="2024-01-02",
            descripcion="Act2",
            coste=60,
        )

        self.factura1 = Factura.objects.create(
            usuario=self.user1,
            cliente=self.cliente1,
            pedido=self.pedido1,
            actuacion=self.actuacion1,
            fecha="2024-01-03",
            numero="F1",
            base_imponible=100,
            iva=21,
            irpf=0,
        )
        self.factura2 = Factura.objects.create(
            usuario=self.user2,
            cliente=self.cliente2,
            pedido=self.pedido2,
            actuacion=self.actuacion2,
            fecha="2024-01-03",
            numero="F2",
            base_imponible=100,
            iva=21,
            irpf=0,
        )


    def test_pedidos_list_filters_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("pedidos_list"))
        self.assertContains(response, "Pedido1")
        self.assertNotContains(response, "Pedido2")

    def test_pedidos_list_requires_login(self):
        response = self.client.get(reverse("pedidos_list"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('pedidos_list')}",
            fetch_redirect_response=False,
        )

    def test_actuaciones_list_filters_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("actuaciones_list"))
        self.assertContains(response, "Act1")
        self.assertNotContains(response, "Act2")

    def test_actuaciones_list_requires_login(self):
        response = self.client.get(reverse("actuaciones_list"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('actuaciones_list')}",
            fetch_redirect_response=False,
        )

    def test_facturas_list_filters_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("facturas_list"))
        self.assertContains(response, "F1")
        self.assertNotContains(response, "F2")

    def test_facturas_list_requires_login(self):
        response = self.client.get(reverse("facturas_list"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('facturas_list')}",
            fetch_redirect_response=False,
        )

    def test_pedido_cross_access_forbidden(self):
        self.client.force_login(self.user1)
        with patch(
            "clientes.forms.Cliente.objects.filter",
            return_value=Cliente.objects.all(),
        ):
            response = self.client.post(
                reverse("pedido_nuevo"),
                {
                    "cliente": self.cliente2.pk,
                    "presupuesto": "",
                    "fecha": "2024-01-01",
                    "descripcion": "Cross",
                    "total": 100,
                },
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Pedido.objects.filter(usuario=self.user1).count(), 1)

    def test_actuacion_cross_access_forbidden(self):
        self.client.force_login(self.user1)
        with patch(
            "clientes.forms.Cliente.objects.filter",
            return_value=Cliente.objects.all(),
        ), patch(
            "pedidos.forms.Pedido.objects.filter",
            return_value=Pedido.objects.all(),
        ):
            response = self.client.post(
                reverse("actuacion_nueva"),
                {
                    "cliente": self.cliente2.pk,
                    "pedido": self.pedido2.pk,
                    "fecha": "2024-01-02",
                    "descripcion": "Cross",
                    "coste": 50,
                },
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Actuacion.objects.filter(usuario=self.user1).count(), 1)

    def test_factura_cross_access_forbidden(self):
        self.client.force_login(self.user1)
        with patch(
            "clientes.forms.Cliente.objects.filter",
            return_value=Cliente.objects.all(),
        ), patch(
            "pedidos.forms.Pedido.objects.filter",
            return_value=Pedido.objects.all(),
        ), patch(
            "actuaciones.forms.Actuacion.objects.filter",
            return_value=Actuacion.objects.all(),
        ):
            response = self.client.post(
                reverse("factura_nueva"),
                {
                    "cliente": self.cliente2.pk,
                    "pedido": self.pedido2.pk,
                    "actuacion": self.actuacion2.pk,
                    "fecha": "2024-01-03",
                    "numero": "FX",
                    "base_imponible": 100,
                    "iva": 21,
                    "irpf": 0,
                    "estado": "borrador",
                },
            )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Factura.objects.filter(usuario=self.user1).count(), 1)

