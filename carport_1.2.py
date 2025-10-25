import FreeCAD, Part, math
import FreeCADGui
import time

# =============== PARAMÈTRES ET CHEMINS ===============
export_step = "carport_final.step"
export_png  = "carport_final.png"

# Dimensions générales
length = 5400           # mm total (entre piliers extrêmes)
width  = 3100           # mm total
height_front = 2200     # mm (poteaux avant, plus bas)
height_back  = 2600     # mm (poteaux arrière, plus haut, donne la pente)
pole_size    = 120      # mm

# Modules PV
module_length   = 1755  # mm
module_width    = 1038  # mm
module_thickness= 35    # mm
modules_x       = 3
modules_y       = 2

# Calcul automatique des gaps pour couverture parfaite, syntaxe corrigée
gap_x = (length - modules_x * module_length) / (modules_x - 1) if modules_x > 1 else 0
gap_y = (width - modules_y * module_width) / (modules_y - 1) if modules_y > 1 else 0

support_width  = 60     # mm
support_height = 40     # mm
rail_section   = 80     # mm

# Pente du toit calculée automatiquement
height_delta = height_back - height_front
roof_angle_rad = math.atan(height_delta / width)
roof_angle_deg = math.degrees(roof_angle_rad)

doc = FreeCAD.newDocument("CarportSolaireFinal")

# ========== 1. Création des piliers ==========
# 3 piliers devant, 3 derrière
for i in range(3):
    # Début (avant)
    x = i * (length - pole_size) / (2)
    y = 0
    pole = Part.makeBox(pole_size, pole_size, height_front, FreeCAD.Vector(x, y, 0))
    obj = Part.show(pole)
    obj.ViewObject.ShapeColor = (0.65,0.65,0.67)
    # Fin (arrière)
    yb = width - pole_size
    poleb = Part.makeBox(pole_size, pole_size, height_back, FreeCAD.Vector(x, yb, 0))
    objb = Part.show(poleb)
    objb.ViewObject.ShapeColor = (0.65,0.65,0.67)

# ========== 2. Rails principaux (avant/arrière : frame) ==========
# Rail avant (horizontal)
rail_f = Part.makeBox(length, rail_section, rail_section, FreeCAD.Vector(0, 0, height_front - rail_section))
obj = Part.show(rail_f); obj.ViewObject.ShapeColor = (0.4,0.4,0.45)
# Rail arrière (horizontal, haut selon pente)
rail_b = Part.makeBox(length, rail_section, rail_section, FreeCAD.Vector(0, width - rail_section, height_back - rail_section))
obj = Part.show(rail_b); obj.ViewObject.ShapeColor = (0.4,0.4,0.45)

# ========== 3. Traverses inclinées (cadre sous les panneaux) ==========
for i in range(3):
    x = i * (length - rail_section) / 2
    # Points départ et arrivé sur rail avant/arrière
    pt1 = FreeCAD.Vector(x + rail_section/2, rail_section, height_front)
    pt2 = FreeCAD.Vector(x + rail_section/2, width - rail_section, height_back)
    # Barre inclinée reliant avant-arrière (frame sous modules)
    bar = Part.makeBox(rail_section, width - 2*rail_section, rail_section, FreeCAD.Vector(x, rail_section, height_front - rail_section/2))
    # Inclinaison : rotation autour axe X pour suivre pente
    angle = roof_angle_deg
    center = FreeCAD.Vector(x + rail_section/2, rail_section, height_front)
    bar.rotate(center, FreeCAD.Vector(1,0,0), angle)
    obj = Part.show(bar)
    obj.ViewObject.ShapeColor = (0.45,0.47,0.53)

# ========== 4. Modules PV + supports (posés sur le frame incliné) ==========
module_num = 1
for j in range(modules_y):
    for i in range(modules_x):
        x = i * (module_length + gap_x)
        y = j * (module_width  + gap_y)
        # Vérification bord droit/bas
        assert x + module_length <= length + 1e-6, f"Module {i+1} dépasse en X"
        assert y + module_width  <= width  + 1e-6, f"Module {j+1} dépasse en Y"
        # Base Z du module (pente, position médiane)
        y_center = y + module_width/2
        z_base = height_front + y_center * (height_delta/width)
        # Supports sous le module (frame) – ici pour effet structurel, on pose sur le cadre
        for fx, fy in [(0.1,0.1),(0.9,0.1),(0.1,0.9),(0.9,0.9)]:
            sx = x + fx*module_length - support_width/2
            sy = y + fy*module_width  - support_width/2
            z_sup = height_front + (sy)*(height_delta/width)
            sup = Part.makeBox(support_width, support_width, support_height,
                               FreeCAD.Vector(sx, sy, z_sup))
            obj = Part.show(sup)
            obj.ViewObject.ShapeColor = (0.4,0.4,0.42)
        # Module PV posé sur le frame incliné
        z_mod = z_base + support_height
        mod = Part.makeBox(module_length, module_width, module_thickness,
                           FreeCAD.Vector(x, y, z_mod))
        center = FreeCAD.Vector(x+module_length/2, y+module_width/2, z_mod)
        mod.rotate(center, FreeCAD.Vector(1,0,0), roof_angle_deg)
        obj = Part.show(mod)
        obj.ViewObject.ShapeColor = (0.03,0.08,0.28)
        module_num += 1

# ========== 5. Export STEP & PNG ==========
Part.export(doc.Objects, export_step)

if FreeCAD.GuiUp:
    view = FreeCADGui.activeDocument().activeView()
    view.viewIsometric()
    view.fitAll()
    time.sleep(1)
    view.saveImage(export_png, 2560, 1440, "White")

FreeCAD.closeDocument(doc.Name)
FreeCADGui.getMainWindow().close()
