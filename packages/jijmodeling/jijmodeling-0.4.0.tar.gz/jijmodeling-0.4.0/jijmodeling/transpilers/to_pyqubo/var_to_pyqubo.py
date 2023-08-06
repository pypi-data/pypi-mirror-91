from typing import Dict, List, Tuple, Type

import numpy as np
from jijmodeling.variables.variable import Variable, Element
from jijmodeling.variables.placeholders import ArraySizePlaceholder, Placeholder
from jijmodeling.variables.obj_vars import Binary, Spin, DisNum, LogEncInteger, Spin
import pyqubo as pyq


def _var_to_pyqubo(
        term: Variable,
        term_label: str,
        placeholder: dict = {},
        fixed_variables: dict = {},
        fixed_indices: dict = {},
        cache: dict = {}
        ) -> pyq.Base:

    if type(term) == Placeholder:
        return pyq.Placeholder(term_label)
    elif type(term) == Element:
        return fixed_indices[term.label]
    elif type(term) == ArraySizePlaceholder:
        array = term.array.calc_value({}, placeholder, fixed_indices)
        if not isinstance(array, np.ndarray):
            array = np.array(array)
        return array.shape[term.dimension]

    indices = [int(ind.calc_value({}, placeholder, fixed_indices))
               for ind in term.subscripts]

    # Objective variables -----------------------
    if isinstance(term, Binary):
        return pyq.Binary(term_label)
    elif isinstance(term, Spin):
        return pyq.Spin(term_label)

    elif isinstance(term, DisNum):
        upper = term.upper.calc_value({}, placeholder, fixed_indices)
        lower = term.lower.calc_value({}, placeholder, fixed_indices)
        bits = term.bits.calc_value({}, placeholder, fixed_indices)
        if isinstance(term.upper, Variable):
            if term.upper.dim > 0:
                upper = np.array(upper)[tuple(indices)]
        if isinstance(term.lower, Variable):
            if term.lower.dim > 0:
                lower = np.array(lower)[tuple(indices)]
        if isinstance(term.bits, Variable):
            if term.bits.dim > 0:
                bits = np.array(bits)[tuple(indices)]

        var_label = term_label + '[{}]'
        coeff = (upper - lower)/(2**bits - 1)
        return coeff * sum(2**i * pyq.Binary(var_label.format(i))
                           for i in range(bits)) + lower

    elif isinstance(term, LogEncInteger):
        upper = term.upper.calc_value({}, placeholder, fixed_indices)
        lower = term.lower.calc_value({}, placeholder, fixed_indices)
        if isinstance(term.upper, Variable):
            if term.upper.dim > 0:
                upper = np.array(upper)[tuple(indices)]
        if isinstance(term.lower, Variable):
            if term.lower.dim > 0:
                lower = np.array(lower)[tuple(indices)]

        bits = int(np.log2(upper - lower))
        remain_value = upper - lower - (2**bits - 1)
        var_label = term_label + '[{}]'
        pyq_obj = sum(2**i * pyq.Binary(var_label.format(i))
                      for i in range(bits)) + lower
        if remain_value > 0:
            pyq_obj += remain_value * pyq.Binary(var_label.format(bits))
        return pyq_obj

    else:
        raise TypeError("`{}` cannot convert pyqubo object."
              .format(term.__class__.__name__))
