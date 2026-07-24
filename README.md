# Anatomía del Cráneo — Conteo de Huesos

Aplicación web interactiva (Flask + HTML5/CSS3/JS + [`<model-viewer>`](https://modelviewer.dev/))
para aprender la ubicación de los huesos del cráneo sobre un **modelo 3D real** (no una
ilustración): el usuario selecciona el nombre de cada hueso y hace clic sobre el punto
correspondiente de un cráneo tridimensional que puede rotar y hacer zoom libremente,
recibe retroalimentación inmediata y, al finalizar, obtiene una calificación con
aciertos, errores y tiempo total. El glosario incluye además un modelo 3D individual
rotable de cada uno de los 22 huesos.

El contenido (huesos del neurocráneo y del viscerocráneo, y sus funciones) proviene de
`Anatomia_Craneo_Cerebro.docx`.

## Modelos 3D y atribución

Los modelos 3D (`app/static/models/`) se generaron a partir de datos anatómicos reales
(no ilustraciones ni IA generativa) de **[BodyParts3D/Anatomography](http://lifesciencedb.jp/bp3d/)**
(The Database Center for Life Science, Japón), licenciados bajo
**Creative Commons Attribution-Share Alike 2.1 Japón**. Como todos los huesos provienen
del mismo modelo segmentado, encajan perfectamente al reensamblarse en `skull_full.glb`.

`scripts/build_bone_models.py` descarga los STL originales, los decima (`trimesh` +
`fast-simplification`) y exporta los `.glb` finales — útil si se quiere regenerar los
modelos o ajustar el nivel de detalle. Requiere `pip install trimesh fast-simplification numpy`
(no son dependencias de la app en producción, solo del script de construcción).

Atribución requerida al reutilizar estos archivos:
> BodyParts3D, (c) The Database Center for Life Science licensed under
> CC Attribution-Share Alike 2.1 Japan

Por la cláusula *ShareAlike* de esa licencia, los archivos `.glb` derivados (no el
código de la aplicación) deben seguir compartiéndose bajo la misma licencia si se
redistribuyen.

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
  utils.py               # helper para IP del cliente y comprobar assets estáticos
  data/bones.py          # datos de los 22 huesos (fuente: docx) + coordenadas 3D de hotspots
  blueprints/
    main/routes.py       # página de inicio y glosario
    game/routes.py       # inicio de actividad y endpoints de juego (responder/finalizar)
  templates/              # index, game, glossary + partial del <model-viewer> del cráneo
  static/css, static/js   # estilos responsive y lógica de interacción
  static/models/          # cráneo_full.glb + models/bones/<clave>.glb (ver scripts/build_bone_models.py)
scripts/build_bone_models.py  # descarga y procesa los modelos 3D desde BodyParts3D
config.py                # configuración (SECRET_KEY, base de datos)
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
