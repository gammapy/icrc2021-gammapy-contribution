# Gammapy: a Python Package for Gamma-Ray Astronomy

Gammapy is a community-developed, open source Python package for Gamma-Ray Astronomy.
It builts on the scientific Python ecosystem Numpy, Scipy and Astropy and implements
high level analysis functionality applicable to Gamma-Ray data of many existing as well as
future instruments. Starting from event lists and description of the specific instrument response
stored in a common FITS based data format, Gammapy implements the reduction of the input data
and instrument reponse to binned data structures, such as WCS, HEALPix or region based maps
with arbitrary non-spatial axes, typically energy. Thereby it also allows to handle the
dependency of the instrument response with time, energy as well as  position on the sky.
In addition it offers a varity of background estimation methods for spectral, spatial,
combined spectro-morphological as well as time and phase analysis.

Binned likelihood fitting Estimation of flux points, flux maps and light curves in energy bands.
It supports a variaty of spectral, spatial and temporal models as well as user implemented custom models, e.g. parametrising energy dependent morphology of sources.

It also supports joint likelihood fitting as well has multi-instrument analysis.

In this contribution we present an overview of the most recent features and API along with some example analyses
using H.E.S.S, Fermi-LAT and simulated CTA data. We also outline the general development status and future goals.



