# -*- coding: utf-8 -*-
# +---------------------------------------------------------------------------+
# |  Copyright (c) 2020 Frank Martinez <mnesarco at gmail.com>                |
# |                                                                           |
# |  This file is part of Marz Workbench.                                     |
# |                                                                           |
# |  Marz Workbench is free software: you can redistribute it and/or modify   |
# |  it under the terms of the GNU General Public License as published by     |
# |  the Free Software Foundation, either version 3 of the License, or        |
# |  (at your option) any later version.                                      |
# |                                                                           |
# |  Marz Workbench is distributed in the hope that it will be useful,                |
# |  but WITHOUT ANY WARRANTY; without even the implied warranty of           |
# |  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |
# |  GNU General Public License for more details.                             |
# |                                                                           |
# |  You should have received a copy of the GNU General Public License        |
# |  along with Marz Workbench.  If not, see <https://www.gnu.org/licenses/>. |
# +---------------------------------------------------------------------------+

from freecad.marz.model.neck_profile import NeckProfile
from freecad.marz.model.instrument import NeckJoint, NutPosition, NutSpacing, inch_to_mm
from freecad.marz.extension.properties import FreecadPropertiesHelper, FreecadPropertyHelper as fcp
from freecad.marz.model.transitions import TransitionFunction

# Support loading old files with different property names
COMPAT_PRE_028 = {
    'Headstock_Width': 'HeadStock_Width', 
    'Headstock_Length': 'HeadStock_Length', 
    'Headstock_Thickness': 'HeadStock_Thickness', 
    'Headstock_Depth': 'HeadStock_Depth', 
    'Headstock_Angle': 'HeadStock_Angle', 
    'Headstock_VoluteRadius': 'HeadStock_VoluteRadius', 
    'Headstock_VoluteOffset': 'HeadStock_VoluteOffset', 
    'Headstock_TopTransitionLength': 'HeadStock_TopTransitionLength', 
    'Headstock_TransitionStiffness': 'HeadStock_TransitionStiffness', 
    'Trussrod_Length': 'TrussRod_Length', 
    'Trussrod_Width': 'TrussRod_Width', 
    'Trussrod_Depth': 'TrussRod_Depth', 
    'Trussrod_HeadLength': 'TrussRod_HeadLength',
    'Trussrod_HeadWidth': 'TrussRod_HeadWidth', 
    'Trussrod_HeadDepth': 'TrussRod_HeadDepth', 
    'Trussrod_TailLength': 'TrussRod_TailLength', 
    'Trussrod_TailWidth': 'TrussRod_TailWidth', 
    'Trussrod_TailDepth': 'TrussRod_TailDepth', 
    'Trussrod_End': 'TrussRod_End', 
    'Stringset_Gauges': 'StringSet_Gauges', 
    'Fretwire_TangDepth': 'FretWire_TangDepth', 
    'Fretwire_TangWidth': 'FretWire_TangWidth', 
    'Fretwire_CrownHeight': 'FretWire_CrownHeight', 
    'Fretwire_CrownWidth': 'FretWire_CrownWidth', 
    'Autoupdate_Fretboard': 'AutoUpdate_Fretboard', 
    'Autoupdate_Neck': 'AutoUpdate_Neck', 
    'Autoupdate_Body': 'AutoUpdate_Body'
}

