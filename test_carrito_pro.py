
import json
import pytest

from carrito_pro import (
    importar_y_validar_orden,
    gestionar_historial_carrito,
    escanear_estanteria_bodega,
    calcular_descuento_cascada,
    ordenar_productos_quicksort,
    buscar_precio_binario,
)


# 1. importar_y_validar_orden
class TestImportarYValidarOrden:

    def test_orden_valida_retorna_diccionario(self):
        json_valido = json.dumps({"items": ["mouse", "teclado"], "total": 25.5})
        resultado = importar_y_validar_orden(json_valido)
        assert resultado is not None
        assert resultado["total"] == 25.5
        assert resultado["items"] == ["mouse", "teclado"]

    def test_json_corrupto_retorna_none(self):
        json_corrupto = "{items: [mouse, teclado], total: 25.5"  # JSON mal formado
        resultado = importar_y_validar_orden(json_corrupto)
        assert resultado is None

    def test_falta_llave_items_retorna_none(self):
        json_sin_items = json.dumps({"total": 10})
        resultado = importar_y_validar_orden(json_sin_items)
        assert resultado is None

    def test_falta_llave_total_retorna_none(self):
        json_sin_total = json.dumps({"items": ["audifonos"]})
        resultado = importar_y_validar_orden(json_sin_total)
        assert resultado is None

    def test_total_negativo_retorna_none(self):
        json_total_negativo = json.dumps({"items": ["audifonos"], "total": -5})
        resultado = importar_y_validar_orden(json_total_negativo)
        assert resultado is None

    def test_total_cero_retorna_none(self):
        json_total_cero = json.dumps({"items": ["audifonos"], "total": 0})
        resultado = importar_y_validar_orden(json_total_cero)
        assert resultado is None


# 2. gestionar_historial_carrito
class TestGestionarHistorialCarrito:

    def test_agregar_item_muta_la_lista_original(self):
        pila = []
        gestionar_historial_carrito(pila, "AGREGAR", "laptop")
        assert pila == ["laptop"]  # confirma mutación por referencia

    def test_agregar_varios_items_mantiene_orden_lifo(self):
        pila = []
        gestionar_historial_carrito(pila, "AGREGAR", "item1")
        gestionar_historial_carrito(pila, "AGREGAR", "item2")
        gestionar_historial_carrito(pila, "AGREGAR", "item3")
        assert pila == ["item1", "item2", "item3"]

    def test_deshacer_extrae_el_ultimo_item_agregado(self):
        pila = ["item1", "item2", "item3"]
        resultado = gestionar_historial_carrito(pila, "DESHACER")
        assert resultado == "item3"
        assert pila == ["item1", "item2"]  # la pila original se modificó

    def test_deshacer_en_pila_vacia_retorna_none(self):
        pila = []
        resultado = gestionar_historial_carrito(pila, "DESHACER")
        assert resultado is None
        assert pila == []

    def test_accion_desconocida_retorna_none(self):
        pila = ["item1"]
        resultado = gestionar_historial_carrito(pila, "ACCION_INVALIDA")
        assert resultado is None
        assert pila == ["item1"]  # no debe mutarse


# 3. escanear_estanteria_bodega
class TestEscanearEstanteriaBodega:

    def test_centro_de_matriz_cuenta_correctamente(self):
        matriz = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
        # vecindad completa 3x3 alrededor del centro (1,1)
        resultado = escanear_estanteria_bodega(matriz, 1, 1)
        assert resultado == 5

    def test_esquina_superior_izquierda_respeta_limites(self):
        matriz = [
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0],
        ]
        # (0,0) está en la esquina, solo 4 celdas son válidas (sin desbordar)
        resultado = escanear_estanteria_bodega(matriz, 0, 0)
        assert resultado == 4

    def test_esquina_inferior_derecha_no_desborda(self):
        matriz = [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 1],
        ]
        resultado = escanear_estanteria_bodega(matriz, 2, 2)
        assert resultado == 4  # no debe lanzar IndexError

    def test_matriz_sin_unos_retorna_cero(self):
        matriz = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        resultado = escanear_estanteria_bodega(matriz, 1, 1)
        assert resultado == 0


