# -*- coding: utf-8 -*-
"""Stat utilities."""
from typing import List, Sequence, Set, Optional
import logging

from numpy import array, nan, concatenate, arange
from pandas.io.formats.format import format_percentiles
from pandas import DataFrame, Series

from kolaBitMEXBot.kola.utils.general import round_to_d5, round_sprice


def has_col_with_amp(data_: DataFrame) -> bool:
    """Return if a column has 'amp' in its name."""
    return has_column_with(data_, "amp")


def has_col_with_low(data_: DataFrame) -> bool:
    """Return if a column has 'low' in its name."""
    return has_column_with(data_, "low")


def has_col_with_high(data_: DataFrame) -> bool:
    """Return if a column has 'high' in its name."""
    return has_column_with(data_, "high")


def has_col_with_mid(data_: DataFrame) -> bool:
    """Return if a column has 'mid' in its name."""
    return has_column_with(data_, "mid")


def has_column_with(data_: DataFrame, with_) -> bool:
    """Return if a dat_.column has with_ in on of its."""
    return any([c for c in data_.columns if with_ in c])


def has_essential_columns(data_: DataFrame) -> List[bool]:
    """Check that data_ has essential columns."""
    essentialCol = ["low", "high", "amp", "mid"]
    return [has_column_with(data_, _ecol) for _ecol in essentialCol]


def name_rcol(base: str, by_: str) -> str:
    """Format the rolling column name."""
    return f"{base}_r{by_}"


def pad_nans(arr_: array, x_: int) -> array:
    """Pad an arr_ with nan to reach the len of x_."""
    _pad = x_ - len(arr_)
    assert _pad >= 0, f"len(arr)={len(arr_)}, x={x_}"
    nans = array([nan] * _pad)
    return concatenate([arr_, nans])


def round_series_tod5(s_: Series) -> Series:
    """Round the values of a serie to d5."""
    return Series(map(round_to_d5, s_.values), index=s_.index)

def round_series_sprice(s_: Series, symbol_=None) -> Series:
    """Round the values of a serie to d5."""
    _round_sprice = lambda x: round_sprice(x, symbol_)
    return Series(map(_round_sprice, s_.values), index=s_.index)

def prepend_col_name(name_, data_, sep="_"):
    """
    Add name_ to data_.column name without repetition.

    Return the new column names.
    """
    _ocn = data_.columns.name
    _colComp = _ocn.split(sep) if _ocn else []

    return sep.join(uniquify([name_] + _colComp))


def uniquify(seq_: Sequence) -> List:
    """Return the uniq element of seq keeping order."""
    seen: Set[bool] = set()
    return [x for x in seq_ if not (x in seen or seen.add(x))]


def get_initials(cols_: List[str]) -> str:
    """Return the initials of the columns."""
    return "".join(map(lambda c: c[0], cols_))


def by_f(x_: float = 388, tu_: str = "1h") -> str:
    """
    Multiply the time unit tu_ by x.
    
    Values of x could be [388 , 48, 12, 6]
    Returns a standard string that can be used in pd.Timedelta
    """
    return f"{x_*int(tu_[:-1])}{tu_[-1]}"


def amp_f(pdUnitCount_: float = 1, tu_: str = "1h"):
    """Format the period Unit Count column name"""
    return f"amp_r{by_f(pdUnitCount_, tu_)}"


# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/


def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


def forme_percentiles(percs_: List):
    """
    Use pandas format funciton to format percentiles

    see original function's doc.
    """
    return format_percentiles(percs_)


def cdr(expr_, sKey_="_"):
    """Split expr_ if possible and return all but head."""
    parts = expr_.split(sKey_)
    if len(parts) <= 1:
        return ""
    elif len(parts) == 2:
        return parts[-1]

    return sKey_.join(parts[1:])


def cat(expr_, sKey_="_"):
    """Split expr_ with sKey et renvois head."""
    parts = expr_.split(sKey_)
    if len(parts) < 1:
        return ""
    return parts[0]


def get_percentiles(step_: float) -> List[float]:
    """Renvoie les pourcentiles for 0 to 1 with step_ including .5."""
    return sorted(list(set(list(arange(0, 1, step_)) + [0.5])))


def add_col_hierachie(data_: DataFrame, name_: str, levelname_: str = "org"):
    """
    Ajoute un niveau hierachique aux colonnes.

    - levelname: Le nom de se niveau
    - name : nom
    """
    copy_ = data_.copy()
    copy_.loc[:, levelname_] = name_
    return (
        copy_.set_index(levelname_, append=True).unstack(levelname_).swaplevel(axis=1)
    )
