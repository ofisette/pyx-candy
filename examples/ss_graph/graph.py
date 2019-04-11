#!/usr/bin/env python3

# We create a PyX 2D graph, plot RMSF along sequence, and add an overview of the
# secondary structure below the graph; alpha helices are stroked (white
# rectangles), beta strands are filled (black rectangles).

from pyx import *
from pyx.graph import graphxy, axis, data
from pyx.graph.axis import parter, texter

from pyxcandy import (read_dat, ssdata, ssplot)

text.set(cls=text.LatexRunner, texenc='utf-8')
text.preamble(r'\usepackage[utf8]{inputenc}')
text.preamble(r'\usepackage{textgreek}')
text.preamble(r'\usepackage{fixltx2e}')
text.preamble(r'\usepackage{libertine}')
text.preamble(r'\renewcommand{\familydefault}{\sfdefault}')
text.preamble(r'\usepackage{sansmath}')

g = graph.graphxy(
    width = 5.0,
    height = 1.2,
    x = axis.linear(
        min = 1,
        max = 269,
        texter = texter.decimal(labelattrs=[text.clearmathmode]),
        title = "TN residue"
    ),
    y = axis.linear(
        min = 0.0,
        parter = parter.linear(tickdists=[4.0,2.0]),
        max = 8.0,
        texter = texter.decimal(labelattrs=[text.clearmathmode]),
        title = r"RMSF ± std (Å)"
    )
)

resid, rmsf_mean, rmsf_std = read_dat("rmsf.dat", [int, float, float])

g.plot(
    data.values(x=resid, y=rmsf_mean),
    [graph.style.line()]
)

ss = [line.strip() for line in open("ss.dat")]

ssplot(g, ssdata(ss))

g.writePDFfile("graph")
