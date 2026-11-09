"""Actividad P2: pruebas unitarias de ServicioInventario."""
from decimal import Decimal

import pytest

from inventario.repositorio import RepositorioProductos, ProductoNoEncontrado
from inventario.servicio_inventario import ServicioInventario


@pytest.fixture
def servicio():
    s = ServicioInventario(RepositorioProductos())
    s.agregar_producto("A1", "Lapicero", Decimal("2.50"), 10)
    return s


def test_agregar_producto_valido(servicio):
    producto = servicio.agregar_producto("B2", "Cuaderno", Decimal("15.00"), 5)
    assert producto.codigo == "B2"
    assert producto.nombre == "Cuaderno"
    assert producto.precio == Decimal("15.00")
    assert servicio.consultar_existencia("B2") == 5


@pytest.mark.parametrize(
    "codigo, nombre, precio, existencia",
    [
        ("", "Sin código", Decimal("1"), 1),
        ("C3", "  ", Decimal("1"), 1),
        ("C3", "Precio cero", Decimal("0"), 1),
        ("C3", "Existencia negativa", Decimal("1"), -1),
        ("A1", "Código duplicado", Decimal("1"), 1),
    ],
)
def test_agregar_producto_invalido(servicio, codigo, nombre, precio, existencia):
    with pytest.raises(ValueError):
        servicio.agregar_producto(codigo, nombre, precio, existencia)


def test_consultar_existencia(servicio):
    assert servicio.consultar_existencia("A1") == 10
    with pytest.raises(ProductoNoEncontrado):
        servicio.consultar_existencia("NOPE")


def test_calcular_total(servicio):
    assert servicio.calcular_total("A1", 4) == Decimal("10.00")
    assert servicio.consultar_existencia("A1") == 10
    assert servicio.calcular_total("A1", 100) == Decimal("250.00")
    with pytest.raises(ValueError):
        servicio.calcular_total("A1", 0)


def test_validar_inventario_suficiente_insuficiente_y_limite(servicio):
    assert servicio.validar_inventario("A1", 3) is True
    assert servicio.validar_inventario("A1", 10) is True   # caso límite
    assert servicio.validar_inventario("A1", 11) is False
    assert servicio.consultar_existencia("A1") == 10
    with pytest.raises(ValueError):
        servicio.validar_inventario("A1", -1)
    with pytest.raises(ProductoNoEncontrado):
        servicio.validar_inventario("NOPE", 1)