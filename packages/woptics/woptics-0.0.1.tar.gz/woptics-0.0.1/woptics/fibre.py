__all__ = ["step_index", "grin"]

import numpy as np


class step_index(object):
    """A step-index multimode fibre.

    The fibre is assumed to be perfectly straight and aligned perfectly
    with the discretization of the grid.
    Fibre assumed to have infinite cladding radius.

    Note that `n_core` **must** be larger than `n_clad`

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(
        self,
        n_core=None,
        n_cladding=None,
        numerical_aperture=None,
        length=None,
        radius=None,
    ):
        """
        Parameters
        ----------
        n_core : float
            Refractive index of the core.
        n_cladding : float
            Refractive index of the cladding.
        numerical_aperture: float
            Numerical aperure of fibre.
        length : float
            Fibre length, in metres.
        radius : float
            Fibre core radius, in metres.
        """
        self.length = length
        self.n_core = n_core
        self.n_cladding = n_cladding
        self.numerical_aperture = numerical_aperture
        self.length = length
        self.radius = radius

    def __call__(self, field):
        """Propogates field in real-space to far end of optical fibre."""
        pass

    def __str__(self):
        return f"{self.num_modes} step-index mmf"


class grin(object):
    raise NotImplementedError()
