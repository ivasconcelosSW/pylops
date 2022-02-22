import warnings

import numpy as np

from pylops import LinearOperator
from pylops.utils._internal import _value_or_list_like_to_array


class Roll(LinearOperator):
    r"""Roll along an axis.

    Roll a multi-dimensional array along ``axis`` for
    a chosen number of samples (``shift``).

    Parameters
    ----------
    dims : :obj:`list` or :obj:`int`
        Number of samples for each dimension
    axis : :obj:`int`, optional
        .. versionadded:: 2.0.0

        Axis along which model is rolled.
    dir : :obj:`int`, optional

        .. deprecated:: 2.0.0
            Use ``axis`` instead. Note that the default for ``axis`` is -1
            instead of 0 which was the default for ``dir``.

    shift : :obj:`int`, optional
        Number of samples by which elements are shifted
    dtype : :obj:`str`, optional
        Type of elements in input array.

    Attributes
    ----------
    shape : :obj:`tuple`
        Operator shape
    explicit : :obj:`bool`
        Operator contains a matrix that can be solved explicitly
        (``True``) or not (``False``)

    Notes
    -----
    The Roll operator is a thin wrapper around :func:`numpy.roll` and shifts
    elements in a multi-dimensional array along a specified direction for a
    chosen number of samples.

    """

    def __init__(self, dims, axis=-1, dir=None, shift=1, dtype="float64"):
        if dir is not None:
            warnings.warn(
                "dir will be deprecated in version 2.0.0, use axis instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )
            axis = dir

        self.dims = _value_or_list_like_to_array(dims)
        self.axis = axis
        N = np.prod(self.dims)
        self.shift = shift
        self.shape = (N, N)
        self.dtype = np.dtype(dtype)
        self.explicit = False

    def _matvec(self, x):
        x = np.reshape(x, self.dims)
        y = np.roll(x, shift=self.shift, axis=self.axis)
        return y.ravel()

    def _rmatvec(self, x):
        x = np.reshape(x, self.dims)
        y = np.roll(x, shift=-self.shift, axis=self.axis)
        return y.ravel()
