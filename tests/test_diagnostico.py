"""Actividad P4: demostrar un defecto, corregirlo y volver a ejecutar."""
import pytest

from inventario.diagnostico import aplicar_descuento


def test_descuento_del_diez_por_ciento_reduce_el_precio():
    # Contrato: un 10 % reduce el precio en una décima parte -> 100 pasa a 90.
    assert aplicar_descuento(100.0, 10.0) == pytest.approx(90.0)


def test_descuento_del_cien_por_ciento_deja_el_precio_en_cero():
    # Caso límite: 100 % de descuento -> el precio final es 0.
    assert aplicar_descuento(50.0, 100.0) == pytest.approx(0.0)