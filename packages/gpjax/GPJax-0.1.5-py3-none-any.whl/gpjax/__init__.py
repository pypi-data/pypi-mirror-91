from jax.config import config
config.update("jax_enable_x64", True)
from .kernel import RBF
from .likelihoods import Gaussian
from .mean_functions import ZeroMean
from .utilities import save, load
from . import gps

__version__ = "0.1.5"
