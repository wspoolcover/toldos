"""Render realista con Blender (módulo bpy, Cycles CPU): materiales procedurales (ladrillo, enfoscado, hormigón, vidrio, acero, madera) sobre casa_v7.glb."""
import bpy, math, sys
import os; D = os.path.dirname(os.path.abspath(__file__)); GLB, OUT = os.path.join(D, "casa_v7.glb"), os.path.join(D, "render_")
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.samples = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 48
sc.cycles.device = "CPU"; sc.cycles.use_denoising = True; sc.render.resolution_x, sc.render.resolution_y = 1400, 950
sc.view_settings.view_transform = "AgX"

def mat(name, build):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); nt.links.new(bsdf.outputs[0], out.inputs[0])
    build(nt, bsdf); return m

def plaster_brick(nt, bsdf):                     # muros: ladrillo visto en el salón (y < 7,4) y enfoscado beige en la casa antigua
    pos = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(pos.outputs["Position"], sep.inputs[0])
    lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = 7.4; nt.links.new(sep.outputs["Y"], lt.inputs[0])
    brick = nt.nodes.new("ShaderNodeTexBrick"); brick.inputs["Scale"].default_value = 1.0; brick.inputs["Mortar Size"].default_value = 0.012
    brick.inputs["Color1"].default_value = (0.55, 0.26, 0.17, 1); brick.inputs["Color2"].default_value = (0.62, 0.33, 0.22, 1); brick.inputs["Mortar"].default_value = (0.75, 0.72, 0.66, 1)
    brick.inputs["Brick Width"].default_value = 0.24; brick.inputs["Row Height"].default_value = 0.07
    nt.links.new(pos.outputs["Position"], brick.inputs["Vector"])
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 18; cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = (0.80, 0.74, 0.62, 1); cr.color_ramp.elements[1].color = (0.90, 0.85, 0.74, 1); nt.links.new(noise.outputs["Fac"], cr.inputs[0])
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"; nt.links.new(lt.outputs[0], mix.inputs["Factor"]); nt.links.new(cr.outputs[0], mix.inputs["A"]); nt.links.new(brick.outputs["Color"], mix.inputs["B"])
    nt.links.new(mix.outputs["Result"], bsdf.inputs["Base Color"]); bsdf.inputs["Roughness"].default_value = 0.9
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.4; nt.links.new(brick.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs[0], bsdf.inputs["Normal"])

def solid(rgb, rough=0.6, metal=0.0, alpha=1.0):
    def b(nt, bsdf):
        bsdf.inputs["Base Color"].default_value = (*rgb, 1); bsdf.inputs["Roughness"].default_value = rough; bsdf.inputs["Metallic"].default_value = metal
        if alpha < 1: bsdf.inputs["Alpha"].default_value = alpha; bsdf.inputs["Transmission Weight"].default_value = 0.9; bsdf.inputs["Roughness"].default_value = 0.05
    return b

def wood(nt, bsdf):
    w = nt.nodes.new("ShaderNodeTexWave"); w.inputs["Scale"].default_value = 3; w.inputs["Distortion"].default_value = 4; cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = (0.45, 0.28, 0.14, 1); cr.color_ramp.elements[1].color = (0.65, 0.45, 0.26, 1); nt.links.new(w.outputs[0], cr.inputs[0]); nt.links.new(cr.outputs[0], bsdf.inputs["Base Color"]); bsdf.inputs["Roughness"].default_value = 0.5

def concrete(nt, bsdf):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 40; cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = (0.50, 0.50, 0.50, 1); cr.color_ramp.elements[1].color = (0.66, 0.66, 0.64, 1); nt.links.new(n.outputs["Fac"], cr.inputs[0]); nt.links.new(cr.outputs[0], bsdf.inputs["Base Color"]); bsdf.inputs["Roughness"].default_value = 0.95

MATS = {"muros": mat("muros", plaster_brick), "parapeto": mat("parapeto", plaster_brick), "forjado": mat("hormigon", concrete), "zuncho": mat("zuncho", concrete), "riostra": mat("riostra", concrete), "cimentacion": mat("cim", concrete),
        "tabique": mat("tabique", solid((0.93, 0.93, 0.90), 0.8)), "murete": mat("murete", solid((0.90, 0.88, 0.80), 0.8)), "escalera": mat("madera_esc", wood), "mobiliario": mat("madera", wood),
        "cristal": mat("vidrio", solid((0.75, 0.88, 0.95), alpha=0.25)), "lucernario": mat("vidrio2", solid((0.75, 0.88, 0.95), alpha=0.3)), "acero": mat("acero", solid((0.18, 0.25, 0.40), 0.45, 0.8)),
        "chimenea": mat("chimenea", solid((0.25, 0.14, 0.12), 0.7)), "paneles": mat("paneles", solid((0.05, 0.08, 0.18), 0.15, 0.3)), "aerotermia": mat("aero", solid((0.82, 0.82, 0.84), 0.4, 0.6))}
for ob in bpy.data.objects:
    if ob.type != "MESH": continue
    key = next((k for k in MATS if ob.name.lower().startswith(k)), None)
    if key: ob.data.materials.clear(); ob.data.materials.append(MATS[key])
    if ob.name.startswith("cimentacion") or ob.name.startswith("riostras"): ob.hide_render = True
# suelo, cielo y sol
bpy.ops.mesh.primitive_plane_add(size=80, location=(6, 8, -0.01)); g = bpy.context.object; g.data.materials.append(mat("suelo", solid((0.55, 0.47, 0.36), 0.95)))
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; sky = w.node_tree.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"; sky.sun_elevation = math.radians(48); sky.sun_rotation = math.radians(200); sky.sun_intensity = 0.5
w.node_tree.links.new(sky.outputs[0], w.node_tree.nodes["Background"].inputs[0]); w.node_tree.nodes["Background"].inputs[1].default_value = 0.06
bpy.ops.object.light_add(type="SUN", location=(0, 0, 20)); sun = bpy.context.object; sun.data.energy = 4.0; sun.rotation_euler = (math.radians(42), 0, math.radians(-25))
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co; cam.lens = 30

def shoot(name, loc, target, hide=()):
    for ob in bpy.data.objects:
        if ob.type == "MESH" and ob.name not in ("Plane",): ob.hide_render = any(ob.name.startswith(h) for h in hide) or ob.name.startswith(("cimentacion", "riostras"))
    co.location = loc; d = [t - l for t, l in zip(target, loc)]
    co.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]) if False else math.acos(-d[2] / math.sqrt(sum(x * x for x in d))), 0, math.atan2(d[1], d[0]) + math.pi / 2)
    sc.render.filepath = OUT + name + ".png"; bpy.ops.render.render(write_still=True); print("render", name)

shoot("exterior_norte", (-6, -14, 7), (5, 7, 2.5))
shoot("exterior_sur", (18, 24, 9), (5, 9, 2.5))
shoot("planta_baja_abierta", (-2, -4, 16), (5, 8.5, 0.5), hide=("muros_PA", "forjado_PB_PA", "forjado_salon", "forjado_cubierta", "parapeto", "lucernario", "tabiques_PA", "cristal_PA", "acero_vigas_cubierta", "zuncho_cubierta", "paneles", "acero_pilares"))
shoot("salon_interior", (5.2, 1.2, 1.6), (4.2, 7.5, 1.3), hide=("muros_PA", "forjado_cubierta", "parapeto", "lucernario", "tabiques_PA", "cristal_PA", "acero_vigas_cubierta", "zuncho_cubierta", "paneles"))