# All Instrument Properties
properties = [

    # Scale
    fcp('scale.bass',                   inch_to_mm(25.5), "Bass Scale", compat=COMPAT_PRE_028),
    fcp('scale.treble',                 inch_to_mm(25.5), "Treble Scale", compat=COMPAT_PRE_028),

    # Nut
    fcp('nut.thickness',                5, "Thickness of the nut", compat=COMPAT_PRE_028),
    fcp('nut.spacing',                  NutSpacing.EQ_GAP, 'String spacing method', enum=NutSpacing, compat=COMPAT_PRE_028),
    fcp('nut.position',                 NutPosition.PERPENDICULAR, 'Nut align', enum=NutPosition, compat=COMPAT_PRE_028),
    fcp('nut.offset',                   0, 'Distance from fret 0 and Nut', compat=COMPAT_PRE_028),
    fcp('nut.depth',                    5, 'Nut slot depth into the fretboard', compat=COMPAT_PRE_028),
    fcp('nut.stringDistanceProj',       34.5, 'Distance from first to last String at average nut position', compat=COMPAT_PRE_028),

    # Neck
    fcp('neck.joint',                   NeckJoint.SETIN, 'Neck joint Type', enum=NeckJoint, compat=COMPAT_PRE_028),
    fcp('neck.startThickness',          15, 'Thickness at nut position', compat=COMPAT_PRE_028),
    fcp('neck.endThickness',            15, 'Thickness at heel transition start position', compat=COMPAT_PRE_028),
    fcp('neck.jointFret',               16, 'Number of fret where heel transition starts', ui='App::PropertyInteger', compat=COMPAT_PRE_028),
    fcp('neck.topOffset',               2, 'Offset between body top and fretboard bottom', compat=COMPAT_PRE_028),
    fcp('neck.angle',                   0, 'Neck break angle', ui='App::PropertyAngle', compat=COMPAT_PRE_028),
    fcp('neck.tenonThickness',          0, 'Tenon Thickness if Set In Neck', compat=COMPAT_PRE_028),
    fcp('neck.tenonLength',             0, 'Tenon Length if Set In Neck', compat=COMPAT_PRE_028),
    fcp('neck.tenonOffset',             0, 'Tenon Offset if Set In Neck', compat=COMPAT_PRE_028),
    fcp('neck.profile',                 "C Classic", 'Neck profile section', options=lambda: [p.name for p in NeckProfile.LIST.values()], compat=COMPAT_PRE_028),
    fcp('neck.transitionLength',        50, 'Length of the heel transition', compat=COMPAT_PRE_028),
    fcp('neck.transitionTension',       35, 'Tension of the heel transition', compat=COMPAT_PRE_028),
    fcp('neck.transitionFunction',      TransitionFunction.CATENARY, 'Math function of the heel transition', enum=TransitionFunction, compat=COMPAT_PRE_028),
    fcp('neck.heelFillet',              1.0, 'Heel corners fillet (radius)', compat=COMPAT_PRE_028),
    fcp('neck.heelOffset',              0.0, 'Heel offset under the fretboard', compat=COMPAT_PRE_028),

    # Fretboard
    fcp('fretboard.thickness',          7, 'Fretboard total thickness', compat=COMPAT_PRE_028),
    fcp('fretboard.startRadius',        inch_to_mm(10), 'Radius at nut', compat=COMPAT_PRE_028),
    fcp('fretboard.endRadius',          inch_to_mm(14), 'Radius at end', compat=COMPAT_PRE_028),
    fcp('fretboard.startMargin',        5, 'Margin before nut', compat=COMPAT_PRE_028),
    fcp('fretboard.endMargin',          5, 'Margin after last fret', compat=COMPAT_PRE_028),
    fcp('fretboard.sideMargin',         3, 'Margin on sides', compat=COMPAT_PRE_028),
    fcp('fretboard.fretNipping',        2, 'Fret tang nipping distance', compat=COMPAT_PRE_028),
    fcp('fretboard.perpendicularFret',  7, 'Number of the perpendicular fret', ui='App::PropertyInteger', compat=COMPAT_PRE_028),
    fcp('fretboard.frets',              24, 'Number of frets', ui='App::PropertyInteger', compat=COMPAT_PRE_028),
    fcp('fretboard.inlayDepth',         1, 'Depth of fretboard inlay carvings', compat=COMPAT_PRE_028),
    fcp('fretboard.filletRadius',       1.0, 'Fillet radius for the corners of the fretboard', compat=COMPAT_PRE_028),

    #! TODO: Needs some refinements
    #! fcp('fretboard.cut',                FretboardCut.PARALLEL, 'End cut type', enum=FretboardCut),
    #! fcp('fretboard.cutBassDistance',    400, 'Distance to cut at bass'),
    #! fcp('fretboard.cutTrebleDistance',  400, 'Distance to cut at treble'),

    # Bridge
    fcp('bridge.bassCompensation',      0, 'Compensation on bass scale', compat=COMPAT_PRE_028),
    fcp('bridge.trebleCompensation',    0, 'Compensation on treble scale', compat=COMPAT_PRE_028),
    fcp('bridge.stringDistanceProj',    63, 'String Distance at Bridge (Projected to vertical)', compat=COMPAT_PRE_028),
    fcp('bridge.height',                16.363, "Height of the bridge from body's top to strings", compat=COMPAT_PRE_028),

    # Headstock
    fcp('headStock.width',                       100, 'Default Width if no custom contour is provided', compat=COMPAT_PRE_028),
    fcp('headStock.length',                      220, 'Default Length if no custom contour is provided', compat=COMPAT_PRE_028),
    fcp('headStock.thickness',                    15, 'Headstock thickness', compat=COMPAT_PRE_028),
    fcp('headStock.depth',                         5, 'Depth (only apply if Flat)', compat=COMPAT_PRE_028),
    fcp('headStock.angle',                         9, 'Headstock break angle', ui='App::PropertyAngle', compat=COMPAT_PRE_028),
    fcp('headStock.transitionParamHorizontal',   0.5, 'Transition stiffness', ui="App::PropertyFloat", name="Headstock_TransitionStiffness", compat=COMPAT_PRE_028),
    fcp('headStock.voluteRadius',                 50, 'Volute radius. If zero then no volute', compat=COMPAT_PRE_028),
    fcp('headStock.voluteOffset',                 10, 'Volute offset into the neck', compat=COMPAT_PRE_028),
    fcp('headStock.topTransitionLength',          20, 'Length of the transition between nut and top of the headstock in Flat headstocks. Ignored if angle is greater than zero', compat=COMPAT_PRE_028),

    # Truss Rod Channel
    fcp('trussRod.length',              430, 'Total Length of trussRod', compat=COMPAT_PRE_028),
    fcp('trussRod.width',               6, 'Channel width', compat=COMPAT_PRE_028),
    fcp('trussRod.depth',               9, 'Channel depth', compat=COMPAT_PRE_028),
    fcp('trussRod.headLength',          20, 'Head length', compat=COMPAT_PRE_028),
    fcp('trussRod.headWidth',           8, 'Head width', compat=COMPAT_PRE_028),
    fcp('trussRod.headDepth',           11, 'Head depth', compat=COMPAT_PRE_028),
    fcp('trussRod.tailLength',          0, 'Tail length', compat=COMPAT_PRE_028),
    fcp('trussRod.tailWidth',           0, 'Tail width', compat=COMPAT_PRE_028),
    fcp('trussRod.tailDepth',           0, 'Tail depth', compat=COMPAT_PRE_028),
    fcp('trussRod.start',               0, 'Distance from neck start (nut)', ui='App::PropertyDistance',
                                        name='Trussrod_End', compat=COMPAT_PRE_028), #Renamed for clarity

    # String Set (Use StringList instead of FloatList because FloatList precision is too limited)
    fcp('stringSet.gauges',             ['0.010','0.013','0.017','0.026','0.036','0.046'], 
                                        'Gauges of the strings in INCHES', ui="App::PropertyStringList",
                                        compat=COMPAT_PRE_028),

    # Fret Wire
    fcp('fretWire.tangDepth',           inch_to_mm(0.055), 'Fret slot depth', compat=COMPAT_PRE_028),
    fcp('fretWire.tangWidth',           inch_to_mm(0.020), 'Fret slot width', compat=COMPAT_PRE_028),
    fcp('fretWire.crownHeight',         inch_to_mm(0.039), 'Crown Height', compat=COMPAT_PRE_028),
    fcp('fretWire.crownWidth',          inch_to_mm(0.084), 'Crown Width', compat=COMPAT_PRE_028),

    # Body
    fcp('body.topThickness',            5,    'Thickness of Top', compat=COMPAT_PRE_028),
    fcp('body.backThickness',           40,   'Thickness of Back', compat=COMPAT_PRE_028),
    fcp('body.length',                  550,  'Max Length of Body Blank', compat=COMPAT_PRE_028),
    fcp('body.width',                   350,  'Max Width of Body Blank', compat=COMPAT_PRE_028),
    fcp('body.neckPocketCarve',         True, 'Carve Neck pocket from body', ui='App::PropertyBool', compat=COMPAT_PRE_028),
    fcp('body.neckPocketDepth',         20,   'Depth of Neck Pocket', compat=COMPAT_PRE_028),
    fcp('body.neckPocketLength',        55,   'Length of Neck Pocket', compat=COMPAT_PRE_028),

    # Internal
    fcp('internal.bodyImport',          0, ui='App::PropertyInteger', mode=4, compat=COMPAT_PRE_028),
    fcp('internal.headstockImport',     0, ui='App::PropertyInteger', mode=4, compat=COMPAT_PRE_028),
    fcp('internal.inlayImport',         0, ui='App::PropertyInteger', mode=4, compat=COMPAT_PRE_028),

    # AutoUpdate
    fcp('autoUpdate.fretboard',         True, 'Toggle Fretboard autoupdate', ui='App::PropertyBool', compat=COMPAT_PRE_028),
    fcp('autoUpdate.neck',              True, 'Toggle Neck autoupdate', ui='App::PropertyBool', compat=COMPAT_PRE_028),
    fcp('autoUpdate.body',              True, 'Toggle Body autoupdate', ui='App::PropertyBool', compat=COMPAT_PRE_028),

]

InstrumentProps = FreecadPropertiesHelper(properties)
