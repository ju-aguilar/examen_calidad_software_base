
"""Pruebas unitarias de las reglas de negocio del inventario."""

import pytest
from decimal import Decimal

from inventario.servicio_inventario import ServicioInventario
from inventario.repositorio import RepositorioProductos
from inventario.excepciones import InventarioError, ProductoNoEncontrado


@pytest.fixture
def servicio():
    repositorio = RepositorioProductos()
    return ServicioInventario(repositorio)


def test_agregar_producto_valido(servicio):
    producto = servicio.agregar_producto(
        "P001", "Teclado", Decimal("150.00"), 10
    )

    assert producto.codigo == "P001"
    assert producto.nombre == "Teclado"
    assert producto.precio == Decimal("150.00")
    assert producto.existencia == 10


def test_rechazar_producto_con_precio_cero(servicio):
    with pytest.raises(InventarioError):
        servicio.agregar_producto(
            "P002", "Mouse", Decimal("0"), 5
        )


def test_rechazar_codigo_duplicado(servicio):
    servicio.agregar_producto(
        "P003", "Monitor", Decimal("900"), 4
    )

    with pytest.raises(InventarioError):
        servicio.agregar_producto(
            "P003", "Otro monitor", Decimal("800"), 3
        )


def test_existencia_cero_es_valida(servicio):
    servicio.agregar_producto(
        "P004", "Impresora", Decimal("500"), 0
    )

    assert servicio.consultar_existencia("P004") == 0


def test_consultar_producto_inexistente(servicio):
    with pytest.raises(ProductoNoEncontrado):
        servicio.consultar_existencia("NO-EXISTE")


def test_validar_inventario_suficiente(servicio):
    servicio.agregar_producto(
        "P005", "Laptop", Decimal("5000"), 8
    )

    assert servicio.validar_inventario("P005", 5) is True
    assert servicio.consultar_existencia("P005") == 8


def test_validar_inventario_insuficiente(servicio):
    servicio.agregar_producto(
        "P006", "Tablet", Decimal("2000"), 3
    )

    assert servicio.validar_inventario("P006", 4) is False
    assert servicio.consultar_existencia("P006") == 3


def test_calcular_total_sin_descontar_existencias(servicio):
    servicio.agregar_producto(
        "P007", "Celular", Decimal("1200.50"), 2
    )

    total = servicio.calcular_total("P007", 3)

    assert total == Decimal("3601.50")
    assert servicio.consultar_existencia("P007") == 2


def test_rechazar_cantidad_cero(servicio):
    servicio.agregar_producto(
        "P008", "Audífonos", Decimal("100"), 5
    )

    with pytest.raises(InventarioError):
        servicio.validar_inventario("P008", 0)


def test_rechazar_nombre_vacio(servicio):
    with pytest.raises(InventarioError):
        servicio.agregar_producto(
            "P009", "   ", Decimal("100"), 5
        )
