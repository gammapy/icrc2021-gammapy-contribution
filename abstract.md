# Gammapy: a Python Package for Gamma-Ray Astronomy

Gammapy is a community-developed, open source Python package for gamma-ray Astronomy, 
which is built on the scientific Python ecosystem Numpy, Scipy and Astropy. It provides
methods for the analysis of gamma-ray data of many instruments including
Imaging Atmospheric Cherenkov Telescopes, Water Cherenkov, as well as space based observatories.

Starting from event lists and a description of the specific instrument response functions (IRF)
stored in open FITS based data formats, Gammapy implements the reduction of the input data
and instrument response to binned WCS, HEALPix or region based data structures. 
Thereby it handles the dependency of the IRFs with time, energy as well as position on the sky.
It offers a variety of background estimation methods for spectral, spatial and spectro-morphological 
analysis. Counts, background and IRFs data are bundled in datasets and can be serialised, rebinned
and stacked.

Gammapy supports to model binned data using Poisson maximum likelihood fitting.
It comes with built-in spectral, spatial and temporal models as well as support for custom user models,
to model e.g. energy dependent morphology of gamma-ray sources. Multiple datasets
can be combined in a joint-likelihood approach to either handle time dependent IRFs, different classes
of events or combination of data from multiple instruments. Gammapy also implements
methods to estimate flux points, including likelihood profiles per energy bin, light curves as well as
flux and signficance maps in energy bins.

In this contribution we present an overview of the most recent features and user interface of Gammapy along
with example analyses using H.E.S.S, Fermi-LAT and simulated CTA data.
