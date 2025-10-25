# cad_automation

A set of FreeCAD Python macros to generate parametric carport structures — including frames, posts, rails, and photovoltaic (PV) module layouts — and export STEP and PNG outputs for CAD and visualization.

These scripts are small, editable macros intended to speed up repetitive CAD tasks for carport / solar canopy layouts by exposing a few top-level parameters (dimensions, module counts, profile sizes). They are designed to be run inside the FreeCAD environment.

---

## Contents

- `carport_1.1.py` — Simple professional carport generator (4 posts, rails, overhanging roof). Exports STEP + PNG (PNG only when run in FreeCAD GUI).  
  Source: https://github.com/jboehm1/cad_automation/blob/36296d12cec608c064d3245c3f8dff2934677734/carport_1.1.py

- `carport_1.2.py` — More advanced solar carport with pitched roof, supports and PV modules (3×2 example). Exports STEP + PNG and demonstrates automatic roof angle & module gaps.  
  Source: https://github.com/jboehm1/cad_automation/blob/36296d12cec608c064d3245c3f8dff2934677734/carport_1.2.py

- `carport_1.3.py` — Parametric carport generator focused on module framing (modules_x/modules_y variables). Generates posts, carrier rails, aluminum frames and PV panels. Exports STEP + PNG.  
  Source: https://github.com/jboehm1/cad_automation/blob/36296d12cec608c064d3245c3f8dff2934677734/carport_1.3.py

---

## Features

- Parametric dimensions for quick layout changes (length, width, heights, profile sizes, module counts)
- Automatic module gap calculation and roof slope (in some versions)
- Export STEP files for CAD interoperability
- PNG rendering for visualization when run with FreeCAD GUI
- Minimal, easy-to-read code intended as a starting point for customization

---

## Requirements

- FreeCAD (tested with FreeCAD Python API)
- The scripts use modules from the FreeCAD distribution: `FreeCAD`, `Part`, and optionally `FreeCADGui`.
- To generate PNG images, run the script inside the FreeCAD GUI (because `FreeCADGui` is required). If running headless (command-line FreeCAD), the PNG export will not work unless the script is adapted to skip GUI calls.

---

## Quick usage

1. Open FreeCAD (GUI).
2. Open the Python console or use Tools → Macros → Create.
3. Paste the contents of one of the `carport_*.py` files into a macro and run it.

Run from command line, example:
´´´/Applications/FreeCAD.app/Contents/MacOS/FreeCAD /Users/jeanb/Documents/code/simple_cad/carport_1.1.py
´´´

Example: run as macro
```text
Tools → Macros → Create → paste script → Execute
```

Run from FreeCAD Python console:
```python
# In FreeCAD's Python console
exec(open('/path/to/carport_1.3.py').read())
```

Notes:
- If a script calls `FreeCADGui` and `FreeCAD.GuiUp` is False, PNG export will be skipped; STEP will still be produced in many cases.
- Some scripts close the document and main window at the end (`FreeCAD.closeDocument(...)`, `FreeCADGui.getMainWindow().close()`). You can remove/comment those lines while iterating.

---

## Parameters (quick reference)

Edit the top of the script to change these (names vary slightly between versions):

- Overall dimensions:
  - `length` — total length in mm (or derived from modules_x × module_length)
  - `width` — total width in mm (or derived from modules_y × module_width)
  - `height`, `height_front`, `height_back` — post / roof heights in mm

- Structural sizes:
  - `pole_size` — post square section in mm
  - `rail_size`, `rail_section` — rail profile sizes in mm
  - `frame_size`, `frame_height` — module frame profiles

- PV / module settings:
  - `module_length`, `module_width`, `module_thickness`
  - `modules_x`, `modules_y` — number of modules along length/width

- Outputs:
  - `export_path_step`, `export_step` — STEP filename
  - `export_path_png`, `export_png` — PNG filename (only when GUI is available)

---

## Output

- STEP (.step) — Solid model suitable for import into CAD tools (SolidWorks, ArchiCAD, etc.)
- PNG (.png) — 2D rendered image (isometric/axonometric) for quick visualization (requires GUI)

Default filenames are hard-coded in each script; change them near the top to match your project structure.

---

## Tips & gotchas

- PNG export requires a running FreeCAD GUI. If you run on a headless server (FreeCADCmd), remove or guard GUI-specific lines.
- If you want to run batch STEP generation on a server, remove `FreeCADGui` calls and any `close main window` calls — the STEP export can work headless.
- The scripts use simple box geometry (Part.makeBox) for profiles. Replace with more detailed profiles if you need realistic metal section geometry.
- The scripts apply color to shown parts for clarity — this does not affect exported STEP geometry.
- Some scripts include assertions to verify module fits. If you change module or layout sizes, watch for assertion errors.

---

## Extending & Contributing

- Add more realistic profiles (I-profiles, C-channels, extrusions) by replacing `Part.makeBox` with sweeps/profiles.
- Parameterize connectors, bolts, and cutouts if you need manufacturing-ready geometry.
- Improve headless compatibility by splitting geometry generation (STEP) and visualization (PNG) into separate modes.
- Pull requests and suggestions are welcome. Include simple examples and, if relevant, small sample STEP outputs for review.

---

## Author & Contact

Author: BOEHM Jean  
GitHub: @jboehm1

---

## License

No license file is present in the repository. If you want this repo to be open-source, add a LICENSE file (MIT / Apache-2.0 / GPL-3.0 are common choices). Until a license is added, assume default copyright.

---

If you'd like, I can:
- produce a cleaned README file matching this content for the repository, and
- suggest a small CONTRIBUTING.md or example macro-run script next to the macros.
