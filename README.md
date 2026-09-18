# Refranes y Recuerdos

Juego de estimulación cognitiva hecho con **Python y Pygame**, pensado para una sesión individual, pausada y positiva.

## Ejecutar

```powershell
python -m pip install -r requirements.txt
python main.py
```

La ventana usa la resolución base requerida: **1280 × 720 a 60 FPS**.

## Estructura modular

- `main.py`: único punto de entrada requerido por el launcher.
- `app.py`: controlador de sesión, puntuación, racha y efectos (juice).
- `models.py`: entidad `Refran` y su validación.
- `refranes.py`: catálogo de 30 refranes.
- `screens.py`: pantallas de bienvenida, juego, reflexión y álbum.
- `ui.py`: componentes visuales reutilizables (botones, campos, popups, efectos).
- `config.py`: resolución, FPS, paleta, tipografía y ritmo de animaciones.

## POO aplicada

- **Abstracción:** `Widget` y `Screen` son clases abstractas que definen contratos claros.
- **Herencia:** `Button`, `TextInput`, `Popup`, `Pill` y `ProgressBar` heredan de `Widget`; las cuatro pantallas heredan de `Screen`.
- **Polimorfismo:** el juego procesa widgets y pantallas a través de los mismos métodos `draw()` y `handle_event()`.
- **Encapsulamiento:** `GameApp`, los widgets y `Refran` mantienen su estado protegido; `Refran.es_respuesta_correcta()` conserva su regla de comparación junto a los datos.

## Tema visual (moderno, cálido y accesible)

Todo el aspecto gráfico vive en `config.py` y se dibuja con las utilidades de `ui.py`:

- **Paleta de alto contraste** pensada para lectura fácil en adultos mayores (tinta cálida sobre crema, acentos vibrantes para acciones y ornamentos).
- **Gradientes y sombras suaves** en fondos, tarjetas y botones (`draw_gradient_rect`, `draw_panel`, `_shadow_surf`).
- **Tipografía automática**: se elige la primera familia moderna disponible (`FONT_STACK`, p. ej. Segoe UI, Calibri o DejaVu Sans).
- **HUD del juego**: barra de progreso animada, chip de avance, badge de tema, puntos y racha.
- **Micro-animaciones**: fundidos de entrada entre pantallas, brillo/escala al pasar el ratón, hundimiento al pulsar y cursor parpadeante.
- **Juice**: partículas, confeti, textos flotantes y destellos al acertar (`FXLayer`), micro-vibración de pantalla en los fallos y mensajes que se desvanecen.

### Cómo personalizar

1. **Colores**: cambia los valores RGB de `config.py` (p. ej. `PRIMARY`, `SUCCESS`, `BG_TOP`). Se aplican en todas las pantallas.
2. **Tipografía**: reordena o añade nombres en `FONT_STACK` (solo fuentes instaladas en el sistema).
3. **Ritmo**: ajusta `FADE_ENTER`, `PRESS_ANIM`, `HOVER_ANIM` o `BURST_LIFE` en segundos.
4. **Efectos**: intensifica la celebración cambiando los números en `GameApp.celebrate()` (`n=`, `speed=`) o las partículas del `FXLayer`.

Los 30 refranes están definidos como objetos `Refran` dentro de `main.py` (importados desde `refranes.py`). Cada uno incluye su respuesta, tema, significado y preguntas para conversación.