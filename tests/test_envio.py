import unittest
from decimal import Decimal

from repuestos.envio import calcular_envio

class TestEnvio(unittest.TestCase):
    def test_cobra_150_si_el_subtotal_es_menor_a_3000(self):
        self.assertEqual(calcular_envio(Decimal("2999.99")), Decimal("150"))

        def test_envio_gratis_desde_3000(self):
            self.assertEqual(calcular_envio(Decimal("3000")), Decimal("0"))
