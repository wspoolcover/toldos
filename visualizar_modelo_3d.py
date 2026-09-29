#!/usr/bin/env python3
"""
Visualización 3D del modelo de cubierta toldo en matplotlib
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# ============================================================================
# PARÁMETROS
# ============================================================================

ANCHO = 3300              # Ancho frontal (eje Y) [mm]
LARGO = 6380              # Largo principal (eje X) [mm]
ALTURA_FRONTAL = 2500     # Altura pilar frontal [mm]
ALTURA_TRASERA = 2900     # Altura pilar trasero [mm]
PERFIL = 80               # Perfil cuadrado [mm]
ESPESOR_PANEL = 40        # Espesor panel sándwich [mm]

# Convertir a metros para visualización
ANCHO_M = ANCHO / 1000
LARGO_M = LARGO / 1000
ALTURA_FRONTAL_M = ALTURA_FRONTAL / 1000
ALTURA_TRASERA_M = ALTURA_TRASERA / 1000
PERFIL_M = PERFIL / 1000
ESPESOR_PANEL_M = ESPESOR_PANEL / 1000

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def crear_caja_3d(x, y, z, dx, dy, dz):
    """Crea los 8 vértices de una caja 3D."""
    return [
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz],
    ]

def caras_caja(vertices):
    """Retorna las 6 caras de una caja a partir de 8 vértices."""
    v = vertices
    return [
        [v[0], v[1], v[5], v[4]],  # Frente (X)
        [v[2], v[3], v[7], v[6]],  # Atrás (X)
        [v[0], v[3], v[7], v[4]],  # Izquierda (Y)
        [v[1], v[2], v[6], v[5]],  # Derecha (Y)
        [v[0], v[1], v[2], v[3]],  # Abajo (Z)
        [v[4], v[5], v[6], v[7]],  # Arriba (Z)
    ]

def interpolar_altura(x, x_total):
    """Interpola altura linealmente entre frontal y trasera."""
    return ALTURA_FRONTAL_M + (ALTURA_TRASERA_M - ALTURA_FRONTAL_M) * (x / x_total)

# ============================================================================
# CREAR FIGURA 3D
# ============================================================================

fig = plt.figure(figsize=(16, 10))
ax = fig.add_subplot(111, projection='3d')

poligonos_aluminio = []
poligonos_panel = []

# ============================================================================
# 1. PILARES
# ============================================================================

# Pilar frontal izquierdo
v = crear_caja_3d(0, 0, 0, PERFIL_M, PERFIL_M, ALTURA_FRONTAL_M)
poligonos_aluminio.extend(caras_caja(v))

# Pilar frontal derecho
v = crear_caja_3d(0, ANCHO_M - PERFIL_M, 0, PERFIL_M, PERFIL_M, ALTURA_FRONTAL_M)
poligonos_aluminio.extend(caras_caja(v))

# Pilar trasero izquierdo
v = crear_caja_3d(LARGO_M - PERFIL_M, 0, 0, PERFIL_M, PERFIL_M, ALTURA_TRASERA_M)
poligonos_aluminio.extend(caras_caja(v))

# Pilar trasero derecho
v = crear_caja_3d(LARGO_M - PERFIL_M, ANCHO_M - PERFIL_M, 0, PERFIL_M, PERFIL_M, ALTURA_TRASERA_M)
poligonos_aluminio.extend(caras_caja(v))

# Pilares intermedios
num_pilares_intermedios = int(LARGO / 1000) - 1
for i in range(1, num_pilares_intermedios + 1):
    x_pilar = (i * 1000) / 1000  # En metros
    if x_pilar < LARGO_M - PERFIL_M:
        altura_interp = interpolar_altura(x_pilar, LARGO_M)

        # Pilar izquierdo
        v = crear_caja_3d(x_pilar, 0, 0, PERFIL_M, PERFIL_M, altura_interp)
        poligonos_aluminio.extend(caras_caja(v))

        # Pilar derecho
        v = crear_caja_3d(x_pilar, ANCHO_M - PERFIL_M, 0, PERFIL_M, PERFIL_M, altura_interp)
        poligonos_aluminio.extend(caras_caja(v))

# ============================================================================
# 2. VIGAS LONGITUDINALES
# ============================================================================

# Viga inferior izquierda
v = crear_caja_3d(0, 0, ALTURA_FRONTAL_M - PERFIL_M, LARGO_M, PERFIL_M, PERFIL_M)
poligonos_aluminio.extend(caras_caja(v))

# Viga inferior derecha
v = crear_caja_3d(0, ANCHO_M - PERFIL_M, ALTURA_FRONTAL_M - PERFIL_M, LARGO_M, PERFIL_M, PERFIL_M)
poligonos_aluminio.extend(caras_caja(v))

# ============================================================================
# 3. TRAVESAÑOS TRANSVERSALES
# ============================================================================

num_travesanos = int(LARGO / 1000) + 1
for i in range(num_travesanos):
    x_pos = (i * 1000) / 1000  # En metros
    if x_pos <= LARGO_M:
        altura_en_pos = interpolar_altura(x_pos, LARGO_M)
        v = crear_caja_3d(x_pos, 0, altura_en_pos - PERFIL_M, PERFIL_M, ANCHO_M, PERFIL_M)
        poligonos_aluminio.extend(caras_caja(v))

# ============================================================================
# 4. VIGAS SUPERIORES (Perímetro)
# ============================================================================

# Viga delantera superior
v = crear_caja_3d(0, 0, ALTURA_FRONTAL_M, PERFIL_M, ANCHO_M, PERFIL_M)
poligonos_aluminio.extend(caras_caja(v))

# Viga trasera superior
v = crear_caja_3d(LARGO_M - PERFIL_M, 0, ALTURA_TRASERA_M, PERFIL_M, ANCHO_M, PERFIL_M)
poligonos_aluminio.extend(caras_caja(v))

# ============================================================================
# 5. PANELES SÁNDWICH (Cubierta)
# ============================================================================

num_paneles = int(LARGO / 1000)
for i in range(num_paneles):
    x_start = (i * 1000) / 1000
    x_end = ((i + 1) * 1000) / 1000

    h_start = interpolar_altura(x_start, LARGO_M)
    h_end = interpolar_altura(x_end, LARGO_M)

    if x_end > LARGO_M:
        x_end = LARGO_M - PERFIL_M

    # Cuatro vértices del panel (forma trapezoidall inclinada)
    vertices_panel = [
        [x_start, 0, h_start],                                        # Frontal-izquierda
        [x_start, ANCHO_M, h_start],                                  # Frontal-derecha
        [x_end, ANCHO_M, h_end + ESPESOR_PANEL_M],                    # Trasero-derecha
        [x_end, 0, h_end + ESPESOR_PANEL_M],                          # Trasero-izquierda
    ]
    poligonos_panel.append(vertices_panel)

# ============================================================================
# AGREGAR POLÍGONOS A LA GRÁFICA
# ============================================================================

# Aluminio (gris)
col_aluminio = Poly3DCollection(poligonos_aluminio, alpha=0.8, facecolor=(0.6, 0.6, 0.6), edgecolor='black', linewidths=0.5)
ax.add_collection3d(col_aluminio)

# Paneles (blanco)
col_panel = Poly3DCollection(poligonos_panel, alpha=0.9, facecolor=(1.0, 1.0, 1.0), edgecolor='gray', linewidths=1.0)
ax.add_collection3d(col_panel)

# ============================================================================
# CONFIGURAR VISTA 3D
# ============================================================================

# Establecer límites
ax.set_xlim(0, LARGO_M * 1.1)
ax.set_ylim(-0.5, ANCHO_M * 1.1)
ax.set_zlim(0, ALTURA_TRASERA_M * 1.2)

# Etiquetas
ax.set_xlabel('Largo (m)', fontsize=12, fontweight='bold')
ax.set_ylabel('Ancho (m)', fontsize=12, fontweight='bold')
ax.set_zlabel('Altura (m)', fontsize=12, fontweight='bold')
ax.set_title('CUBIERTA TOLDO - MODELO 3D\nAluminio RAL 7016 + Paneles Sándwich Blanco',
             fontsize=14, fontweight='bold', pad=20)

# Ángulo de vista (isométrico)
ax.view_init(elev=25, azim=45)

# Grid
ax.grid(True, alpha=0.3)

# ============================================================================
# AÑADIR INFORMACIÓN DE PARÁMETROS
# ============================================================================

info_text = f"""
DIMENSIONES PRINCIPALES:
• Ancho frontal: {ANCHO} mm ({ANCHO_M:.2f} m)
• Largo: {LARGO} mm ({LARGO_M:.2f} m)
• Altura frontal: {ALTURA_FRONTAL} mm ({ALTURA_FRONTAL_M:.2f} m)
• Altura trasera: {ALTURA_TRASERA} mm ({ALTURA_TRASERA_M:.2f} m)
• Pendiente: {ALTURA_TRASERA - ALTURA_FRONTAL} mm
• Perfil aluminio: {PERFIL}×{PERFIL} mm (RAL 7016)
• Espesor panel: {ESPESOR_PANEL} mm
"""

fig.text(0.02, 0.98, info_text, transform=fig.transFigure, fontsize=10,
         verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()

# Guardar como imagen
output_path = '/tmp/claude-0/-home-user-toldos/2ab7ff12-901a-5618-91e8-b6514acf56f0/scratchpad/modelo_3d_cubierta.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\n✓ Imagen guardada en: {output_path}")

try:
    plt.show()
except:
    pass

print("\n✓ Visualización 3D generada correctamente")
print(f"Modelo: Cubierta toldo {ANCHO}×{LARGO} mm con estructura de aluminio RAL 7016")
