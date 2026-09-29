# 📐 Modelo 3D Paramétrico: Cubierta Toldo Aluminio

## 📋 Contenido Entregado

### 1. **Cubierta_Toldo.FCMacro** 
Archivo de macro para FreeCAD (Python script completo)
- Estructura de aluminio RAL 7016 (perfil 80×80 mm)
- Paneles sándwich blanco/blanco (40 mm espesor)
- Totalmente paramétrico (modificar dimensiones fácilmente)
- Grupos organizados: PILARES, VIGAS, TRAVESAÑOS, PANELES_SANDWICH

### 2. **visualizar_modelo_3d.py**
Script Python independiente para visualizar el modelo sin FreeCAD
- Genera una vista 3D isométrica
- Exporta automáticamente a PNG
- Utiliza matplotlib

### 3. **modelo_3d_cubierta.png**
Visualización previa en 3D del modelo (isométrica 45°)

---

## 🚀 Cómo Usar en FreeCAD

### Opción A: Desde FreeCAD GUI
1. Abre **FreeCAD**
2. Ve a **Macro → Crear macro nueva** (o Edit → Preferences → Macro)
3. Copia y pega el contenido de `Cubierta_Toldo.FCMacro`
4. Presiona **Ejecutar** (botón verde ▶ o Ctrl+E)
5. El modelo se generará automáticamente en el árbol del documento

### Opción B: Directamente desde archivo
1. Abre FreeCAD
2. Ve a **Macro → Ejecutar macro**
3. Selecciona el archivo `Cubierta_Toldo.FCMacro`
4. El modelo se cargará en un nuevo documento

### Opción C: Línea de comandos (Linux/Mac)
```bash
freecad Cubierta_Toldo.FCMacro
```

---

## 🔧 Parámetros del Modelo

Al inicio del script, tienes estas variables que puedes modificar:

```python
# Dimensiones generales [mm]
ANCHO = 3300              # Ancho frontal (eje Y)
LARGO = 6380              # Largo principal (eje X)
ALTURA_FRONTAL = 2500     # Altura pilar frontal
ALTURA_TRASERA = 2900     # Altura pilar trasero
ANCHO_INTERIOR = 2660     # Ancho útil interior (para referencia)

# Estructura
PERFIL = 80               # Perfil cuadrado aluminio: 80×80 mm
ESPESOR_PANEL = 40        # Espesor panel sándwich [mm]

# Separación
ESPACIADO_TRANSVERSAL = 1000  # Separación entre travesaños [mm]

# Colores (RGB 0-1)
COLOR_ALUMINIO = (0.5, 0.5, 0.5)    # Gris antracita RAL 7016
COLOR_PANEL = (1.0, 1.0, 1.0)       # Blanco
```

---

## 📐 Interpretación del Croquis Original

Basándome en el croquis manuscrito, el modelo incluye:

### ✅ Estructura Identificada:
- **Ancho frontal**: 3300 mm (línea superior del toldo)
- **Largo**: 6380 mm (opción principal) / 6700 mm (alternativa)
- **Altura frontal**: 2500 mm (pilares delanteros)
- **Altura trasera**: 2900 mm (pilares traseros)
- **Pendiente**: 400 mm (altura aumenta hacia atrás)
- **Perfil estructural**: 80 × 80 mm (aluminio RAL 7016)
- **Panel sándwich**: 40 mm (blanco/blanco)
- **2660 mm**: Conservado como ANCHO_INTERIOR (ancho útil entre pilares)

### 🤔 Ambigüedades Preservadas:
1. **Largo**: Variable LARGO permite cambiar entre 6380 y 6700 mm sin reconstruir
2. **Cota 2660 mm**: Incluida como parámetro separado para clarificaciones futuras
3. **Altura trasera**: Rango 2800-3000 mm → usamos 2900 mm como estándar (ajustable)

---

## 🛠 Estructura del Modelo Generado

### Grupos en FreeCAD:
```
ESTRUCTURA_ALUMINIO
├── PILARES (4 esquinas + intermedios cada 1000 mm)
│   ├── Pilar_Frontal_Izquierdo
│   ├── Pilar_Frontal_Derecho
│   ├── Pilar_Trasero_Izquierdo
│   ├── Pilar_Trasero_Derecho
│   ├── Pilar_Intermedio_1_Izquierdo
│   ├── Pilar_Intermedio_1_Derecho
│   └── ... (según LARGO)
├── VIGAS
│   ├── Viga_Longitudinal_Inferior_Izquierda
│   ├── Viga_Longitudinal_Inferior_Derecha
│   ├── Viga_Delantera_Superior
│   └── Viga_Trasera_Superior
├── TRAVESANOS
│   ├── Travesano_00
│   ├── Travesano_01
│   └── ... (cada 1000 mm)
└── PANELES_SANDWICH (múltiples paneles con pendiente)
    ├── Panel_00
    ├── Panel_01
    ├── Panel_Encuentro_Edificio
    └── ...
```

