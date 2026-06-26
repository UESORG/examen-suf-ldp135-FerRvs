[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/66UDLJ0P)

# Carlos_Fernando_Rivas_Moran_RM22108_LDP_GT2

# Examen_Complementario_LDP2026
Describir aqui como funciona el codigo del archivo carrito_pro.py  y como funcionan los test de test_carrito_pro.py

# E-Commerce Pro — Backend Transaccional

Laboratorio suplementario para la materia Lógica de Programación 

En este repositorio tenemos la implementación del backend transaccional de la
plataforma ficticia "E-Commerce Pro", aplicando algoritmos de búsqueda,
ordenamiento, recursividad y estructuras de datos.

## Archivos del proyecto

- `carrito_pro.py` — Lógica de negocio (las 6 funciones requeridas).
- `test_carrito_pro.py` — Pruebas unitarias con `pytest`.
- `README.md` — Este documento.

## 1. `carrito_pro.py`

### `importar_y_validar_orden(json_orden)`
Recibimos un **string en formato JSON** y lo decodifica con `json.loads()` la cual esta dentro
de un bloque `try/except`. Luego esto se valida, usando `if`, buscando que el diccionario
resultante tenga las llaves `"items"` y `"total"`; en caso de  faltar alguna, lanza
manualmente un `KeyError`. También valida que `"total"` sea mayor a `0`; si
no lo es, lanza un `ValueError`. Todas las excepciones (más errores de
JSON mal formado) son atrapadas en el `except`, devolviendo `None` cuando algo
falla, o el diccionario completo de la orden cuando todo es válido.

### `gestionar_historial_carrito(historial_pila, accion, item=None)`
Trata la lista `historial_pila` como una **Pila (estructura LIFO)**, mutándola
**por referencia** (no se crea una copia). Usa condicionales `if/elif`:
- `"AGREGAR"` → `historial_pila.append(item)` inserta el ítem al final de la
  pila y lo retorna.
- `"DESHACER"` → `historial_pila.pop()` extrae y retorna el último ítem
  agregado; si la pila está vacía, retorna `None` sin lanzar error.

### `escanear_estanteria_bodega(matriz_bodega, fila_centro, col_centro)`
Recorre con dos ciclos `for` anidados un rango de `-1` a `1` en filas y
columnas (la vecindad 3x3) alrededor de la coordenada central. Antes de leer
cada celda valida con `if` que el índice de fila y columna esté dentro de los
límites reales de la matriz, evitando así un `IndexError` cuando el centro
está en un borde o esquina. Cada vez que encuentra un `1` dentro del rango
válido, incrementa una variable acumuladora (`contador_unos`), que es
finalmente retornada.

### `calcular_descuento_cascada(nodo_descuento)`
Recorre recursivamente un **árbol binario representado con diccionarios**.
- **Caso base:** si el nodo actual contiene la llave `"porcentaje_final"`, se
  retorna ese valor de inmediato (aquí termina la recursión).
- **Caso recursivo:** si `"cliente_frecuente"` es `True`, la función se llama
  a sí misma con el sub-árbol `"derecha"`; si es `False`, se llama con
  `"izquierda"`. Si en algún punto el nodo es `None`, se retorna `None` para
  evitar errores.

### `ordenar_productos_quicksort(lista_items)`
Implementa **QuickSort** de forma recursiva sobre una lista de diccionarios
de productos, comparando la llave `"precio"`. En cada llamada se elige un
elemento *pivote* y, usando **listas por comprensión**, se generan tres
sublistas: `menores`, `iguales` y `mayores` al precio del pivote. La función
se llama recursivamente sobre `menores` y `mayores`, y el resultado final se
concatena como `menores + iguales + mayores`, quedando la lista ordenada de
forma ascendente. El caso base es una lista de 0 o 1 elementos, que se
retorna sin cambios.

### `buscar_precio_binario(lista_ordenada, precio_buscado)`
Implementa **Búsqueda Binaria** mediante un ciclo `while` controlado por la
condición `puntero_inicio <= puntero_fin`. En cada iteración calcula el
índice medio, compara (`if/elif/else`) el precio en esa posición contra
`precio_buscado`, y ajusta los punteros (`puntero_inicio` o `puntero_fin`)
para descartar la mitad de la lista que no puede contener el valor buscado.
Esto logra una complejidad logarítmica O(log n). Si los punteros se cruzan
sin encontrar coincidencia, retorna `-1`. La función admite tanto listas de
números puros como listas de diccionarios con llave `"precio"`.

---

## 2. `test_carrito_pro.py`
Las pruebas están escritas con **pytest** y organizadas en una clase por cada
función, cubriendo los escenarios pedidos en la consigna:

- **`TestImportarYValidarOrden`** 
— prueba una orden válida, un JSON
  corrupto (mal formado), JSON sin la llave `"items"`, sin la llave
  `"total"`, y con `"total"` igual a 0 o negativo. Todos los casos de fallo
  deben retornar `None`.

- **`TestGestionarHistorialCarrito`
** — verifica que `"AGREGAR"` mute la
  lista original (prueba de mutación por referencia), que el orden LIFO se
  respete al agregar varios ítems, que `"DESHACER"` extraiga el último ítem
  agregado, que una pila vacía retorne `None` sin fallar, y que una acción
  desconocida no altere la pila.

- **`TestEscanearEstanteriaBodega`** 
— prueba el conteo en el centro de una
  matriz, en la esquina superior izquierda y en la esquina inferior derecha
  (límites de la matriz, sin desbordamiento), y una matriz sin ningún `1`.

- **`TestCalcularDescuentoCascada`** 
— prueba el caso base directo, el
  descenso por `"derecha"` cuando `cliente_frecuente` es `True`, el descenso
  por `"izquierda"` cuando es `False`, una recursión de varios niveles
  combinando ambos casos, y un nodo `None`.

- **`TestOrdenarProductosQuicksort`** 
— prueba el ordenamiento correcto de una
  lista de productos, una lista vacía, una lista de un solo elemento, precios
  repetidos, y una prueba de "eficiencia" con 500 elementos generados
  aleatoriamente para confirmar que el algoritmo recursivo termina y ordena
  correctamente listas más grandes.
  
- **`TestBuscarPrecioBinario`** 
— prueba la búsqueda de un precio existente y
  uno inexistente, búsqueda sobre una lista de diccionarios, una lista vacía,
  los elementos extremos (primero y último), y una prueba de integración que
  combina `ordenar_productos_quicksort` + `buscar_precio_binario`.

### Cómo ejecutar las pruebas

```bash
pip install pytest
pytest test_carrito_pro.py -v
```

Todas las pruebas (31 en total) deben pasar exitosamente (`PASSED`).
