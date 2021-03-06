""" Python 3D FDTD Simulator """

__author__ = "Floris laporte"
__version__ = "0.0.1"

from .grid import Grid
from .sources import PointSource, LineSource
from .detectors import LineDetector, BlockDetector
from .objects import Object, AbsorbingObject, AnisotropicObject
from .boundaries import PeriodicBoundary, PML
from .backend import backend
from .backend import set_backend
from .visualization import dB_map_2D, plot_detection
