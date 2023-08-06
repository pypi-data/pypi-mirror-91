
# from anon.conf import _BACKEND 

# backend = _BACKEND['ops']
backend = ["jax"]

if 'jax' in backend:
    from jax.numpy import *

elif 'numpy' in backend:
    from numpy import *

