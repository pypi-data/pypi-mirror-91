__all__ = ['Param', 'bool_arg', 'anno_parser', 'args_from_prog', 'call_parse']

# Cell
import inspect,functools,argparse

# Cell
class Param:
    "A parameter in a function used in `anno_parser` or `call_parse`"
    def __init__(self, help=None, type=None, opt=True, action=None, nargs=None, const=None,
                 choices=None, required=None):
        self.help,self.type,self.opt,self.action,self.nargs = help,type,opt,action,nargs
        self.const,self.choices,self.required = const,choices,required

    def set_default(self, d):
        if d==inspect.Parameter.empty: self.opt = False
        else:
            self.default = d
            self.help += f" (default: {d})"

    @property
    def pre(self): return '--' if self.opt else ''
    @property
    def kwargs(self): return {k:v for k,v in self.__dict__.items() if v is not None and k!='opt'}

# Cell
def bool_arg(v):
    "Use as `type` for `Param` to get `bool` behavior"
    if isinstance(v, bool): return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'): return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'): return False
    else: raise argparse.ArgumentTypeError('Boolean value expected.')

# Cell
def anno_parser(func, prog=None, from_name=False):
    "Look at params (annotated with `Param`) in func and return an `ArgumentParser`"
    p = argparse.ArgumentParser(description=func.__doc__, prog=prog)
    for k,v in inspect.signature(func).parameters.items():
        param = func.__annotations__.get(k, Param())
        param.set_default(v.default)
        p.add_argument(f"{param.pre}{k}", **param.kwargs)
    p.add_argument(f"--xtra", help="Parse for additional args", type=str)
    return p

# Cell
def args_from_prog(func, prog):
    "Extract args from `prog`"
    if '##' in prog: _,prog = prog.split('##', 1)
    progsp = prog.split("#")
    args = {progsp[i]:progsp[i+1] for i in range(0, len(progsp), 2)}
    for k,v in args.items():
        t = func.__annotations__.get(k, Param()).type
        if t: args[k] = t(v)
    return args

# Cell
def call_parse(func):
    "Decorator to create a simple CLI from `func` using `anno_parser`"
    mod = inspect.getmodule(inspect.currentframe().f_back)
    if not mod: return func

    @functools.wraps(func)
    def _f(*args, **kwargs):
        mod = inspect.getmodule(inspect.currentframe().f_back)
        if not mod: return func(*args, **kwargs)

        p = anno_parser(func)
        args = p.parse_args()
        xtra = getattr(args, 'xtra', None)
        if xtra is not None:
            if xtra==1: xtra = p.prog
            for k,v in args_from_prog(func, xtra).items(): setattr(args,k,v)
        del(args.xtra)
        func(**args.__dict__)
    if mod.__name__=="__main__":
        setattr(mod, func.__name__, _f)
        return _f()
    else: return _f

