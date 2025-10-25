import FreeCAD, Part

# -----------------------------
# PARAMÈTRES CARPORT
# -----------------------------
length = 5000         # Longueur totale en mm
width = 3000          # Largeur totale en mm
height = 2400         # Hauteur sous toit en mm
pole_size = 120       # Section poteaux carrés mm
rail_size = 80        # Section rails mm
roof_thickness = 40   # Épaisseur toit mm
overhang = 250        # Dépassement du toit sur chaque côté mm
roof_offset = 30      # Toit posé au-dessus des rails mm

export_path_step = "carport_professionnel.step"
export_path_png  = "carport_professionnel.png"

doc = FreeCAD.newDocument("CarportPro")

# -----------------------------
# 1. Poteaux (4 coins)
# -----------------------------
poles = []
for i in range(2):
    for j in range(2):
        x = i * (length - pole_size)
        y = j * (width - pole_size)
        pole = Part.makeBox(pole_size, pole_size, height, FreeCAD.Vector(x, y, 0))
        poles.append(pole)
        obj = Part.show(pole)
        obj.ViewObject.ShapeColor = (0.7, 0.7, 0.7)

# -----------------------------
# 2. Rails longitudinaux (avant/arrière)
# -----------------------------
for i in range(2):
    y = i * (width - rail_size)
    rail = Part.makeBox(length, rail_size, rail_size, FreeCAD.Vector(0, y, height - rail_size))
    obj = Part.show(rail)
    obj.ViewObject.ShapeColor = (0.4, 0.4, 0.4)

# -----------------------------
# 3. Rails latéraux (gauche/droite)
# -----------------------------
for i in range(2):
    x = i * (length - rail_size)
    rail = Part.makeBox(rail_size, width, rail_size, FreeCAD.Vector(x, 0, height - rail_size))
    obj = Part.show(rail)
    obj.ViewObject.ShapeColor = (0.4, 0.4, 0.4)

# -----------------------------
# 4. Toit avec débords
# -----------------------------
roof_length = length + 2*overhang
roof_width = width + 2*overhang
roof = Part.makeBox(roof_length, roof_width, roof_thickness,
                    FreeCAD.Vector(-overhang, -overhang, height + roof_offset))
roof_obj = Part.show(roof)
roof_obj.ViewObject.ShapeColor = (0.2, 0.2, 0.2)

# -----------------------------
# 5. Export STEP
# -----------------------------
carport_objects = doc.Objects
Part.export(carport_objects, export_path_step)
print(f"Carport exporté au format STEP : {export_path_step}")

# -----------------------------
# 6. Export Image PNG (vue isométrique, fond blanc)
# -----------------------------
import FreeCADGui
if FreeCAD.GuiUp:
    from time import sleep
    view = FreeCADGui.activeDocument().activeView()
    view.viewIsometric()
    view.fitAll()
    # Petite pause pour s'assurer que la vue est à jour
    sleep(1)
    view.saveImage(export_path_png, 1920, 1080, 'White')
    print(f"Image PNG exportée : {export_path_png}")
else:
    print("Impossible d’exporter une image sans interface graphique (FreeCADGui)")
#FreeCAD.closeDocument("CarportPro")
#FreeCADGui.getMainWindow().close()
# -----------------------------
# Notes d’utilisation
# -----------------------------
# 1. Change export_path_* selon ton dossier
# 2. Lance la macro depuis l’interface graphique de FreeCAD (sinon PNG impossible)
# 3. La vue est automatiquement placée en isométrique, fond blanc, résolution HD
# 4. Le STEP est exporté pour utilisation CAO, plans ou import Odoo


FreeCAD.closeDocument(doc.Name)
FreeCADGui.getMainWindow().close()
