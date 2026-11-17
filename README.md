# Repuestos Pro

Pedidos de repuestos Mercedes-Benz: de código que "funciona" a código profesional.
Proyecto para demostrar Clean Code, Git, SOLID y Testing/TDD.

## Requisitos

Python 3.8 o superior. No necesita instalar nada más (usa `unittest`, que viene con Python).

## Cómo correrlo

Abre la terminal **dentro de la carpeta raíz del proyecto** (`repuestos-pro`):

```bash
python -m unittest -v      # corre todas las pruebas
python main.py             # pedido con el código limpio
python modulo1_antes.py    # el mismo pedido con el código original
```

En Windows, si `python` no funciona, usa `py`.

## Estructura

| Archivo | Qué muestra |
| --- | --- |
| `modulo1_antes.py` | El código original, con code smells a propósito |
| `repuestos/modelos.py` | Los datos: `Repuesto` y `LineaPedido` |
| `repuestos/descuentos.py` | O y L de SOLID: descuentos intercambiables |
| `repuestos/repositorio.py` | D de SOLID: acceso a datos detrás de una abstracción |
| `repuestos/notificador.py` | I de SOLID: interfaz pequeña |
| `repuestos/pedido.py` | S de SOLID: la lógica del pedido |
| `main.py` | Demo del código limpio |
| `tests/test_descuentos.py` | Pruebas con AAA y prueba de contrato (Liskov) |
| `tests/test_pedido.py` | Dobles de prueba: fake y mock |
| `tests/test_refactor_seguro.py` | Refactor seguro: viejo y nuevo dan el mismo resultado |
