from functools import wraps, partial
from collections import namedtuple
from typing import Union, Tuple, Callable

from anabel import jit
import anabel.ops as anp
# import elle.iterate

Arguments = namedtuple("Arguments", "x,y,state,params")

def kell_no1(
    dim:      Union[int,Tuple[Tuple[int,int]]]=None,
    statevar: str   = "state",
    main:     str   = "main",
    jacx:     str   = None,
    # inv:Callable  = elle.iterate.inv_no1,
    form:     str   = "x,y,s=s,p=p,**e->x,y,s",
    paramvar: str   = "params",
    dimvar:   str   = None,
    origin:   tuple = None, 
    order:    int   = None
) -> Callable:
    """Wraps a basic local map generator.


    This wrapper carries out the following operations:
        
        - adds an `origin` attribute to the generated function according to the
          `dim` specified.

        - adds a `shape` attribute based on dimensions given in `dim`
          
        - adds option to wrapped function to expose closed-over local variables
          as an attribute.
    """


    def _decorator(func: Callable[...,dict]) -> Callable[...,tuple]:

        @wraps(func)
        def wrapper(*args, 
            _expose=False, _jit=False, _form_as:str=None, _curry=False, 
        **kwds) -> Callable:

            loc = func(*args, **kwds)

            if origin is None:
                assert dim is not None
                if isinstance(dim,str):
                    _dim = loc[dim]
                else:
                    _dim = dim
                if isinstance(_dim,int):
                    xshape,yshape = ((_dim, 1), (_dim,1))
                else:
                    xshape, yshape = _dim
                    if isinstance(xshape,int):
                        xshape = (xshape, 1)
                    if isinstance(yshape,int):
                        yshape = (yshape, 1)
                
                shape = (xshape, yshape)
                x0, y0 = anp.zeros(xshape), anp.zeros(yshape)
                _origin = Arguments(x0, y0, loc[statevar], {})

            else:
                if isinstance(origin,str):
                    _origin = loc[origin]
                else:
                    _origin = origin
                shape = _origin[0].shape, _origin[1].shape
            
            if isinstance(main,str):
                _main = loc[main]
            else:
                _main = main

            #-transformations------------------
            # if _form_as is not None:
            #     main = reform(main, form, _form_as)
                
            if _jit:
                _main = jit(_main)
            #----------------------------------
            if _expose:
                _main.closure = loc

#             main.params = loc[paramvar]
            _main.origin = _origin
            _main.shape  = shape

            # __lshift__(self, other)
            
            return _main
            # ~ __invert__
        wrapper.part  = lambda **kwds: partial(wrapper, **kwds)
        return wrapper
    return _decorator

# def reform(func:Callable, form:str, newform:str):
#     old_args, old_out = form.split("->")

#     old_out = old_out.replace(" ","").split(",")


#     new_args, new_out = newform.split("->")
#     new_out = new_out.replace(" ","").split(",")

#     indices = ",".join(old_out.index[new] for new in new_out)

#     return exec(f"def reformed({}): return func({})[{indices}]")









