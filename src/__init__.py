import random

import numpy as np

import pyx
from pyx import *
from pyx.graph import graphxy, axis, data
from pyx.graph.axis import parter, painter, texter
from pyx.graph.axis.tick import tick

def read_dat(input_file, col_types, comment_chars = '#%@'):
    """Read data from a text file, returning a tuple of lists.

    Arguments:
    input_file -- A filename or file-like stream
    col_types -- A list of types, one for each column in the data file

    Keyword argument:
    comment_chars -- Ignore lines starting with these characters (default: #%@)
    """

    if isinstance(input_file, str):
        input_file = open(input_file)

    rows = []
    ncol = len(col_types)

    for n, line in enumerate(input_file):
        line = line.strip()
        if line and not line[0] in comment_chars:
            cols = []
            tokens = line.split()
            if len(tokens) != ncol:
                raise Exception('line %d: read %d columns, expected %d' %
                                (n + 1, len(tokens), len(col_types)))
            for j in range(ncol):
                cols.append(col_types[j](tokens[j]))
            rows.append(cols)

    if not rows:
        raise Exception('empty data file')

    nrow = len(rows[0])
    cols = [[] for i in range(ncol)]

    for row in rows:
        for j in range(ncol):
            cols[j].append(row[j])

    return cols

def trend(series, n):
    """Return the running average, minimum and maximum of a series for an n-
    element moving window."""
    meanvals = []
    minvals = []
    maxvals = []
    running = []
    for val in series:
        running.append(val)
        if len(running) > n:
            running.pop(0)
        meanvals.append(sum(running) / len(running))
        minvals.append(min(running))
        maxvals.append(max(running))
    return meanvals, minvals, maxvals

def hist(vals, nbins=None, minv=None, maxv=None, normalize=False, maxh=None,
        factor=None):
    """Make a histogram, returning a two-tuple of bin centers and bin values.

    Arguments:
    vals -- Input values

    Keyword arguments:
    nbins -- Number of bins (default: min(len(vals)/10, 100))
    minv, maxv -- Histogram range (inclusive, default: min(vals), max(vals))
    normalize -- Scale bin values to total 1.0 (default: False)
    maxh -- Scale bin values so that the largest becomes maxh (default: None)
    factor -- Scale bin values by factor (default: None)
    """
    if minv is None:
        minv = min(vals)
    if maxv is None:
        maxv = max(vals)
    if nbins is None:
        nbins = int(np.ceil(len(vals) / 10))
        if nbins > 100:
            nbins = 100
    d = np.nextafter((maxv - minv) / nbins, np.inf)
    centers = [i*d + d/2 + minv for i in range(nbins)]
    bins = [0 for i in range(nbins)]
    for val in vals:
        i = int(np.floor((val - minv) / d))
        if 0 <= i < len(bins):
            bins[i] += 1
    if normalize or maxh is not None or factor is not None:
        if normalize:
            sumb = sum(bins)
            factor = 1.0 / sumb
        elif maxh is not None:
            factor = maxh / max(bins)
        for i in range(nbins):
            bins[i] *= factor
    return centers, bins

def rgb256pyx(red, green, blue):
    """Return a PyX RGB color from unsigned 1-byte int components (0-255)."""
    return color.rgb(
        float(red)/255,
        float(green)/255,
        float(blue)/255
    )

def gradient_comp_func(colors, comp):
    n = len(colors)
    d = 1.0 / (n-1)
    def func(x):
        for i in range(n):
            c = i*d
            if (c - d/2) <= x <= (c + d/2):
                return getattr(colors[i], comp)
    return func

def sharpgradient_rgb_multi(color1, color2, *colors):
    """Return a PyX RGB gradient that sharply transitions through colors."""
    colors = [color1, color2, *colors]
    return color.functiongradient_rgb(
        gradient_comp_func(colors, "r"),
        gradient_comp_func(colors, "g"),
        gradient_comp_func(colors, "b")
    )

def fakebarpainter(*args, **kwargs):
    """Return a PyX linear axis painter that behaves like a bar axis painter."""
    return painter.regular(innerticklength=0, outerticklength=0)

def keyticks(labels, *args, **kwargs):
    """Return a list of PyX ticks that can be used as keys in a fake bar
    plot.

    Each key is assigned an integer position on the graph axis starting at 0."""
    return [tick(i, label=labels[i], *args, **kwargs) \
            for i in range(len(labels))]

def emptyaxis():
    """Return a PyX linear axis with no ticks"""
    return axis.linear(min=0, max=1, parter=None)

def fakebaraxis(ticks, painter=fakebarpainter(),*args, **kwargs):
    """Return a PyX linear axis that can be used to make fake bar plots.

    Use "keyticks" to create the ticks expected by this function."""
    return axis.linear(
        min=-0.5,
        max=len(ticks)-0.5,
        parter=None,
        manualticks=ticks,
        painter=painter,
        *args,
        **kwargs
    )

