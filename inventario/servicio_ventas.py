
"""Actividad P3: integrar inventario, repositorio y registro de ventas."""

from inventario.modelos import LineaVenta, ResultadoVenta
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario
from inventario.excepciones import InventarioInsuficiente


class ServicioVentas:
    def __init__(
        self,
        inventario: ServicioInventario,
        repositorio: RepositorioProductos
    ) -> None:
        self.inventario = inventario
        self.repositorio = repositorio

    def registrar_venta(self, linea: LineaVenta) -> ResultadoVenta:
        """Registra una venta y descuenta las existencias correspondientes."""

        # Comprobar que existe suficiente inventario.
        disponible = self.inventario.validar_inventario(
            linea.codigo, linea.cantidad
        )

        if not disponible:
            raise InventarioInsuficiente(
                f"Existencias insuficientes para el producto {linea.codigo}"
            )

        # Calcular el importe de la venta.
        total = self.inventario.calcular_total(
            linea.codigo, linea.cantidad
        )

        # Consultar las existencias actuales.
        producto = self.repositorio.obtener(linea.codigo)

        # Descontar las unidades vendidas una sola vez.
        nueva_existencia = producto.existencia - linea.cantidad

        self.repositorio.actualizar_existencia(
            linea.codigo, nueva_existencia
        )

        # Devolver el resultado de la venta.
        return ResultadoVenta(
            total=total,
            unidades=linea.cantidad
        )
