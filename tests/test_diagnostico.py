
"""Actividad P4: demostrar un defecto, corregirlo y volver a ejecutar."""

from inventario.diagnostico import aplicar_descuento


def test_aplicar_descuento():
    """Comprueba que el descuento reduzca correctamente el precio."""
    resultado = aplicar_descuento(100, 10)

    assert resultado == 90
