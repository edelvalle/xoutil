from __future__ import absolute_import as _
import warnings

warnings.warn('xoutil.six is deprecated, use six directly. xoutil.six will be'
              ' removed in 1.7.0', stacklevel=2)

from six import *
from six import moves

moves = sys.modules[__name__ + ".moves"] = moves
