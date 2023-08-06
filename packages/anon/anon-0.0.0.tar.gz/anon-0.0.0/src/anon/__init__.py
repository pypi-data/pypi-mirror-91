
__version__ = '0.0.0'
# from .version import __version__



try:
    from ._anon import execute_model  # noqa
except ImportError:
    def execute_model(args):
        return max(args, key=len)

try:
    import jaxlib
except ImportError:
    COMPILER = None
else:
    COMPILER = jaxlib


# from .core import *
# import anon.io
import anon.diff
import anon.dual
import anon.quad

# import anabel.ops
