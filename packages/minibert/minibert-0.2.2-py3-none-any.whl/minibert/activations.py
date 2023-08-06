import torch
import torch.nn.functional as F


def parse_activation_function(act):
    act = act.strip().lower()
    if act in ("nothing", "none"):
        return lambda x: x
    else:
        f = getattr(torch, act, None)
        if f is None:
            f = getattr(F, act)
        return f
