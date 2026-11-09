"""Actividad P4: localizar, corregir y demostrar un defecto deliberado."""


def aplicar_descuento(precio: float, porcentaje: float) -> float:
    """Calcula el precio con descuento.

    Contrato: porcentaje entre 0 y 100; precio no negativo.
    Por ejemplo, un 10 % debe reducir el precio en una décima parte.
    """
    if precio < 0 or not 0 <= porcentaje <= 100:
        raise ValueError("Precio o porcentaje inválido")
    # DEFECTO INTENCIONAL del examen: identificar con una prueba y corregir.
    

    return precio - precio * (porcentaje / 100)
