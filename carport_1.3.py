"""
Carport Solar Structure Generator (FreeCAD Python Macro)
--------------------------------------------------------
This script generates a parametric carport structure for solar panels.

- Modular design: change number of modules (X and Y) for instant resizing.
- Creates vertical posts, carrier rails (main beams), aluminum frames, and photovoltaic panels.
- All geometry is adjustable: edit module dimensions and structural sizes as needed.

Exported file formats:
    STEP (.step) for CAD interoperability (SolidWorks, Archicad, etc.)
    PNG image for quick visualization

Author: [BOEHM Jean]
Date: [14-10-2025]
Usage: Run in FreeCAD Python console or as macro.
"""

import FreeCAD, Part, math
import FreeCADGui
import time

# === EXPORT SETTINGS ===
export_step = "carport_sans_supports.step"
export_png = "carport_sans_supports.png"





# === CARPORT CONFIGURATION ===
# CHANGE HERE THE NUMBER OF MODULES!
modules_x = 3  # Number of modules along X (length)
modules_y = 2  # Number of modules along Y (width)





# === MODULE & STRUCTURE DIMENSIONS (mm) ===
module_length    = 1800  # Solar panel length
module_width     = 1035  # Solar panel width
module_thickness = 40    # Solar panel thickness
frame_size       = 55    # Aluminum frame profile (width)
frame_height     = 50    # Aluminum frame profile (height)
pole_size        = 120   # Vertical post profile (square)
rail_size        = 60    # Carrier rail profile (height/width)

length = modules_x * module_length
width  = modules_y * module_width
height_base = 2200      # Height of lower edge (posts, rails, frame)

doc = FreeCAD.newDocument("CarportSansSupports")

# === 1. Generate Vertical Posts (Columns) ===
for i in range(modules_x):
    x = i * module_length + module_length/2 - pole_size/2
    # Front row
    Part.show(Part.makeBox(pole_size, pole_size, height_base,
            FreeCAD.Vector(x, 0, 0))).ViewObject.ShapeColor = (0.6,0.6,0.65)
    # Rear row
    Part.show(Part.makeBox(pole_size, pole_size, height_base,
            FreeCAD.Vector(x, width-pole_size, 0))).ViewObject.ShapeColor = (0.6,0.6,0.65)

# === 2. Generate Main Carrier Rails (Beams) ===
# Front and Rear rails
for y in [0, width-rail_size]:
    Part.show(Part.makeBox(length, rail_size, rail_size,
            FreeCAD.Vector(0, y, height_base-rail_size))).ViewObject.ShapeColor = (0.3,0.3,0.37)
# Left and Right rails
for x in [0, length-rail_size]:
    Part.show(Part.makeBox(rail_size, width, rail_size,
            FreeCAD.Vector(x, 0, height_base-rail_size))).ViewObject.ShapeColor = (0.24,0.27,0.35)

# === 3. Generate Aluminum Frame and PV Panels (for each module) ===
for j in range(modules_y):
    for i in range(modules_x):
        xmod = i * module_length
        ymod = j * module_width
        z_frame = height_base

        # Aluminum frame -- four profiles (rectangle)
        frame_front = Part.makeBox(module_length, frame_size, frame_height,
                    FreeCAD.Vector(xmod, ymod, z_frame))
        Part.show(frame_front).ViewObject.ShapeColor = (0.43,0.43,0.49)
        frame_back = Part.makeBox(module_length, frame_size, frame_height,
                    FreeCAD.Vector(xmod, ymod+module_width-frame_size, z_frame))
        Part.show(frame_back).ViewObject.ShapeColor = (0.43,0.43,0.49)
        for xr in [xmod, xmod+module_length-frame_size]:
            frame_side = Part.makeBox(frame_size, module_width, frame_height,
                          FreeCAD.Vector(xr, ymod, z_frame))
            Part.show(frame_side).ViewObject.ShapeColor = (0.43,0.43,0.49)

        # Photovoltaic panel placed just above aluminum frame
        z_pv = z_frame + frame_height
        pv = Part.makeBox(module_length, module_width, module_thickness,
                    FreeCAD.Vector(xmod, ymod, z_pv))
        Part.show(pv).ViewObject.ShapeColor = (0.16, 0.25, 0.42)  # Slightly lighter blue

# === 4. Export STEP file and PNG for CAD & visualization ===
Part.export(doc.Objects, export_step)
if FreeCAD.GuiUp:
    view = FreeCADGui.activeDocument().activeView()
    view.viewAxonometric(); view.fitAll()
    time.sleep(1)
    view.saveImage(export_png, 2560, 1440, "White")
FreeCAD.closeDocument(doc.Name)
FreeCADGui.getMainWindow().close()
