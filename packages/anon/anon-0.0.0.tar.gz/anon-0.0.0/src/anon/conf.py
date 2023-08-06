try:
    from jax.config import *
except:
    pass

_BACKEND = {
    'ops': 'jax',
    'numeric': 'jax'
}

def use(backend, **kwds):
    _BACKEND['ops'] = backend
    _BACKEND['numeric'] = backend





