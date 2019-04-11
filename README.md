# pyxcandy

Small collection of utilities for the PyX graphics package

This currently includes: data file reading, timeseries trends, histograms,
colour conversion, multi-colour gradients, “fake” bar plots, rain/cloud/box
plots and secondary structure plots. Even if you do not use PyX, this code might
still be useful if you want to add similar features to your favourite plotting
program.

## License

You can use pyxcandy under the terms of the MIT License; see
[`LICENSE.md`](https://github.com/ofisette/pyxcandy/blob/master/LICENSE.md) in
the project files.

## Status

This is experimental software initially developed for my specific needs. It has
not been extensively tested, but has been used to produce figures for several
papers and should be pretty safe to use.

## Installation

This package was developed for Python 3.6 and PyX 0.14, and will not work with
Python 2; numpy is also required. Link the `src` directory or copy its contents
to a location where it will be found by your Python interpreter.

## Documentation

There is no documentation for this package. Refer to the source code,
docstrings, and to the `examples` directory.

## Community

pyxcandy is developed by [Olivier Fisette](mailto:olivier.fisette@rub.de) in
the [Molecular Simulation Group](https://molecular-simulation.org/) of Lars V.
Schäfer at the Center for Theoretical Chemistry of Ruhr-University Bochum,
Germany.

Bug reports, documentation and examples are welcome. However, since PyX is no
longer actively maintained (as far as I can see), I do not plan to add new
features to pyxcandy or to merge such contributions. Development is tracked in
the project’s [repository](https://github.com/ofisette/pyxcandy).
