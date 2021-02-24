# Gammapy: a Python Package for Gamma-Ray Astronomy

Gammapy is a community-developed, open source Python package for Gamma-Ray Astronomy.
It builts on the scientific Python ecosystem Numpy, Scipy and Astropy and provides
high level analysis functionality applicable to Gamma-Ray data of mutiple existing as well as
future instruments.

Starting from event lists and description of the specific instrument response
stored in a open FITS based data format, Gammapy implements the reduction of the input data
and instrument reponse to binned data structures, such as WCS, HEALPix or region based maps
with arbitrary non-spatial axes, typically energy. It also allows to handle the
dependency of the instrument response with time, energy as well as position on the sky.
In addition it offers a varity of background estimation methods for spectral, spatial,
combined spectro-morphological as well as time analysis. Counts data, background and IRFs
are bundled in datasets and can be serialised, rebinned and stacked.

Gammapy allows to model the binned data in many ways using Poisson maximum likelihood fitting.
It supports a variaty of built-in spectral, spatial and temporal models as well as user implemented
custom models, e.g. parametrising energy dependent morphology of Gamma-Ray sources. In addition
it also supports multiple backends for fitting such as Iminuit, Sherpa or Scipy. Mutiple datasets
can be combined in a joint-likelihood approach to handle either time dependent IRFs, different classes
of events or the combination data from multiple instruments. At the highest API level Gammapy implements
methods to estimate flux points, including likelihood profiles per energy bin, light curves as well as
flux and TS maps in energy bins.

In this contribution we present an overview of the most recent features and API along with some example analyses
using H.E.S.S, Fermi-LAT and simulated CTA data. We also outline the general development status and future goals.