def boxdata(vals):
    """Compute and return the required data for an ext/std box plot."""
    min = np.min(vals)
    max = np.max(vals)
    mean = np.mean(vals)
    median = np.median(vals)
    std = np.std(vals)
    return min, max, mean - std, mean + std, median

def boxplot(g, i, data, color=None, size=0.1, ya=False, d=-0.25):
    """Add a box plot to an existing graph.

    This method uses a fake bar plot approach by treating a linear axis as a
    bar axis. Use "fakebaraxis" to create this axis, and "emptyaxis" to create
    the opposite one (e.g. x and x2).

    Arguments:
    g -- PyX graph2d
    i -- Key index for the plot
    data -- Input values: whisker min, whisker max, box bottom, box top, band

    Keyword arguments:
    color -- Fill the box with this color (default: None)
    size -- Box and whisker size (default: 0.1 cm)
    ya -- Plot along the y-axis instead of x-axis (default: False)
    d -- Offset to the bar plot key position (default: -0.25)
    """
    min, max, bottom, top, band = data
    orig = i + d
    if ya:
        x1, y1 = g.pos(orig, min)
        x2, y2 = g.pos(orig, bottom)
        x3, y3 = g.pos(orig, top)
        x4, y4 = g.pos(orig, max)
    else:
        x1, y1 = g.pos(min, orig)
        x2, y2 = g.pos(bottom, orig)
        x3, y3 = g.pos(top, orig)
        x4, y4 = g.pos(max, orig)
    g.stroke(path.line(x1, y1, x2, y2))
    g.stroke(path.line(x3, y3, x4, y4))
    if ya:
        x1, y1 = g.pos(orig - size, min)
        x2, y2 = g.pos(orig + size, min)
        x3, y3 = g.pos(orig - size, max)
        x4, y4 = g.pos(orig + size, max)
    else:
        x1, y1 = g.pos(min, orig - size)
        x2, y2 = g.pos(min, orig + size)
        x3, y3 = g.pos(max, orig - size)
        x4, y4 = g.pos(max, orig + size)
    g.stroke(path.line(x1, y1, x2, y2), [style.linecap.square])
    g.stroke(path.line(x3, y3, x4, y4), [style.linecap.square])
    if ya:
        x1, y1 = g.pos(orig - size, bottom)
        x2, y2 = g.pos(orig + size, bottom)
        x3, y3 = g.pos(orig + size, top)
        x4, y4 = g.pos(orig - size, top)
    else:
        x1, y1 = g.pos(bottom, orig - size)
        x2, y2 = g.pos(bottom, orig + size)
        x3, y3 = g.pos(top, orig + size)
        x4, y4 = g.pos(top, orig - size)
    box = path.path(
        path.moveto(x1, y1),
        path.lineto(x2, y2),
        path.lineto(x3, y3),
        path.lineto(x4, y4),
        path.closepath()
    )
    if color is not None:
        g.fill(box, [color])
    g.stroke(box)
    if ya:
        x1, y1 = g.pos(orig - size, band)
        x2, y2 = g.pos(orig + size, band)
    else:
        x1, y1 = g.pos(band, orig - size)
        x2, y2 = g.pos(band, orig + size)
    g.stroke(path.line(x1, y1, x2, y2))

def clouddata(vals):
    """Compute and return the required data for a cloud plot."""
    return hist(vals, maxh=0.5)

def cloudplot(g, i, data, color=color.gray.black, ya=False, d=0.0):
    """Add a cloud plot to an existing graph.

    This method uses a fake bar plot approach by treating a linear axis as a
    bar axis. Use "fakebaraxis" to create this axis, and "emptyaxis" to create
    the opposite one (e.g. x and x2).

    Arguments:
    g -- PyX graph2d
    i -- Key index for the plot
    data -- Input values: histogram bin centers and bin values

    Keyword arguments:
    color -- Stroke the line with this color (default: black)
    ya -- Plot along the y-axis instead of x-axis (default: False)
    d -- Offset to the bar plot key position (default: -0.25)
    """
    centers, bins = data
    orig = i + d
    bins = [b + orig for b in bins]
    if ya:
        g.plot(
            pyx.graph.data.values(x=bins, y=centers),
            [graph.style.line(lineattrs=[color])]
        )
    else:
        g.plot(
            pyx.graph.data.values(x=centers, y=bins),
            [graph.style.line(lineattrs=[color])]
        )

def raindata(vals):
    """Compute and return the required data for a rain plot."""
    return [random.uniform(0.0, 0.5) for i in range(len(vals))], vals