# 4. calcular_descuento_cascada
class TestCalcularDescuentoCascada:

    def test_caso_base_directo(self):
        nodo = {"porcentaje_final": 10}
        assert calcular_descuento_cascada(nodo) == 10

    def test_cliente_frecuente_baja_por_derecha(self):
        arbol = {
            "cliente_frecuente": True,
            "izquierda": {"porcentaje_final": 5},
            "derecha": {"porcentaje_final": 20},
        }
        assert calcular_descuento_cascada(arbol) == 20

    def test_cliente_no_frecuente_baja_por_izquierda(self):
        arbol = {
            "cliente_frecuente": False,
            "izquierda": {"porcentaje_final": 5},
            "derecha": {"porcentaje_final": 20},
        }
        assert calcular_descuento_cascada(arbol) == 5

    def test_recursividad_en_varios_niveles(self):
        arbol = {
            "cliente_frecuente": True,
            "izquierda": {"porcentaje_final": 1},
            "derecha": {
                "cliente_frecuente": False,
                "izquierda": {"porcentaje_final": 15},
                "derecha": {"porcentaje_final": 30},
            },
        }
        # primer nivel: True -> derecha; segundo nivel: False -> izquierda
        assert calcular_descuento_cascada(arbol) == 15

    def test_nodo_vacio_retorna_none(self):
        assert calcular_descuento_cascada(None) is None


# 5. ordenar_productos_quicksort
class TestOrdenarProductosQuicksort:

    def test_ordena_lista_de_precios_correctamente(self):
        productos = [
            {"nombre": "mouse", "precio": 15},
            {"nombre": "laptop", "precio": 800},
            {"nombre": "cable", "precio": 3},
            {"nombre": "monitor", "precio": 150},
        ]
        resultado = ordenar_productos_quicksort(productos)
        precios_ordenados = [p["precio"] for p in resultado]
        assert precios_ordenados == [3, 15, 150, 800]

    def test_lista_vacia_retorna_lista_vacia(self):
        assert ordenar_productos_quicksort([]) == []

    def test_lista_de_un_elemento_se_retorna_igual(self):
        productos = [{"nombre": "mouse", "precio": 10}]
        assert ordenar_productos_quicksort(productos) == productos

    def test_lista_con_precios_repetidos(self):
        productos = [
            {"nombre": "A", "precio": 10},
            {"nombre": "B", "precio": 5},
            {"nombre": "C", "precio": 10},
            {"nombre": "D", "precio": 5},
        ]
        resultado = ordenar_productos_quicksort(productos)
        precios_ordenados = [p["precio"] for p in resultado]
        assert precios_ordenados == [5, 5, 10, 10]

    def test_eficiencia_con_lista_grande(self):
        # Verifica que el algoritmo termine correctamente con una entrada
        # de mayor tamaño (sensibilidad a la eficiencia/recursividad).
        import random

        productos = [{"id": i, "precio": random.randint(1, 10000)} for i in range(500)]
        resultado = ordenar_productos_quicksort(productos)
        precios_ordenados = [p["precio"] for p in resultado]
        assert precios_ordenados == sorted(precios_ordenados)


# 6. buscar_precio_binario
class TestBuscarPrecioBinario:

    def test_encuentra_precio_existente_en_lista_de_numeros(self):
        precios = [3, 15, 150, 800]
        resultado = buscar_precio_binario(precios, 150)
        assert resultado == 2

    def test_precio_no_existente_retorna_menos_uno(self):
        precios = [3, 15, 150, 800]
        resultado = buscar_precio_binario(precios, 99)
        assert resultado == -1

    def test_busca_en_lista_de_diccionarios_ordenada(self):
        productos_ordenados = [
            {"nombre": "cable", "precio": 3},
            {"nombre": "mouse", "precio": 15},
            {"nombre": "monitor", "precio": 150},
            {"nombre": "laptop", "precio": 800},
        ]
        resultado = buscar_precio_binario(productos_ordenados, 800)
        assert resultado == 3

    def test_lista_vacia_retorna_menos_uno(self):
        assert buscar_precio_binario([], 10) == -1

    def test_primer_y_ultimo_elemento(self):
        precios = [1, 2, 3, 4, 5]
        assert buscar_precio_binario(precios, 1) == 0
        assert buscar_precio_binario(precios, 5) == 4

    def test_integracion_quicksort_y_busqueda_binaria(self):
        # Prueba de integración: ordena con quicksort y luego busca
        productos = [
            {"nombre": "A", "precio": 50},
            {"nombre": "B", "precio": 5},
            {"nombre": "C", "precio": 200},
        ]
        ordenados = ordenar_productos_quicksort(productos)
        indice = buscar_precio_binario(ordenados, 50)
        assert ordenados[indice]["nombre"] == "A"
