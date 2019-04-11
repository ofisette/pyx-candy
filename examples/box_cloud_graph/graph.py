#!/usr/bin/env python3

# We create a PyX 2D graph, add a “fake” bar plot axis, and use it to plot
# several RMSD datasets from a molecular dynamics simulation. Each dataset has
# an associated key (a protein name) associated with an index (i) that controls
# its position on the graph. Instead of individual points or a simple bar plot,
# we use box plots and cloud plots, which provide, for each data set, both a
# detailed view of the distribution (cloud) and a statistical overview (box).

from pyx import *
from pyx.graph import graphxy, axis
from pyx.graph.axis import parter, texter

from pyxcandy import (
    fakebaraxis,
    emptyaxis,
    keyticks,
    rgb256pyx,
    read_dat,
    clouddata,
    cloudplot,
    boxdata,
    boxplot
)

protein_names = [
        r"α\textsubscript{HC}",
        r"β\textsubscript{2}m",
        "Tsn",
        "ERp57",
        "Crt",
]

protein_keys = keyticks(protein_names)

BlueU = rgb256pyx(0, 119, 184)
DarkBlueD = rgb256pyx(0, 76, 115)
OrangeU = rgb256pyx(252, 160, 0)
PinkU = rgb256pyx(227, 125, 173)
VermillonU = rgb256pyx(244, 65, 0)

text.set(cls=text.LatexRunner, texenc='utf-8')
text.preamble(r'\usepackage[utf8]{inputenc}')
text.preamble(r'\usepackage{textgreek}')
text.preamble(r'\usepackage{fixltx2e}')
text.preamble(r'\usepackage{libertine}')
text.preamble(r'\renewcommand{\familydefault}{\sfdefault}')
text.preamble(r'\usepackage{sansmath}')

g = graphxy(
    width = 5.0,
    height = 2.4,
    x = fakebaraxis(
        ticks = protein_keys,
        texter = texter.decimal(labelattrs=[text.clearmathmode])
    ),
    x2 = emptyaxis(),
    y = axis.linear(
        min = 0.0,
        max = 12.0,
        parter = parter.linear(tickdists=[4.0,2.0]),
        texter = texter.decimal(labelattrs=[text.clearmathmode]),
        title = r"C\textsubscript{α} RMSD ± std (Å)"
    )
)

i = 0
time, rmsd = read_dat("rmsd_Ahc.xvg", [float, float])
rmsd = [x * 10 for x in rmsd]
cloudplot(g, i, clouddata(rmsd), BlueU, ya=True)
boxplot(g, i, boxdata(rmsd), ya=True)

i = 1
time, rmsd = read_dat("rmsd_B2m.xvg", [float, float])
rmsd = [x * 10 for x in rmsd]
cloudplot(g, i, clouddata(rmsd), DarkBlueD, ya=True)
boxplot(g, i, boxdata(rmsd), ya=True)

i = 2
time, rmsd = read_dat("rmsd_Tsn.xvg", [float, float])
rmsd = [x * 10 for x in rmsd]
cloudplot(g, i, clouddata(rmsd), OrangeU, ya=True)
boxplot(g, i, boxdata(rmsd), ya=True)

i = 3
time, rmsd = read_dat("rmsd_ERp57.xvg", [float, float])
rmsd = [x * 10 for x in rmsd]
cloudplot(g, i, clouddata(rmsd), PinkU, ya=True)
boxplot(g, i, boxdata(rmsd), ya=True)

i = 4
time, rmsd = read_dat("rmsd_Crt.xvg", [float, float])
rmsd = [x * 10 for x in rmsd]
cloudplot(g, i, clouddata(rmsd), VermillonU, ya=True)
boxplot(g, i, boxdata(rmsd), ya=True)

g.writePDFfile("graph")
