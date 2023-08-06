from autolens.plot.mat_wrap import plotter
from test_autolens.simulators.imaging import instrument_util

# In this tutorial, we'll introduce a new pixelization, called an adaptive-pixelization. This pixelization doesn't use
# uniform grid of rectangular pixels, but instead uses ir'Voronoi' pixels. So, why would we want to do that?
# Lets take another look at the rectangular grid, and think about its weakness.

# Lets quickly remind ourselves of the image, and the 3.0" circular mask we'll use to mask it.
imaging = instrument_util.load_test_imaging(
    dataset_name="light_sersic__source_sersic", instrument="vro"
)
array = imaging.image

mask = al.Mask2D.elliptical(
    shape=imaging.shape_2d,
    pixel_scales=imaging.pixel_scales,
    major_axis_radius=6.0,
    axis_ratio=0.5,
    phi=0.0,
    centre=(0.0, 0.0),
)
aplt.Array(array=array, mask=mask, positions=[[(1.0, 1.0)]], centres=[[(0.0, 0.0)]])

imaging = instrument_util.load_test_imaging(
    dataset_name="mass_sie__source_sersic__offset_centre", instrument="vro"
)
array = imaging.image

mask = al.Mask2D.elliptical(
    shape=imaging.shape_2d,
    pixel_scales=imaging.pixel_scales,
    major_axis_radius=6.0,
    axis_ratio=0.5,
    phi=0.0,
    centre=(1.0, 1.0),
)
aplt.Array(array=array, mask=mask, positions=[[(2.0, 2.0)]], centres=[[(1.0, 1.0)]])
aplt.Array(array=array, mask=mask, positions=[[(2.0, 2.0)]], centres=[[(1.0, 1.0)]])
