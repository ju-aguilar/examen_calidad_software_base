
"""Actividad P2: completar las reglas de negocio y sus pruebas unitarias."""
from decimal import Decimal

from inventario.modelos import Producto
from inventario.repositorio import RepositorioProductos
from inventario.excepciones import InventarioError, ProductoNoEncontrado


class ServicioInventario:
    def __init__(self, repositorio: RepositorioProductos) -> None:
        self.repositorio = repositorio

    def agregar_producto(
        self, codigo: str, nombre: str, precio: Decimal, existencia: int
    ) -> Producto:
        """Registra un producto validando sus datos y evitando duplicados."""

        if not isinstance(codigo, str) or not codigo.strip():
            raise InventarioError("El código no puede estar vacío")

        if not isinstance(nombre, str) or not nombre.strip():
            raise InventarioError("El nombre no puede estar vacío")

        if not isinstance(precio, Decimal) or precio <= 0:
            raise InventarioError("El precio debe ser mayor que cero")

        if isinstance(existencia, bool) or not isinstance(existencia, int) or existencia < 0:
            raise InventarioError("La existencia debe ser un entero mayor o igual a cero")

        try:
            self.repositorio.obtener(codigo)
        except ProductoNoEncontrado:
            pass
        else:
            raise InventarioError("El código del producto ya existe")

        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            existencia=existencia
        )

        self.repositorio.guardar(producto)
        return producto

    def consultar_existencia(self, codigo: str) -> int:
        """Devuelve las existencias del producto solicitado."""

        producto = self.repositorio.obtener(codigo)
        return producto.existencia

    def validar_inventario(self, codigo: str, cantidad: int) -> bool:
        """Comprueba que exista suficiente inventario sin modificarlo."""

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise InventarioError("La cantidad debe ser un entero mayor que cero")

        producto = self.repositorio.obtener(codigo)
        return producto.existencia >= cantidad

    def calcular_total(self, codigo: str, cantidad: int) -> Decimal:
        """Calcula el importe sin descontar las existencias."""

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise InventarioError("La cantidad debe ser un entero mayor que cero")

        producto = self.repositorio.obtener(codigo)
        return producto.precio * cantidad
