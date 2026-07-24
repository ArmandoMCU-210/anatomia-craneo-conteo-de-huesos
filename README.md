# Anatomía del Cráneo — Conteo de Huesos

Aplicación web interactiva (Flask + HTML5/CSS3/JS) para aprender la ubicación de los
huesos del cráneo. El usuario selecciona el nombre de cada hueso y lo coloca sobre el
punto correspondiente de un esquema lateral del cráneo, recibe retroalimentación
inmediata y, al finalizar, obtiene una calificación con aciertos, errores y tiempo total.

El contenido (huesos del neurocráneo y del viscerocráneo, y sus funciones) proviene de
`Anatomia_Craneo_Cerebro.docx`.

## Requisitos

- Python 3.10+

## Instalación y ejecución

```bash
pip install -r requirements.txt
python run.py
```

La app queda disponible en `http://127.0.0.1:5000/`.

## Estructura del proyecto

```
app/
  __init__.py          # application factory
  models.py             # modelo Attempt (registro de intentos por IP)
  utils.py               # helper para obtener la IP del cliente
  data/bones.py          # datos de los 22 huesos (fuente: docx) + coordenadas del SVG
  blueprints/
    main/routes.py       # página de inicio y glosario
    game/routes.py       # inicio de actividad y endpoints de juego (responder/finalizar)
  templates/              # index, game, glossary + partial del SVG del cráneo
  static/css, static/js   # estilos responsive y lógica de interacción
config.py                # configuración (SECRET_KEY, base de datos SQLite)
run.py                    # punto de entrada
```

## Registro de intentos

Cada intento completado se guarda en base de datos (SQLite en local) con la dirección
IP del dispositivo, fecha/hora, tiempo empleado, calificación, aciertos y errores. La
pantalla de resultados muestra cuántas veces se ha realizado la actividad desde la
misma IP.

## Despliegue en Vercel

El proyecto incluye `vercel.json` y `api/index.py` (punto de entrada serverless que
expone la app Flask). Pasos:

1. Importa el repositorio de GitHub en [vercel.com/new](https://vercel.com/new) (o usa
   `vercel` / `vercel --prod` con la CLI ya autenticada).
2. Configura las variables de entorno del proyecto en Vercel:
   - `SECRET_KEY`: una cadena aleatoria y secreta (obligatoria en producción).
   - `DATABASE_URL`: cadena de conexión a una base de datos **Postgres** (Vercel Postgres,
     Neon, Supabase, etc.), con formato `postgresql://usuario:password@host:puerto/bd`.

> **Importante:** Vercel ejecuta la app en funciones serverless con sistema de archivos
> de solo lectura (salvo `/tmp`, que no persiste entre invocaciones). Si no configuras
> `DATABASE_URL` con una base de datos real, la app seguirá funcionando pero el
> historial de intentos por IP se reiniciará constantemente al usar SQLite en `/tmp`.
> Para que el conteo de intentos sea confiable en producción, es necesario usar Postgres
> (o similar) mediante `DATABASE_URL`. Localmente, sin esa variable, se sigue usando
> SQLite en `instance/attempts.db` sin ninguna configuración adicional.
