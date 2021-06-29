import matplotlib.pyplot as plt
import matplotlib.cm as cm
from gammapy.maps import Map
from gammapy.estimators import TSMapEstimator, FluxMaps
from gammapy.datasets import MapDataset
from gammapy.modeling.models import (
    SkyModel,
    PowerLawSpectralModel,
    PointSpatialModel,
)
from gammapy.irf import PSFMap, EDispKernelMap
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np

def read_dataset():
	counts = Map.read(
    "$GAMMAPY_DATA/fermi-3fhl-gc/fermi-3fhl-gc-counts-cube.fits.gz"
	)
	background = Map.read(
	    "$GAMMAPY_DATA/fermi-3fhl-gc/fermi-3fhl-gc-background-cube.fits.gz"
	)

	exposure = Map.read(
	    "$GAMMAPY_DATA/fermi-3fhl-gc/fermi-3fhl-gc-exposure-cube.fits.gz"
	)

	psfmap = PSFMap.read(
	    "$GAMMAPY_DATA/fermi-3fhl-gc/fermi-3fhl-gc-psf-cube.fits.gz", format="gtpsf"
	)

	edisp = EDispKernelMap.from_diagonal_response(
	    energy_axis=counts.geom.axes["energy"],
	    energy_axis_true=exposure.geom.axes["energy_true"],
	)

	return MapDataset(
	    counts=counts,
	    background=background,
	    exposure=exposure,
	    psf=psfmap,
	    name="fermi-3fhl-gc",
	    edisp=edisp,
	)

def estimate_ts_map(dataset):
	spatial_model = PointSpatialModel()

	# We choose units consistent with the map units here...
	spectral_model = PowerLawSpectralModel(amplitude="1e-22 cm-2 s-1 keV-1", index=2)
	model = SkyModel(spatial_model=spatial_model, spectral_model=spectral_model)

	estimator = TSMapEstimator(
    	model,
    	kernel_width="3 deg",
    	energy_edges=[10, 50, 2000] * u.GeV,
    	n_jobs=4
	)
	return estimator.run(dataset)


def plot_sqrt_ts_maps(maps):
	fig = plt.figure(figsize=(10, 3))

	projection = maps.sqrt_ts.geom.wcs
	rect = (0.052, 0.1, 0.42, 0.8)
	ax_1 = fig.add_axes(rect=rect, projection=projection)

	rect = (0.48, 0.1, 0.42, 0.8)
	ax_2 = fig.add_axes(rect=rect, projection=projection)

	rect = (0.915, 0.15, 0.02, 0.7)
	cax = fig.add_axes(rect=rect)

	kwargs = {}
	kwargs.setdefault("interpolation", "nearest")
	kwargs.setdefault("origin", "lower")
	kwargs.setdefault("cmap", "afmhot")
	kwargs.setdefault("vmin", -2)
	kwargs.setdefault("vmax", 14)

	sqrt_ts_1 = maps.sqrt_ts.get_image_by_idx((0,))
	im = ax_1.imshow(sqrt_ts_1.data, **kwargs)
	ax_1.set_title("Energy 10 GeV - 60 GeV")
	lon, lat = ax_1.coords["glon"], ax_1.coords["glat"]
	lon.set_axislabel("Galactic Longitude")
	lat.set_axislabel("Galactic Latitude")
	lon.set_ticks_position('b')
	lat.set_ticks_position('l')

	sqrt_ts_2 = maps.sqrt_ts.get_image_by_idx((1,))
	im = ax_2.imshow(sqrt_ts_2.data, **kwargs)
	ax_2.set_title("Energy 60 GeV - 2000 GeV")
	lon, lat = ax_2.coords["glon"], ax_2.coords["glat"]
	lon.set_axislabel("Galactic Longitude")
	lat.set_axislabel("Galactic Latitude")
	lon.set_ticks_position('b')
	lat.set_ticks_position('r')
	lon.set_ticks([5, 0, 355, 350] * u.deg)
	lon.set_major_formatter("dd")

	cbar = fig.colorbar(im, cax=cax, label="sqrt(TS)")
	plt.savefig("../poster/figures/fermi-gc-sqrt-ts.pdf", dpi=300)


if __name__ == "__main__":
	# dataset = read_dataset()
	# maps = estimate_ts_map(dataset=dataset)
	# maps.write("data/fermi-ts-maps.fits")

	maps = FluxMaps.read("data/fermi-ts-maps.fits")
	plot_sqrt_ts_maps(maps=maps)
