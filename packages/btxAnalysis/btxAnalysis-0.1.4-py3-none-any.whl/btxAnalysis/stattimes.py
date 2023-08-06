# -*- coding: utf-8 -*-
"""Time utilities for statistiques."""
from typing import Tuple, Sequence, Dict, Optional
import re

from pandas import Timedelta, Series, DataFrame, Timestamp

from btxAnalysis.statcons import PFMT


def gbk(by_, method_: str = "down"):
    """
    Return a function rounding a ts by_.

    For method see gb_key
    """
    return lambda ts: gb_key(ts, by_, method_)


def gb_key(idx, timeunit, method_="center"):
    """
    Round idx (value of the index) to timeunit.
    works with Indexes

    -method_: down up or center, method to round
    """
    if timeunit[-1] == "m":
        timeunit = f"{int(timeunit[:-1]) * 60}s"

    _rts = idx.round(timeunit)
    if method_ == "down":
        if _rts > idx:
            return _rts - Timedelta(timeunit)
    if method_ == "up":
        if _rts < idx:
            return _rts + Timedelta(timeunit)
    return _rts


def get_rounded_ts(tsi_, by_="5m", method_: str = "down"):
    """
    Return the timestamp index (tsi_) rounded by_.

    - center: Select the rounding method (see gb key)
    """
    return Series(map(gbk(by_, method_), tsi_), index=tsi_)


def format_ts(ts_, by_="1W"):
    """Format the  to by_ resolution."""
    assert by_[-1] in PFMT.keys(), f"by={by_} not in periode format keys {PFMT.keys()}."

    return ts_.strftime(PFMT[by_[-1]])


def ts_extent(ref_, as_unix_ts_=False):
    """
    Return extrems of a iterable.
    if a dataframe is passed to ref_ return the extent of its index
    if as_unix_ts is True, suppors the iterable avec a timestamp method
    """
    _idx = ref_.index if isinstance(ref_, DataFrame) else ref_

    tsh = _idx[0], _idx[-1]
    if not as_unix_ts_:
        return tsh
    else:
        # assert
        return list(map(lambda x: int(x.timestamp()), tsh))


def add_default_ts_round_columns(data_: DataFrame, by_=None, round_=True) -> Tuple:
    """
    Add a column with rounded ts index by default to data_.

    data_ should have ts index
    Return a tuple with the data and the added column name.
    """
    if by_ is None:
        by_ = "1h"
    tsName = f"ts{by_}_down"
    data_.loc[:, tsName] = get_rounded_ts(data_.index, by_, "down")
    return data_, tsName


def get_tsCol_from(data_) -> str:
    """
    Get the ts from on of the data_ columns.

    if defCol is None tries to find a column with ts inside.
    If not possible return False.
    """

    def found_valid(col_):
        return len(col_) > 0

    _defCol: Sequence[str] = [
        c for c in data_.columns if c.startswith("ts") and "_" in c
    ]

    if not found_valid(_defCol):
        # look for rounding name columns
        _defCol = [c for c in data_.columns if c.split("_")[-1].startswith("r")]

    return _defCol[0]


def get_tsby_from_dataCol(data_: DataFrame):
    """Get time unit from the groupby formatted data_.columns."""
    return get_tu_from_dataCol(data_, "ts")


def get_rby_from_dataCol(data_: DataFrame) -> str:
    """Get tu unit from the rolling formatted data_.columns."""
    return get_tu_from_dataCol(data_, "r")


def get_tu_from_dataCol(data_: DataFrame, tuType_: Optional[str] = None) -> str:
    """
    Get tu unit of tuType_ from the the data_.columns.

    - tuType_: r ou ts if None essaye r puis ts
    """
    assert isinstance(data_, DataFrame), f"but type(data_)={type(data_)}."

    if tuType_ is None:
        tu_r = get_tu_from_dataCol(data_, "r")
        return tu_r if tu_r else get_tu_from_dataCol(data_, "ts")

    tUnits = set(
        [
            get_tu_from_(colName)["tu"]
            for colName in data_.columns
            if get_tu_from_(colName)["tutype"] == tuType_
        ]
    )

    assert (
        len(tUnits) <= 1
    ), f"but tUnits={tUnits} colName={data_.columns} et typType_={tuType_}"

    return tUnits.pop() if len(tUnits) == 1 else ""


def get_tu_from_colName(data_: DataFrame):
    """Return the times unit part of a ref_.column.name."""
    assert isinstance(data_, DataFrame), f"but type(data_)={type(data_)}."
    return get_tu_from_(data_.columns.name)["tu"]


def get_tuby_from_dataCol(data_: DataFrame):
    """Get tu unit from the rolling formatted data_.columns."""
    res = {}
    for col in data_.columns:
        _tutype, _tuby = get_tuby_from_(col, tutype_=True)
        res[_tutype] = _tuby

    return res.get("r") if res.get("r", "") else res.get("ts", "")


def get_tuby_from_(mot_: str, tutype_: bool = False):
    """
    Return the times unit part of a ref_.column.name.

    -tutype_: renvois aussi le type du match
    """
    match = get_tu_from_(mot_)
    nb, tu = match["nb"], match["tu"]

    if tutype_:
        return match["tutype"], f"{nb}{tu}"

    return f"{nb}{tu}"


def get_tu_from_(mot_: str) -> Dict[str, str]:
    """Recupère un nombre et une unité de temps du mot_."""
    pat = ".*(?:_|\A)(?P<tutype>r|ts)?(?P<nb>\d+)(?P<tu>[yhmsd])(?:_|\Z).*"
    res = re.match(pat, mot_)
    if res is not None:
        return res.groupdict()

    return {"tutype": "", "nb": "", "tu": ""}


def set_by(by):
    """Convert by timedelta to standard timedelta."""
    return f"{int(by[:-1]) * 60}s" if by.endswith("m") else by


def bys(card=[5, 10, 20], unit="m"):
    """
    Set a defaut resolution triplet.

    use unit and car to change them.
    card should be the list of cardinalities.
    """
    return [f"{x}{unit}" for x in card]


def _cols(ext, bys=bys):
    """
    Define way to write columns with resolution.

    Return columns.
    """
    return [f"{ext}_{b}" for b in bys]


def convert_ts(ts_):
    if isinstance(ts_, str):
        return Timestamp(ts_)
    if isinstance(ts_, Timestamp):
        return ts_
