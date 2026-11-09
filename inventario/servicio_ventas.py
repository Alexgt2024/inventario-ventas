"""Actividad P3: integrar inventario, repositorio y registro de ventas."""
from inventario.excepciones import InventarioInsuficiente
from inventario.modelos import LineaVenta, ResultadoVenta
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario


class ServicioVentas:
    def __init__(self, inventario: ServicioInventario, repositorio: RepositorioProductos) -> None:
        self.inventario = inventario
        self.repositorio = repositorio

    def registrar_venta(self, linea: LineaVenta) -> ResultadoVenta:
        """Vende una línea de producto.

        Reglas: cantidad > 0, producto existente, existencias suficientes.
        Si no hay existencia, lanzar InventarioInsuficiente.
        Si se concreta la venta, descontar unidades exactamente una vez,
        devolver total y unidades. Ante error, no modificar existencias.
        """
        # Todas las validaciones y el cálculo ocurren ANTES de modificar el stock,
        # así que cualquier error deja las existencias intactas.
        # validar_inventario lanza ValueError si cantidad <= 0 y
        # ProductoNoEncontrado si el producto no existe.
        if not self.inventario.validar_inventario(linea.codigo, linea.cantidad):
            raise InventarioInsuficiente(
                f"Existencias insuficientes para {linea.codigo}: "
                f"se pidieron {linea.cantidad}"
            )

        total = self.inventario.calcular_total(linea.codigo, linea.cantidad)

        # Único punto donde se modifica el inventario (exactamente una vez).
        existencia_actual = self.repositorio.obtener(linea.codigo).existencia
        self.repositorio.actualizar_existencia(
            linea.codigo, existencia_actual - linea.cantidad
        )

        return ResultadoVenta(total=total, unidades=linea.cantidad)