
"""Actividad P3: pruebas de integración del sistema."""

import pytest
from decimal import Decimal

from inventario.modelos import LineaVenta
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario
from inventario.servicio_ventas import ServicioVentas
from inventario.excepciones import InventarioInsuficiente


def crear_servicios():
    """Crea los servicios utilizando el repositorio real."""
    repositorio = RepositorioProductos()
    inventario = ServicioInventario(repositorio)
    ventas = ServicioVentas(inventario, repositorio)

    return repositorio, inventario, ventas


def test_registrar_producto_y_consultar_inventario():
    repositorio, inventario, ventas = crear_servicios()

    inventario.agregar_producto(
        "P101", "Teclado", Decimal("150.00"), 10
    )

    producto = repositorio.obtener("P101")

    assert producto.codigo == "P101"
    assert producto.nombre == "Teclado"
    assert inventario.consultar_existencia("P101") == 10


def test_registrar_venta_y_actualizar_existencias():
    repositorio, inventario, ventas = crear_servicios()

    inventario.agregar_producto(
        "P102", "Mouse", Decimal("100.00"), 10
    )

    resultado = ventas.registrar_venta(
        LineaVenta(codigo="P102", cantidad=3)
    )

    assert resultado.total == Decimal("300.00")
    assert resultado.unidades == 3
    assert inventario.consultar_existencia("P102") == 7
    assert repositorio.obtener("P102").existencia == 7


def test_rechazar_venta_con_existencias_insuficientes():
    repositorio, inventario, ventas = crear_servicios()

    inventario.agregar_producto(
        "P103", "Monitor", Decimal("900.00"), 2
    )

    with pytest.raises(InventarioInsuficiente):
        ventas.registrar_venta(
            LineaVenta(codigo="P103", cantidad=5)
        )

    assert inventario.consultar_existencia("P103") == 2
    assert repositorio.obtener("P103").existencia == 2
