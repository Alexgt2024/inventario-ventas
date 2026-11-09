"""Actividad P3: pruebas que integran servicio de inventario, repositorio y ventas."""
from decimal import Decimal

import pytest

from inventario.excepciones import InventarioInsuficiente
from inventario.modelos import LineaVenta
from inventario.repositorio import RepositorioProductos
from inventario.servicio_inventario import ServicioInventario
from inventario.servicio_ventas import ServicioVentas


@pytest.fixture
def repositorio():
    return RepositorioProductos()


@pytest.fixture
def inventario(repositorio):
    return ServicioInventario(repositorio)


@pytest.fixture
def ventas(inventario, repositorio):
    return ServicioVentas(inventario, repositorio)


def test_alta_producto_y_consulta_de_inventario(inventario, repositorio):
    """Flujo 1: alta de producto -> consulta de inventario."""
    producto = inventario.agregar_producto("A1", "Lapicero", Decimal("2.50"), 10)

    assert inventario.consultar_existencia("A1") == 10
    assert repositorio.obtener("A1") == producto
    assert [p.codigo for p in repositorio.listar()] == ["A1"]


def test_alta_venta_descuenta_existencias_y_calcula_total(inventario, ventas):
    """Flujo 2: alta -> venta -> descuento de existencias -> total."""
    inventario.agregar_producto("A1", "Lapicero", Decimal("2.50"), 10)

    resultado = ventas.registrar_venta(LineaVenta(codigo="A1", cantidad=4))

    assert resultado.total == Decimal("10.00")
    assert resultado.unidades == 4
    assert inventario.consultar_existencia("A1") == 6   # descontó una sola vez


def test_venta_insuficiente_se_rechaza_sin_modificar_stock(inventario, ventas):
    """Flujo 3: alta -> intento de venta insuficiente -> rechazo sin tocar stock."""
    inventario.agregar_producto("A1", "Lapicero", Decimal("2.50"), 10)

    with pytest.raises(InventarioInsuficiente):
        ventas.registrar_venta(LineaVenta(codigo="A1", cantidad=11))

    assert inventario.consultar_existencia("A1") == 10  # stock intacto