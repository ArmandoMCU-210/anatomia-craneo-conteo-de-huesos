# Contenido extraído de Anatomia_Craneo_Cerebro.docx (huesos del neurocráneo y del viscerocráneo).
# "region_id"/"marker3d" solo existen para los huesos visibles en una vista lateral externa del
# cráneo; el resto (etmoides, vómer, palatinos, cornetes) son internos y solo se muestran en el
# glosario (con su propio modelo 3D, pero sin punto interactivo en el juego).
#
# Los modelos 3D (app/static/models/) provienen de BodyParts3D/Anatomography (The Database
# Center for Life Science, Japón), licenciados bajo CC BY-SA 2.1 Japón. Fueron descargados,
# decimados y reensamblados con scripts/build_bone_models.py — ver ese script y el pie de
# página de la app para la atribución completa.

BONES = {
    "frontal": {
        "name": "Hueso frontal",
        "category": "neurocraneo",
        "region_id": "frontal",
        "marker3d": (0.15, 55.3, 27.9),
        "description": (
            "Hueso impar y medio situado en la parte anterior y superior del cráneo. "
            "Forma la frente, el techo de las órbitas oculares y parte de las fosas nasales. "
            "En su interior contiene los senos frontales, cavidades neumáticas que aligeran su peso."
        ),
        "function": "Protege los lóbulos frontales del cerebro y sirve de soporte óseo a la frente y a las cejas.",
    },
    "parietal": {
        "name": "Huesos parietales",
        "category": "neurocraneo",
        "region_id": "parietal",
        "marker3d": (-42.8, 70.4, -61.3),
        "description": (
            "Huesos pares, de forma cuadrangular, ubicados en las porciones laterales y superior del "
            "cráneo. Se articulan entre sí en la línea media mediante la sutura sagital, y con el hueso "
            "frontal a través de la sutura coronal."
        ),
        "function": "Forman la mayor parte de la bóveda craneal y protegen los lóbulos parietales del cerebro.",
    },
    "temporal": {
        "name": "Huesos temporales",
        "category": "neurocraneo",
        "region_id": "temporal",
        "marker3d": (-49.0, -0.9, -32.8),
        "description": (
            "Huesos pares situados en las porciones laterales e inferiores del cráneo. Se dividen en "
            "varias porciones (escamosa, timpánica, mastoidea y petrosa) y alojan las estructuras del "
            "oído medio e interno."
        ),
        "function": (
            "Protegen los lóbulos temporales del cerebro, alojan el aparato auditivo y vestibular, "
            "y se articulan con la mandíbula formando la articulación temporomandibular."
        ),
    },
    "occipital": {
        "name": "Hueso occipital",
        "category": "neurocraneo",
        "region_id": "occipital",
        "marker3d": (0.0, -1.3, -89.3),
        "description": (
            "Hueso impar situado en la parte posterior e inferior del cráneo. Presenta un orificio "
            "amplio, el foramen magno, a través del cual el encéfalo se continúa con la médula espinal."
        ),
        "function": (
            "Protege el cerebelo y el tronco encefálico, y permite la comunicación entre el cráneo "
            "y la columna vertebral a través del foramen magno."
        ),
    },
    "esfenoides": {
        "name": "Hueso esfenoides",
        "category": "neurocraneo",
        "region_id": "sphenoid",
        "marker3d": (0.13, 2.8, 0.65),
        "description": (
            "Hueso impar de forma irregular, comparado tradicionalmente con una mariposa con las alas "
            "extendidas, situado en la base del cráneo. Se articula prácticamente con todos los demás "
            "huesos craneales."
        ),
        "function": "Actúa como pieza clave de unión de la base craneal y aloja a la glándula hipófisis en la silla turca.",
    },
    "etmoides": {
        "name": "Hueso etmoides",
        "category": "neurocraneo",
        "region_id": None,
        "marker3d": None,
        "description": (
            "Hueso impar de estructura ligera y esponjosa, situado entre las órbitas oculares, por "
            "delante del esfenoides. Forma parte del techo de las fosas nasales y del tabique nasal. "
            "No es visible desde una vista lateral externa del cráneo."
        ),
        "function": (
            "Contribuye a la formación de las fosas nasales y las órbitas, y participa en el sentido "
            "del olfato al alojar la lámina cribosa, por donde pasan los filetes del nervio olfatorio."
        ),
    },
    "nasal": {
        "name": "Huesos nasales",
        "category": "viscerocraneo",
        "region_id": "nasal",
        "marker3d": (-3.6, 2.2, 59.0),
        "description": (
            "Pequeños huesos pares y alargados situados en la línea media del rostro, entre los "
            "procesos frontales de los maxilares."
        ),
        "function": "Forman el puente óseo de la nariz y sirven de sostén a los cartílagos nasales.",
    },
    "maxilar": {
        "name": "Huesos maxilares",
        "category": "viscerocraneo",
        "region_id": "maxilla",
        "marker3d": (-18.1, -25.5, 36.2),
        "description": (
            "Huesos pares de gran tamaño que constituyen la mandíbula superior. Contienen los alveolos "
            "dentales superiores y los senos maxilares."
        ),
        "function": (
            "Sostienen los dientes superiores, forman gran parte del paladar duro, el piso de las "
            "órbitas y las paredes laterales de las fosas nasales."
        ),
    },
    "mandibula": {
        "name": "Mandíbula",
        "category": "viscerocraneo",
        "region_id": "mandible",
        "marker3d": (-0.03, -53.1, 11.6),
        "description": (
            "Hueso impar y el único móvil del cráneo, ya que se articula con los huesos temporales "
            "mediante la articulación temporomandibular. Presenta un cuerpo horizontal y dos ramas "
            "verticales."
        ),
        "function": (
            "Sostiene los dientes inferiores y permite los movimientos de apertura, cierre y "
            "lateralidad necesarios para la masticación y el habla."
        ),
    },
    "cigomatico": {
        "name": "Huesos cigomáticos",
        "category": "viscerocraneo",
        "region_id": "zygomatic",
        "marker3d": (-45.5, -7.8, 25.5),
        "description": (
            "Conocidos comúnmente como huesos malares, son huesos pares de forma irregular situados "
            "en la parte lateral y superior de la cara."
        ),
        "function": "Forman la prominencia de los pómulos y completan la pared lateral e inferior de la órbita.",
    },
    "lagrimal": {
        "name": "Huesos lagrimales",
        "category": "viscerocraneo",
        "region_id": "lacrimal",
        "marker3d": (-22.0, -10.0, 30.0),
        "description": (
            "Son los huesos más pequeños y delicados de la cara, ubicados en la pared medial de cada "
            "órbita."
        ),
        "function": "Forman parte de la pared interna de la órbita y alojan el conducto nasolagrimal, por el cual drenan las lágrimas hacia la fosa nasal.",
    },
    "palatino": {
        "name": "Huesos palatinos",
        "category": "viscerocraneo",
        "region_id": None,
        "marker3d": None,
        "description": (
            "Huesos pares de forma irregular, situados en la parte posterior de las fosas nasales, "
            "entre los maxilares y las apófisis pterigoides del esfenoides. No son visibles desde una "
            "vista lateral externa."
        ),
        "function": "Completan la porción posterior del paladar duro y contribuyen a la formación del piso de las fosas nasales y de las órbitas.",
    },
    "vomer": {
        "name": "Vómer",
        "category": "viscerocraneo",
        "region_id": None,
        "marker3d": None,
        "description": (
            "Hueso impar y delgado, de forma cuadrangular, situado en la línea media de las fosas "
            "nasales. No es visible desde una vista lateral externa."
        ),
        "function": "Forma la porción posteroinferior del tabique nasal, junto con la lámina perpendicular del etmoides.",
    },
    "cornetes": {
        "name": "Cornetes nasales inferiores",
        "category": "viscerocraneo",
        "region_id": None,
        "marker3d": None,
        "description": (
            "Huesos pares curvos y alargados, ubicados en las paredes laterales de las fosas nasales, "
            "por debajo de los cornetes medio y superior del etmoides. No son visibles desde una vista "
            "lateral externa."
        ),
        "function": "Aumentan la superficie de la mucosa nasal, favoreciendo la filtración, humidificación y calentamiento del aire inspirado.",
    },
}

# Huesos usados como objetivos interactivos del juego (visibles en la vista lateral).
INTERACTIVE_KEYS = [key for key, data in BONES.items() if data["region_id"]]

# region_id (nombre del hotspot 3D) -> clave del hueso, para validar respuestas en el servidor.
REGION_TO_KEY = {BONES[key]["region_id"]: key for key in INTERACTIVE_KEYS}

CATEGORY_LABELS = {
    "neurocraneo": "Neurocráneo",
    "viscerocraneo": "Viscerocráneo",
}

# Modelos 3D (.glb) en app/static/models/. Cada hueso (incluidos los internos, solo para el
# glosario) tiene su propio modelo individual recentrado; además existe un cráneo completo
# ensamblado (SKULL_MODEL_FILENAME) con los hotspots del juego ya alineados a esa misma escena.
BONES_MODELS_DIR = "models/bones"
SKULL_MODEL_FILENAME = "models/skull_full.glb"

for _key in BONES:
    BONES[_key]["model"] = f"{_key}.glb"
del _key
