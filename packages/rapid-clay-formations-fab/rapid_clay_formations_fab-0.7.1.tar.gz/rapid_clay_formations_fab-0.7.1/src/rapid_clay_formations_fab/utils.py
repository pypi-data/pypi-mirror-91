"""
********************************************************************************
rapid_clay_formations_fab.utils
********************************************************************************
.. currentmodule:: rapid_clay_formations_fab.utils
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg

try:
    from typing import Any
except ImportError:
    pass


def wrap_list(list_, idx):  # type: (list, int) -> Any
    """Return value at index, wrapping if necessary.

    Parameters
    ----------
    list_ : :class:`list`
        List to wrap around.
    idx : :class:`int`
        Index of item to return in list.

    Returns
    -------
    :class:`list` element
        Item at given index, index will be wrapped if necessary.
    """
    return list_[idx % len(list_)]


def ensure_frame(frame_like):  # type: (Any) -> cg.Frame
    """Convert geometry objects to :class:`compas.geometry.Frame`.

    Parameters
    ----------
    frame_like
        Frame like object, currently :class:`compas.geometry.Frame`,
        :class:`compas.geometry.Plane`, :class:`compas.geometry.Point`,
        :class:`Rhino.Geometry.Plane`, or :class:`Rhino.Geometry.Point3d`.

    Returns
    -------
    :class:`compas.geometry.Frame`

    Notes
    -----
    If a point is given the point is used as the frames origin and the X and
    Y will be the X and Y unit vectors.

    :class:`compas.geometry.Plane` is defined only by origin and normal, the
    X and Y axis will be chosen arbitrarely,
    see :meth:`compas.geometry.Frame.from_plane`.
    """
    if isinstance(frame_like, cg.Frame):
        return frame_like

    if isinstance(frame_like, cg.Plane):
        return cg.Frame.from_plane(frame_like)

    if isinstance(frame_like, cg.Point):
        return cg.Frame(frame_like, [1, 0, 0], [0, 1, 0])

    try:  # try to compare to Rhino objects
        import Rhino.Geometry as rg
        from rapid_clay_formations_fab.rhino import rgplane_to_cgframe
        from rapid_clay_formations_fab.rhino import rgpoint_to_cgpoint

        if isinstance(frame_like, rg.Plane):
            return rgplane_to_cgframe(frame_like)
        if isinstance(frame_like, rg.Point3d):
            pt = rgpoint_to_cgpoint(frame_like)
            return cg.Frame(pt, [1, 0, 0], [0, 1, 0])
    except ImportError:
        pass

    raise TypeError(
        "Can't convert {} to compas.geometry.Frame".format(type(frame_like))
    )
