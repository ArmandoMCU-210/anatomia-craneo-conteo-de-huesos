"""Descarga y procesa los modelos 3D de los huesos del cráneo usados por la app.

Fuente de datos: BodyParts3D/Anatomography (The Database Center for Life Science,
Japón), licenciado bajo Creative Commons Attribution-Share Alike 2.1 Japón.
http://lifesciencedb.jp/bp3d/  ·  https://github.com/Kevin-Mattheus-Moerman/BodyParts3D

Atribución requerida al reutilizar estos archivos:
"BodyParts3D, (c) The Database Center for Life Science licensed under
CC Attribution-Share Alike 2.1 Japan"

Requiere: pip install trimesh fast-simplification numpy

Genera:
  app/static/models/bones/<clave>.glb   (un modelo por hueso, recentrado, para el glosario)
  app/static/models/skull_full.glb      (cráneo completo ensamblado, para el juego)

Los IDs FMA (Foundational Model of Anatomy) y las coordenadas de los hotspots del
juego (app/data/bones.py, campo "marker3d") dependen de este script: si se vuelve a
generar, hay que recalcular y actualizar esas coordenadas.
"""

import os
import urllib.request

import numpy as np
import trimesh

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_BONES_DIR = os.path.join(BASE_DIR, "app", "static", "models", "bones")
OUT_SKULL = os.path.join(BASE_DIR, "app", "static", "models", "skull_full.glb")
STL_CACHE = os.path.join(BASE_DIR, ".cache", "bodyparts3d_stl")

BASE_URL = "https://raw.githubusercontent.com/Kevin-Mattheus-Moerman/BodyParts3D/main/assets/BodyParts3D_data/stl/{}.stl"

# clave del hueso (debe coincidir con app/data/bones.py) -> IDs FMA.
# Para huesos pares, el primer ID es el lado usado como referencia del hotspot.
FMA_MAP = {
    "frontal": ["FMA52734"],
    "parietal": ["FMA52788", "FMA52789"],
    "temporal": ["FMA52738", "FMA52739"],
    "occipital": ["FMA52735"],
    "esfenoides": ["FMA52736"],
    "etmoides": ["FMA52740"],
    "nasal": ["FMA53647", "FMA53648"],
    "maxilar": ["FMA53649", "FMA53650"],
    "mandibula": ["FMA52748"],
    "cigomatico": ["FMA52892", "FMA52893"],
    "lagrimal": ["FMA53645", "FMA53646"],
    "palatino": ["FMA53655", "FMA53656"],
    "vomer": ["FMA9710"],
    "cornetes": ["FMA54737", "FMA54738"],
}

BONE_COLOR = [232, 220, 196, 255]  # ivory/cream, tono óseo mate

# Los datos de BodyParts3D vienen en Z-up; glTF/model-viewer/three.js asumen Y-up.
# Rotamos -90 grados en X para que el eje superior-inferior anatómico sea Y (vertical).
UP_AXIS_FIX = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])


def to_yup(mesh):
    mesh.apply_transform(UP_AXIS_FIX)
    return mesh


def download(fma):
    os.makedirs(STL_CACHE, exist_ok=True)
    dest = os.path.join(STL_CACHE, fma + ".stl")
    if not os.path.exists(dest):
        print("downloading", fma)
        urllib.request.urlretrieve(BASE_URL.format(fma), dest)
    return dest


def load(fma):
    return trimesh.load(download(fma), force="mesh")


def safe_decimate(mesh, target_faces):
    try:
        if len(mesh.faces) > target_faces:
            return mesh.simplify_quadric_decimation(face_count=target_faces)
    except Exception as e:
        print("  decimation failed, keeping original:", e)
    return mesh


def colorize(mesh):
    mesh.visual = trimesh.visual.ColorVisuals(mesh, face_colors=BONE_COLOR)
    return mesh


def build_individual_models():
    print("\n=== Modelos individuales (glosario) ===")
    os.makedirs(OUT_BONES_DIR, exist_ok=True)
    for key, fmas in FMA_MAP.items():
        parts = [load(f) for f in fmas]
        combined = trimesh.util.concatenate(parts) if len(parts) > 1 else parts[0]
        to_yup(combined)
        combined.apply_translation(-combined.centroid)
        combined = safe_decimate(combined, 14000)
        colorize(combined)
        out_path = os.path.join(OUT_BONES_DIR, f"{key}.glb")
        combined.export(out_path)
        print(key, "->", round(os.path.getsize(out_path) / 1024, 1), "KB")


def build_full_skull():
    print("\n=== Cráneo completo ensamblado (juego) ===")
    all_parts = []
    for key, fmas in FMA_MAP.items():
        parts = [load(f) for f in fmas]
        for p in parts:
            to_yup(p)
        primary = safe_decimate(parts[0].copy(), 5000)
        meshes_for_key = [primary] + [safe_decimate(p.copy(), 5000) for p in parts[1:]]
        all_parts.append((key, meshes_for_key, parts[0]))

    all_vertices = np.vstack([p.vertices for _, meshes, _ in all_parts for p in meshes])
    global_center = all_vertices.mean(axis=0)

    scene = trimesh.Scene()
    hotspots = {}
    for key, meshes, primary_raw in all_parts:
        for i, m in enumerate(meshes):
            m.apply_translation(-global_center)
            colorize(m)
            scene.add_geometry(m, node_name=f"{key}_{i}")
        hotspots[key] = tuple(round(v, 2) for v in (primary_raw.centroid - global_center))

    os.makedirs(os.path.dirname(OUT_SKULL), exist_ok=True)
    scene.export(OUT_SKULL)
    print("skull_full.glb ->", round(os.path.getsize(OUT_SKULL) / 1024, 1), "KB")
    print("\nCoordenadas para app/data/bones.py (marker3d):")
    for key, xyz in hotspots.items():
        print(f"  {key}: {xyz}")


if __name__ == "__main__":
    build_individual_models()
    build_full_skull()
