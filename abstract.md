# Gammapy: a Python Package for Gamma-Ray Astronomy

Gammapy is a community-developed, open source Python package for Gamma-Ray Astronomy.
It builts on the scientific Python ecosystem Numpy, Scipy and Astropy and implements
high level analysis functionality applicable to Gamma-Ray data of many instruments.
Starting from event lists and description of the specific instrument response it supports
reduction of the input data to binned data structures, such as WCS, HEALPix or region
based maps.

It also offers a varity of background estimation methods for spectral, spatial,
combined spectro-morphological as well as time analysis.

It supports a variaty of spectral, spatial and temporal models as well as user implemented custom models, e.g. parametrising energy dependent morphology of sources.

It also supports joint likelihood fitting as well has multi-instrument analysis.

In this contribution we present an overview of the most recent features and API along with some example analyses
using H.E.S.S and Fermi-LAT and simulated CTA data. We also outline the general development status and future goals.


Estimation of flux points, flux maps and light curves in energy bands.
