#!/usr/bin/python
#
# -- Windows Powershell install conda to $env:USERPROFILE\Miniforge (one-time)
#   curl.exe -L -o miniforge.exe https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
#   Start-Process -Wait -FilePath miniforge.exe -ArgumentList @("/InstallationType=JustMe", "/RegisterPython=0", "/NoRegistry=1", "/NoScripts=0", "/S", "/D=$env:USERPROFILE\Miniforge")
#
# -- Windows Powershell activate conda
#   . $env:USERPROFILE\Miniforge\shell\condabin\conda-hook.ps1
#   conda activate
#
# -- Windows Powershell install cadquery (one-time)
#   conda create -n cq
#   conda activate cq
#   mamba install cadquery
#
# -- Windows Powershell generate custom pinheader
#   . $env:USERPROFILE\Miniforge\shell\condabin\conda-hook.ps1
#   conda activate cq
#   python CustomPinHeader_02x09_P2.54mm_Hybrid.py
#

import cadquery as cq
from cadquery.vis import show

body_color = cq.Color(0.148, 0.145, 0.145)
pins_color = cq.Color(0.859, 0.738, 0.496)

n = 9
pitch = 2.54
row_pitch = 7.62
base_width = 2.54
base_height = 2.54
base_chamfer = pitch/10.0
pin_width = 0.64
pin_length_above_base = 6.0
pin_end_chamfer = pin_width/4.0

pin_length_below_board = 3.0
pin_length_horizontal = 2.82
base_z_offset = 0.76

def make_base():
    base = (
        cq.Workplane("XY")
        .workplane(offset = base_z_offset)
        .moveTo(-base_width / 2.0 + base_chamfer, n / 2.0 * pitch)
    )
    for x in range(0, n):
        base = (
            base.line(-base_chamfer, -base_chamfer)
            .vLine(-pitch + base_chamfer*2.0)
            .line(base_chamfer, -base_chamfer)
        )
    base = base.hLine(base_width - base_chamfer*2.0)
    for x in range(0, n):
        base = (
            base.line(base_chamfer, base_chamfer)
            .vLine(pitch - base_chamfer*2.0)
            .line(-base_chamfer, base_chamfer)
        )
    base = base.close().extrude(base_height)
    return base

#
# -- make THT pins 1 and 9
#
def make_THT_pins():
    total_length = pin_length_below_board + base_height + pin_length_above_base
    pin = (
        cq.Workplane("XY")
        .workplane(offset = -pin_length_below_board + base_z_offset)
        .box(pin_width, pin_width, total_length, centered = (True, True, False))
        .edges("#Z")
        .chamfer(pin_end_chamfer)
    )
    pins = cq.Workplane("XY").workplane(offset = -pin_length_below_board)
    for y in (0, 8):
        pins = pins.union(pin.translate((0, (y - 4)*-pitch,0)))
    return pins

#
# -- make SMD pins 2 through 8
#
def make_SMD_pins():
    pin_array = []
    pin_array.append(
        cq.Workplane("XZ")
        .workplane(offset = -((n - 1) * pitch + pin_width) / 2.0)
        .moveTo(pin_width / 2.0, base_z_offset + base_height + pin_length_above_base)
        .hLine(-pin_width)
        .vLine(-base_z_offset - base_height - pin_length_above_base + pin_width)
        .hLine(-pin_length_horizontal + pin_width)
        .vLine(-pin_width)
        .hLine(pin_length_horizontal)
        .close()
        .extrude(pin_width)
        .edges(">X and <Z")
        .fillet(pin_width)
    )
    pin_array[0] = pin_array[0].faces(">Z").chamfer(pin_end_chamfer)
    pin_array[0] = pin_array[0].faces("<X").chamfer(pin_end_chamfer)
    pin_array.append(
        cq.Workplane("XZ")
        .workplane(offset = -((n - 1) * pitch + pin_width) / 2.0)
        .moveTo(-pin_width / 2.0, base_z_offset + base_height + pin_length_above_base)
        .hLine(pin_width)
        .vLine(-base_z_offset - base_height - pin_length_above_base + pin_width)
        .hLine(pin_length_horizontal - pin_width)
        .vLine(-pin_width)
        .hLine(-pin_length_horizontal)
        .close()
        .extrude(pin_width)
        .edges("<X and <Z")
        .fillet(pin_width)
    )
    pin_array[1] = pin_array[1].faces(">Z").chamfer(pin_end_chamfer)
    pin_array[1] = pin_array[1].faces(">X").chamfer(pin_end_chamfer)

    pins = cq.Workplane("XY")
    right_pin = range(1, n - 1, 2)
    left_pin = range(2, n - 1, 2)
    for y in right_pin:
            pins = pins.union(pin_array[0].translate((0, y*-pitch, 0)))
    for y in left_pin:
            pins = pins.union(pin_array[1].translate((0, y*-pitch, 0)))
    return pins

if __name__ == "__main__":
    assembly = cq.Assembly()
    base = make_base()
    assembly.add(base, color = body_color)
    assembly.add(base.translate((row_pitch, 0.0, 0.0)), color = body_color)
    THT_pins = make_THT_pins()
    assembly.add(THT_pins, color = pins_color)
    assembly.add(THT_pins.translate((row_pitch, 0.0, 0.0)), color = pins_color)
    SMD_pins = make_SMD_pins()
    assembly.add(SMD_pins, color = pins_color)
    assembly.add(SMD_pins.rotate((0, 0, 0), (0, 0, 1), 180).translate((row_pitch, 0.0, 0.0)), color = pins_color)
    assembly.export("CustomPinHeader_02x09_P2.54mm_Hybrid.step", "STEP")