def rainplot(g, i, data, color=color.gray.black, size=0.025, ya=False, d=-0.5):
    """Add a rain plot to an existing graph.

    This method uses a fake bar plot approach by treating a linear axis as a
    bar axis. Use "fakebaraxis" to create this axis, and "emptyaxis" to create
    the opposite one (e.g. x and x2).

    Arguments:
    g -- PyX graph2d
    i -- Key index for the plot
    data -- Input values

    Keyword arguments:
    color -- Fill the dots with this color (default: black)
    size -- Dot size (default: 0.025 cm)
    ya -- Plot along the y-axis instead of x-axis (default: False)
    d -- Offset to the bar plot key position (default: -0.25)
    """
    jitter, vals = data
    orig = i + d
    jitter = [j + orig for j in jitter]
    if ya:
        g.plot(
            pyx.graph.data.values(x=vals, y=jitter),
            [graph.style.symbol(
                symbol=graph.style.symbol.circle,
                size=size,
                symbolattrs=[deco.filled([color]), deco.stroked.clear]
            )]
        )
    else:
        g.plot(
            pyx.graph.data.values(x=jitter, y=vals),
            [graph.style.symbol(
                symbol=graph.style.symbol.circle,
                size=size,
                symbolattrs=[deco.filled([color]), deco.stroked.clear]
            )]
        )

def ssdata(arr, fresid=1):
    """Compute and return the required data for an SS plot.

    Argument:
    arr -- Array of secondary structure chars (L, H or S)

    Keyword argument:
    fresid -- ID of first residue (default: 1)
    """
    loops = []
    helices = []
    strands = []
    cssfresid = fresid
    css = arr[0]
    for i, ss in enumerate(arr[1:]):
        resid = i + fresid + 1
        if ss != css:
            if css == "L":
                ssarr = loops
            elif css == "H":
                ssarr = helices
            elif css == "S":
                ssarr = strands
            ssarr.append((cssfresid, resid - 1))
            cssfresid = resid
            css = ss
    if css == "L":
        ssarr = loops
    elif css == "H":
        ssarr = helices
    elif css == "S":
        ssarr = strands
    ssarr.append((cssfresid, resid))
    return fresid, fresid + len(arr) - 1, helices, strands

def ssplot(g, data, size=0.1, d=-0.125, ya=False):
    """Add a secondary structure plot to an existing graph.

    Arguments:
    g -- PyX graph2d
    i -- Key index for the plot
    data -- Input values

    Keyword arguments:
    color -- Fill the dots with this color (default: black)
    size -- Dot size (default: 0.025 cm)
    ya -- Plot along the y-axis instead of x-axis (default: False)
    d -- Offset to the bar plot key position (default: -0.25)
    """
    fresid, lresid, helices, strands = data
    if ya:
        x1 = x2 = d
        _, y1 = g.pos(0, fresid)
        _, y2 = g.pos(0, lresid)
    else:
        x1, _ = g.pos(fresid, 0)
        x2, _ = g.pos(lresid, 0)
        y1 = y2 = d
    g.stroke(path.line(x1, y1, x2, y2), [style.linecap.square])
    for ssfresid, sslresid in helices:
        if ya:
            x1 = d - size / 2
            x2 = d + size / 2
            _, y1 = g.pos(0, ssfresid)
            _, y2 = g.pos(0, sslresid)
        else:
            x1, _ = g.pos(ssfresid, 0)
            x2, _ = g.pos(sslresid, 0)
            y1 = d - size / 2
            y2 = d + size / 2
        rect = path.path(
            path.moveto(x1, y1),
            path.lineto(x1, y2),
            path.lineto(x2, y2),
            path.lineto(x2, y1),
            path.closepath()
        )
        g.fill(rect, [color.gray.white])
        g.stroke(rect)
    for ssfresid, sslresid in strands:
        if ya:
            x1 = d - size / 2
            x2 = d + size / 2
            _, y1 = g.pos(0, ssfresid)
            _, y2 = g.pos(0, sslresid)
        else:
            x1, _ = g.pos(ssfresid, 0)
            x2, _ = g.pos(sslresid, 0)
            y1 = d - size / 2
            y2 = d + size / 2
        rect = path.path(
            path.moveto(x1, y1),
            path.lineto(x1, y2),
            path.lineto(x2, y2),
            path.lineto(x2, y1),
            path.closepath()
        )
        g.fill(rect)
        g.stroke(rect)

__all__ = [
    "read_dat",
    "trend",
    "hist",
    "rgb256pyx",
    "sharpgradient_rgb_multi",
    "fakebarpainter",
    "keyticks",
    "emptyaxis",
    "fakebaraxis",
    "boxdata",
    "boxplot",
    "clouddata",
    "cloudplot",
    "raindata",
    "rainplot",
    "ssdata",
    "ssplot"
]
