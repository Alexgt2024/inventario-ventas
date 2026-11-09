"""Actividad P2: completar las reglas de negocio y sus pruebas unitarias."""
from decimal import Decimal
from inventario.modelos import Producto
from inventario.repositorio import RepositorioProductos, ProductoNoEncontrado


class ServicioInventario:
    def __init__(self, repositorio: RepositorioProductos) -> None:
        self.repositorio = repositorio

    def agregar_producto(self, codigo: str, nombre: str, precio: Decimal, existencia: int) -> Producto:
        """Registra un producto; valida código, nombre, precio y existencia.

        Requisitos: código/nombre no vacíos; precio > 0; existencia >= 0;
        no permitir códigos duplicados. Devolver el producto guardado.
        """
        if not codigo or not codigo.strip():
            raise ValueError("El código no puede estar vacío")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        if existencia < 0:
            raise ValueError("La existencia no puede ser negativa")
        try:
            self.repositorio.obtener(codigo)
        except ProductoNoEncontrado:
            pass
        else:
            raise ValueError(f"Ya existe un producto con el código {codigo}")
        producto = Producto(codigo=codigo, nombre=nombre, precio=precio, existencia=existencia)
        self.repositorio.guardar(producto)
        return producto

    def consultar_existencia(self, codigo: str) -> int:
        """Devuelve existencias; si no existe, propaga ProductoNoEncontrado."""
        return self.repositorio.obtener(codigo).existencia

    def validar_inventario(self, codigo: str, cantidad: int) -> bool:
        """Exige cantidad > 0 y producto existente.

        Devuelve True cuando hay suficientes unidades. Devuelve False si
        la existencia es insuficiente (no modifica el inventario).
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        producto = self.repositorio.obtener(codigo)
        return producto.existencia >= cantidad

    def calcular_total(self, codigo: str, cantidad: int) -> Decimal:
        """Devuelve precio * cantidad si cantidad > 0 y producto existe.

        No descuenta inventario. Una existencia insuficiente no invalida
        el cálculo de cotización; la venta real lo validará después.
        """
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        producto = self.repositorio.obtener(codigo)
        return producto.precio * cantidad