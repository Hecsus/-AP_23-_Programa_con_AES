"""Comprobaciones simples de la AP23 (ejecutar: python -m unittest)."""

import io
import unittest
from contextlib import redirect_stdout

from Crypto.Random import get_random_bytes

from ap23_aes import aes_mode_ecb_basic, aes_mode_ctr_basic


class PruebasAES(unittest.TestCase):
    def comprobar_tamanos(self, texto, largo_clave):
        clave = get_random_bytes(largo_clave)

        # Ocultamos las salidas explicativas durante las pruebas automaticas.
        with redirect_stdout(io.StringIO()):
            ecb = aes_mode_ecb_basic(texto, clave)
            ctr, nonce = aes_mode_ctr_basic(texto, clave)

        self.assertEqual(len(ecb) % 16, 0)
        self.assertEqual(len(ctr), len(texto))
        self.assertGreater(len(nonce), 0)
        self.assertEqual(len(ecb), ((len(texto) + 15) // 16) * 16)

    def test_hola_bob(self):
        self.comprobar_tamanos(b"Hola Bob", 16)
        self.comprobar_tamanos(b"Hola Bob", 32)

    def test_mensajes_largos(self):
        for largo in [16, 17, 31, 32, 33]:
            self.comprobar_tamanos(b"A" * largo, 16)
            self.comprobar_tamanos(b"A" * largo, 32)

    def test_texto_utf8(self):
        self.comprobar_tamanos("¡Hola, Bob!".encode("utf-8"), 16)


if __name__ == "__main__":
    unittest.main()