---

## 📝 Cómo Modificar el Modelo

### Ejemplo 1: Cambiar largo a 6700 mm
```python
LARGO = 6700  # en lugar de 6380
```
Guarda, ejecuta nuevamente, y el modelo se regenerará automáticamente con todos los travesaños ajustados.

### Ejemplo 2: Aumentar la pendiente
```python
ALTURA_TRASERA = 3200  # en lugar de 2900
```
La diferencia 3200 - 2500 = 700 mm de pendiente (fue 400 mm antes).

### Ejemplo 3: Cambiar espaciado de travesaños
```python
ESPACIADO_TRANSVERSAL = 1500  # en lugar de 1000 mm
```
Ahora los travesaños se distribuyen cada 1500 mm en lugar de 1000 mm.

---

## 🎨 Colores y Acabados

- **Estructura de aluminio**: RGB (0.5, 0.5, 0.5) → Gris antracita (RAL 7016)
- **Paneles sándwich**: RGB (1.0, 1.0, 1.0) → Blanco
- **Bordes**: Negro fino para definición

Para cambiar colores, edita:
```python
COLOR_ALUMINIO = (0.5, 0.5, 0.5)   # RGB para aluminio
COLOR_PANEL = (1.0, 1.0, 1.0)      # RGB para paneles
```

---

## 💾 Exportación desde FreeCAD

Una vez generado el modelo en FreeCAD, puedes exportarlo a:

- **STEP** (.step) - Para importar en otros CAD
- **STL** (.stl) - Para impresión 3D
- **IGES** (.iges) - Compatible general
- **PDF 3D** - Para visualización

**Pasos**:
1. Click derecho en el grupo `ESTRUCTURA_ALUMINIO`
2. **File → Export as → [formato deseado]**

---

## ⚠️ Notas Importantes

### Parámetros No Independientes:
- Los pilares intermedios se generan automáticamente cada `ESPACIADO_TRANSVERSAL` mm
- Las alturas se **interpolan linealmente** entre frontal y trasera
- Los paneles siguen automáticamente la pendiente de la cubierta

### Precisión:
- Todas las dimensiones están en **milímetros (mm)** en el código
- El modelo escala correctamente en FreeCAD (1 unidad = 1 mm)

### Rendimiento:
- En equipos estándar, el modelo se genera en **< 2 segundos**
- Si experimentas lentitud, reduce `ESPACIADO_TRANSVERSAL` a 1500 o 2000 mm

---

## 🔍 Validación del Modelo

Para verificar que el modelo es correcto:

1. **Medidas**: En FreeCAD, selecciona dos vértices y mide la distancia (Tools → Measure)
2. **Volúmenes**: Click derecho en objeto → Properties → Volume
3. **Pendiente**: Compara altura trasera - altura frontal (debe ser ALTURA_TRASERA - ALTURA_FRONTAL)

---

## 📞 Ayuda Rápida

### El modelo no aparece
- Verifica que el documento esté activo (`doc.recompute()` al final del script)
- Recalcula manualmente: **Edit → Refresh** o **F5**

### Los colores no se ven
- FreeCAD a veces necesita recargar la vista: **View → Fit All** (V, F)

### Cambios no se aplican
- Borra todos los objetos (`Edit → Delete All`)
- Ejecuta nuevamente la macro

---

## 📊 Resumen de Dimensiones Clave

| Parámetro | Valor Estándar | Rango Recomendado | Unidad |
|-----------|----------------|-------------------|--------|
| ANCHO | 3300 | 2500-4000 | mm |
| LARGO | 6380 | 6000-7000 | mm |
| ALTURA_FRONTAL | 2500 | 2000-3000 | mm |
| ALTURA_TRASERA | 2900 | 2500-3500 | mm |
| PERFIL | 80 | 60-100 | mm |
| ESPESOR_PANEL | 40 | 30-50 | mm |
| ESPACIADO_TRANSVERSAL | 1000 | 800-1500 | mm |

---

## 🎯 Próximos Pasos

1. **Ejecutar el script** en FreeCAD con los parámetros estándar
2. **Validar el modelo** contra el croquis original
3. **Ajustar dimensiones** si es necesario
4. **Exportar** en el formato que necesites (STEP, STL, etc.)
5. **Compartir** con tu equipo de diseño o fabricación

---

**Creado con**: Python 3 + FreeCAD Python API  
**Fecha**: 2026-09-29  
**Versión**: 1.0 (Modelo base paramétrico)
