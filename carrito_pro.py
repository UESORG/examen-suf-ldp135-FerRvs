
import json


# 1. importar_y_validar_orden
def importar_y_validar_orden(json_orden):

    try:
        orden = json.loads(json_orden)

        if "items" not in orden or "total" not in orden:
            raise KeyError("La orden no contiene las llaves 'items' y/o 'total'.")

        if orden["total"] <= 0:
            raise ValueError("El total de la orden debe ser mayor a 0.")

        resultado = orden
        return resultado

    except (KeyError, ValueError, json.JSONDecodeError, TypeError):
        return None


# 2. gestionar_historial_carrito
def gestionar_historial_carrito(historial_pila, accion, item=None):
    
    if accion == "AGREGAR":
        historial_pila.append(item)
        return item
    elif accion == "DESHACER":
        if len(historial_pila) == 0:
            return None
        ultimo_item = historial_pila.pop()
        return ultimo_item
    else:
        return None

# 3. escanear_estanteria_bodega
def escanear_estanteria_bodega(matriz_bodega, fila_centro, col_centro):
    
    contador_unos = 0
    filas_totales = len(matriz_bodega)

    for desplazamiento_fila in range(-1, 2):
        for desplazamiento_col in range(-1, 2):
            fila_actual = fila_centro + desplazamiento_fila
            col_actual = col_centro + desplazamiento_col

            # Respetar límites: la fila debe existir...
            if 0 <= fila_actual < filas_totales:
                columnas_totales = len(matriz_bodega[fila_actual])
                # ...y la columna debe existir dentro de esa fila.
                if 0 <= col_actual < columnas_totales:
                    if matriz_bodega[fila_actual][col_actual] == 1:
                        contador_unos += 1

    return contador_unos

# 4. calcular_descuento_cascada
def calcular_descuento_cascada(nodo_descuento):
    
    if nodo_descuento is None:
        return None

    if "porcentaje_final" in nodo_descuento:
        return nodo_descuento["porcentaje_final"]

    if nodo_descuento.get("cliente_frecuente") is True:
        return calcular_descuento_cascada(nodo_descuento.get("derecha"))
    else:
        return calcular_descuento_cascada(nodo_descuento.get("izquierda"))

# 5. ordenar_productos_quicksort
def ordenar_productos_quicksort(lista_items):
    
    if len(lista_items) <= 1:
        return lista_items

    pivote = lista_items[len(lista_items) // 2]
    precio_pivote = pivote["precio"]

    menores = [item for item in lista_items if item["precio"] < precio_pivote]
    iguales = [item for item in lista_items if item["precio"] == precio_pivote]
    mayores = [item for item in lista_items if item["precio"] > precio_pivote]

    return (
        ordenar_productos_quicksort(menores)
        + iguales
        + ordenar_productos_quicksort(mayores)
    )


# 6. buscar_precio_binario
def buscar_precio_binario(lista_ordenada, precio_buscado):
    
    puntero_inicio = 0
    puntero_fin = len(lista_ordenada) - 1

    while puntero_inicio <= puntero_fin:
        puntero_medio = (puntero_inicio + puntero_fin) // 2
        elemento_medio = lista_ordenada[puntero_medio]

        valor_medio = (
            elemento_medio["precio"]
            if isinstance(elemento_medio, dict)
            else elemento_medio
        )

        if valor_medio == precio_buscado:
            return puntero_medio
        elif valor_medio < precio_buscado:
            puntero_inicio = puntero_medio + 1
        else:
            puntero_fin = puntero_medio - 1

    return -1
