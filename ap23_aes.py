"""
AP 23 - Programa con AES (MF0489_3)

Comparacion entre AES-ECB y AES-CTR con claves de 128 y 256 bits.
Ejercicio educativo: ECB no se recomienda para datos reales.
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def aes_mode_ecb_basic(texto_plano, clave_cifrado):
    """Cifra en ECB agregando bytes nulos hasta completar bloques de 16."""
    # Primero probamos sin padding, como indica el ejercicio.
    try:
        aes = AES.new(clave_cifrado, AES.MODE_ECB)
        aes.encrypt(texto_plano)
        print("ECB sin padding: el tamaño ya es multiplo de 16.")

    except ValueError as error:
        print("ECB sin padding - Error:", error)

    # El profesor utiliza bytes nulos como padding en este ejemplo.
    texto_padding = texto_plano

    while len(texto_padding) % 16 != 0:
        texto_padding += b"\x00"

    aes = AES.new(clave_cifrado, AES.MODE_ECB)
    texto_cifrado = aes.encrypt(texto_padding)

    print("Texto con padding:", texto_padding)
    print("Tamaño con padding:", len(texto_padding), "bytes")
    print("Texto cifrado ECB (hex):", texto_cifrado.hex())
    print("Tamaño cifrado ECB:", len(texto_cifrado), "bytes")

    return texto_cifrado


def aes_mode_ctr_basic(texto_plano, clave_cifrado):
    """Cifra en CTR, que no requiere padding."""
    aes = AES.new(clave_cifrado, AES.MODE_CTR)
    texto_cifrado = aes.encrypt(texto_plano)

    print("Texto cifrado CTR (hex):", texto_cifrado.hex())
    print("Tamaño cifrado CTR:", len(texto_cifrado), "bytes")
    print("Nonce CTR (hex):", aes.nonce.hex())

    # Para descifrar hay que conservar la misma clave y el mismo nonce.
    descifrador = AES.new(clave_cifrado, AES.MODE_CTR, nonce=aes.nonce)
    comprobacion = descifrador.decrypt(texto_cifrado)
    print("Comprobacion del descifrado CTR:", comprobacion == texto_plano)

    return texto_cifrado, aes.nonce


if __name__ == "__main__":
    texto = input("Introduce un mensaje para Bob: ")
    texto_plano = texto.encode("utf-8")

    print("\nTexto original:", texto)
    print("Tamaño original:", len(texto_plano), "bytes")

    # Parte 1: clave de 16 bytes = 128 bits (proporcionada en clase).
    clave_128 = b'A\x83\xbeU\xd7\xa9b\x18\x85AN0\xbft\xc3\xab'
    print("\n--- AES 128 BITS - ECB ---")
    cifrado_ecb_128 = aes_mode_ecb_basic(texto_plano, clave_128)

    print("\n--- AES 128 BITS - CTR ---")
    cifrado_ctr_128, nonce_128 = aes_mode_ctr_basic(texto_plano, clave_128)

    # Parte 2: clave de 32 bytes = 256 bits.
    clave_256 = get_random_bytes(32)
    print("\n--- AES 256 BITS - ECB ---")
    cifrado_ecb_256 = aes_mode_ecb_basic(texto_plano, clave_256)

    print("\n--- AES 256 BITS - CTR ---")
    cifrado_ctr_256, nonce_256 = aes_mode_ctr_basic(texto_plano, clave_256)

    print("\n--- RESUMEN DE TAMAÑOS ---")
    print("Texto plano:  ", len(texto_plano), "bytes")
    print("ECB 128 bits: ", len(cifrado_ecb_128), "bytes")
    print("CTR 128 bits: ", len(cifrado_ctr_128), "bytes")
    print("ECB 256 bits: ", len(cifrado_ecb_256), "bytes")
    print("CTR 256 bits: ", len(cifrado_ctr_256), "bytes")
