#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.convolution import Gaussian2DKernel
from regions import CircleSkyRegion
from gammapy.modeling import Fit
from gammapy.data import DataStore
from gammapy.datasets import (
    Datasets,
    FluxPointsDataset,
    SpectrumDataset,
    MapDataset,
)
from gammapy.modeling.models import (
    PowerLawSpectralModel,
    SkyModel,
    GaussianSpatialModel,
)
from gammapy.maps import MapAxis, WcsNDMap, WcsGeom, RegionGeom
from gammapy.makers import (
    MapDatasetMaker,
    SafeMaskMaker,
    SpectrumDatasetMaker,
    ReflectedRegionsBackgroundMaker,
)
from gammapy.estimators import TSMapEstimator, FluxPointsEstimator, FluxPoints
from gammapy.estimators.utils import find_peaks
from gammapy.visualization import plot_spectrum_datasets_off_regions

# Configure the logger, so that the spectral analysis
# isn't so chatty about what it's doing.
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


ENERGY_AXIS = MapAxis.from_edges(
    np.logspace(-1.0, 1.0, 10), unit="TeV", name="energy", interp="log"
)

GEOM = WcsGeom.create(
    skydir=(0, 0), npix=(500, 400), binsz=0.02, frame="galactic", axes=[ENERGY_AXIS]
)


def get_observations():
    # Select observations
    data_store = DataStore.from_dir("$GAMMAPY_DATA/cta-1dc/index/gps")
    obs_id = [110380, 111140, 111159]
    return data_store.get_observations(obs_id)


def make_datasets(observations):
    # Define map geometry
    stacked = MapDataset.create(geom=GEOM)
    stacked.edisp = None
    maker = MapDatasetMaker(selection=["counts", "background", "exposure", "psf"])
    maker_safe_mask = SafeMaskMaker(methods=["offset-max"], offset_max=2.5 * u.deg)

    for obs in observations:
        cutout = stacked.cutout(obs.pointing_radec, width="5 deg")
        dataset = maker.run(cutout, obs)
        dataset = maker_safe_mask.run(dataset, obs)
        stacked.stack(dataset)

    return stacked  


def make_datasets_spectral(observations):
    target_position = SkyCoord(0, 0, unit="deg", frame="galactic")
    on_radius = 0.2 * u.deg
    on_region = CircleSkyRegion(center=target_position, radius=on_radius)

    exclusion_mask = GEOM.to_image().region_mask([on_region], inside=False)
    
    energy_axis = MapAxis.from_energy_bounds(
        0.1, 40, 40, unit="TeV", name="energy"
    )
    energy_axis_true = MapAxis.from_energy_bounds(
        0.05, 100, 200, unit="TeV", name="energy_true"
    )

    geom = RegionGeom.create(region=on_region, axes=[energy_axis])
    dataset_empty = SpectrumDataset.create(
        geom=geom, energy_axis_true=energy_axis_true
    )

    dataset_maker = SpectrumDatasetMaker(
        containment_correction=False, selection=["counts", "exposure", "edisp"]
    )
    bkg_maker = ReflectedRegionsBackgroundMaker(exclusion_mask=exclusion_mask)
    safe_mask_masker = SafeMaskMaker(methods=["aeff-max"], aeff_percent=10)

    datasets = Datasets()

    for observation in observations:
        dataset = dataset_maker.run(
            dataset_empty.copy(name=f"obs-{observation.obs_id}"), observation
        )
        dataset_on_off = bkg_maker.run(dataset, observation)
        dataset_on_off = safe_mask_masker.run(dataset_on_off, observation)
        datasets.append(dataset_on_off)

    return datasets


def make_flux_points(datasets):
    # Flux points are computed on stacked observation
    stacked_dataset = datasets.stack_reduce(name="stacked")
    stacked_dataset.models = datasets.models

    energy_edges = MapAxis.from_energy_bounds(
        "1 TeV", "30 TeV", nbin=7
        ).edges

    fpe = FluxPointsEstimator(
        energy_edges=energy_edges, source="source-gc", selection_optional="all"
        )
    return fpe.run(datasets=[stacked_dataset])


def fit_model(datasets):
    spectral_model = PowerLawSpectralModel(
        index=2, amplitude=1e-11 * u.Unit("cm-2 s-1 TeV-1"), reference=1 * u.TeV
    )

    model = SkyModel(spectral_model=spectral_model, name="source-gc")

    datasets.models = model

    fit = Fit(datasets)
    result = fit.run()
    return datasets.models


def plot_spectrum_and_image():
    dataset_image = MapDataset.read("data/stacked.fits").to_image()
    datasets = Datasets.read("data/datasets.yaml")

    fig = plt.figure(figsize=(10, 4))

    wcs = dataset_image.counts.geom.wcs
    rect = (0.052, 0.06, 0.4, 0.98)
    ax = fig.add_axes(rect=rect, projection=wcs)
    dataset_image.counts.smooth("0.03 deg").plot(ax=ax, vmax=15, stretch="asinh")

    datasets[0].counts.geom.region.to_pixel(ax.wcs).plot(ax=ax, edgecolor="white")
    plot_spectrum_datasets_off_regions(datasets, ax=ax, legend_kwargs={"loc": "lower left"})

    rect = (0.535, 0.14, 0.45, 0.8)
    ax = fig.add_axes(rect=rect)
    fp = FluxPoints.read("data/flux-points.fits", sed_type="likelihood")
    fp.plot(ax=ax, sed_type="e2dnde", color="tab:orange")
    fp.plot_ts_profiles(ax=ax, sed_type="e2dnde")

    plt.savefig("../poster/figures/cta-gc-image-spectrum.pdf", dpi=300)


if __name__ == "__main__":
    # observations = get_observations()
    # stacked = make_datasets(observations)
    # stacked.write("data/stacked.fits", overwrite=True)

    # datasets = make_datasets_spectral(observations)
    # datasets.write("data/datasets.yaml", overwrite=True)

    # models = fit_model(datasets)
    # models.write("data/best-fit-model.yaml", overwrite=True)

    # fp = make_flux_points(datasets)
    # fp.write("data/flux-points.fits", overwrite=True)

    plot_spectrum_and_image()
