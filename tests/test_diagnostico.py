"""Actividad P4: demostrar un defecto, corregirlo y volver a ejecutar."""

import pytest

from inventario.diagnostico import aplicar_descuento


def test_aplicar_descuento():
    """Comprueba que el descuento reduzca correctamente el precio."""
    resultado = aplicar_descuento(100, 10)
    assert resultado == 90


def test_aplicar_descuento_sin_descuento():
    """Porcentaje 0 devuelve el precio original."""
    assert aplicar_descuento(50, 0) == 50


def test_aplicar_descuento_total():
    """Porcentaje 100 deja el precio en 0."""
    assert aplicar_descuento(50, 100) == 0


def test_aplicar_descuento_precio_negativo_lanza_error():
    """Un precio negativo debe lanzar ValueError (cubre la línea 12)."""
    with pytest.raises(ValueError):
        aplicar_descuento(-1, 10)


def test_aplicar_descuento_porcentaje_invalido_lanza_error():
    """Un porcentaje fuera de [0, 100] debe lanzar ValueError (cubre la línea 12)."""
    with pytest.raises(ValueError):
        aplicar_descuento(100, 150)