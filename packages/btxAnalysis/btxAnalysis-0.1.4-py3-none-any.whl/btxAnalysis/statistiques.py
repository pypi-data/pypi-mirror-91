# -*- coding: utf-8 -*-
"""
Helper price statistical functions.

Preparing data to get statistics from price data
can use bitmex with btxDataHelper.
"""
from typing import List, Sequence, Dict, Tuple, Optional
from kolaBitMEXBot.kola.utils.general import round_sprice

import logging
import numpy as np
from pandas import (
    DataFrame,
    Series,
    concat,
    Timedelta,
    Index,
    Timestamp,
    date_range,
    MultiIndex,
)

import Ressources.ml_mlk_lib as mlib
import Ressources.btxDataHelper as bdh
from btxAnalysis.statutils import (
    by_f,
    cdr,
    round_series_sprice,
    has_col_with_mid,
    has_col_with_amp,
    has_essential_columns,
    name_rcol,
    prepend_col_name,
    get_initials,
    get_percentiles,
)
from btxAnalysis.stattimes import (
    set_by,
    format_ts,
    get_tuby_from_dataCol,
    get_tuby_from_,
    ts_extent,
    get_tsCol_from,
    add_default_ts_round_columns,
    get_tu_from_dataCol,
)

from btxAnalysis.statcons import BEASTS

logger = logging.getLogger("")
logger.setLevel("INFO")


# types
Df = DataFrame
Ss = Series


def sample(data, cols=["avg", "amplitude"], frac=0.01):
    """
    Sample data triming down to with cols.

    use cols=slice(None) pour avoir toutes les colonnes.
    - data :: le jeu de donnée
    - cols :: les colonnes à subsettés
    - frac :: la portion du jeu de donnée à renvoyer.
    """
    ref = data
    if isinstance(cols, str) and cols.lower() == "all":
        pass
    elif cols:
        ref = data.loc[:, cols]

    ref.columns.name = prepend_col_name(f"s{frac}", ref)

    if frac == 1:
        return ref

    ref = ref.sample(frac=frac).sort_index()
    #    ref.columns.name = prepend_col_name(f"s{frac}", ref)

    return ref


def prepare_data(
    years: Sequence = [2019], bins: str = "1m", dirname="", bname=""
) -> Tuple[DataFrame]:
    """
    Load btxdata for years (as list).

    Add amplitudes and price variation %.
    The first DataFrame returned has the variations the second amplitudes.
    Statistics per days are also computed
    """
    logging.info(f"dirname={dirname}, bname={bname}")
    #    import ipdb; ipdb.set_trace()

    fdf = bdh.load_btxData(years, bins, dirname, bname)
    cols = ["low", "high", "avg"]
    vdf = concat([fdf, bdh.compute_var_in_base_perc(fdf.loc[:, cols])], axis=1)
    vdf.loc[:, "min_abs"] = vdf.loc[:, cols].abs().max(axis=1)
    # La plus grande variation des variations des low et high
    vdf.loc[:, "max_abs"] = vdf.loc[:, cols].abs().min(axis=1)

    # ### Adding amplitude / avg price en %

    vdf["amplitude_per"] = vdf.amplitude / vdf.avg * 100
    cols = [
        "month",
        "weekofyear",
        "dayofyear",
        "day",
        "hour",
        "minute",
        "dayofweek",
        "day_name",
    ]
    vedf = mlib.expand_dtdf(vdf, cols)
    fedf = mlib.expand_dtdf(fdf, cols)

    return vedf, fedf


def last_(x: float, unit: str, data: DataFrame):
    """
    Slice data to keep only the last x time units.

    - x a float: the number of timeunit
    - unit: the time unit for example to 'h', 'd', or 'm' (default)
    """
    timeDelta = Timedelta(x, unit=unit)
    lastTime = data.index[-1]

    rep = data.loc[(lastTime - timeDelta) :, :]
    rep.columns.name = prepend_col_name("l", data)
    return rep


def trunc_start(data_: DataFrame, by_: str):
    """Truncate data_ by removing the first by timedelta records."""
    _by = set_by(by_)
    _timeDelta = Timedelta(float(_by[:-1]), unit=_by[-1])

    init_a, init_b = ts_extent(data_.index)
    new_start_idx = init_a + _timeDelta
    return data_.loc[new_start_idx:init_b]


def ldata_f(data_: DataFrame, a_: float, b_: Optional[float] = None, unit_="h"):
    """Slice data_ on time internale [-a_ -b_] using time unit_."""
    if b_ is not None:
        assert a_ > b_

    _recent = data_.index[-1]
    _end = _recent if b_ is None else _recent - Timedelta(b_, unit=unit_)
    _start = _recent - Timedelta(a_, unit=unit_)

    rep = data_.loc[_start:_end, :]
    rep.columns.name = prepend_col_name("l", data_)

    return rep


def rolling(data: DataFrame, by: str):
    """Rewrite pd.rolling to handle minutes. ex by='5m'."""
    return data.rolling(set_by(by))


def rolling_min_max(data: DataFrame, what="amplitude", by: str = "15m"):
    """
    Compute 'what' on 'data' using 'by' time resolution.

    Groupe the data by 'by' time resolution. 
    Compute for each group the min and max for the what column.
    - what (amplitude or amplitude_per) or pass a function ?
    - by doit être en ts unit reconnu par pandas

    Returns a tuple min, max, and  serie amplitude
    """
    assert isinstance(data, DataFrame), "data needs to be DataFrame but it is {type(data)}"
    assert (
        what in data.columns
    ), "'{what}' that you compute over the rolling {by} window, must be in your data's columns."

    # we update the function to handle list of what
    _whats = [what] if isinstance(what, str) else what

    _by = set_by(by)  # convert minutes to seconds

    # get rolling min and max
    rollMin = data.rolling(_by).min()
    rollMax = data.rolling(_by).max()
    # naming for latter ref.
    rollMin.columns = [f"{c}_min" for c in rollMin.columns]
    rollMax.columns = [f"{c}_max" for c in rollMax.columns]

    R = None
    for i, _what in enumerate(_whats):
        rollAmp = rollMax[f"{_what}_max"] - rollMin[f"{_what}_min"]
        rollAmp.name = f"{_what}_amp"
        if i:
            R = concat([R, rollAmp], axis=1)
        else:
            R = concat([rollMin, rollMax, rollAmp], axis=1)
            R.columns.name = f"{by}"

        if "_per" in _what:
            R.loc[:, f"{_what}_mid"] = (rollMax.high_max + rollMin.low_min) / 2
            R.loc[:, "{_what}_amp_per"] = round(R.amplitude / R.mid * 100, 4)

    _min, _max = None, None
    if isinstance(what, str):
        _min, _max = R.loc[:, rollAmp.name].apply([min, max])

    return _min, _max, R


def compute_min_max_over_span(
    data,
    what="amplitude",
    inspan=[1, 2, 6, 12, 48, 144, 600],
    outspan=[1, 2, 3, 5, 15, 60, 120, 360, 720],
    indexaspddelta=False,
):
    """
    Compute min, max for 'what' rolling over the data for several timespan.

    - inspan: the rolling windows in 'i' minutes
    - outspan: the global time frame. Starting now and going back 'o' hours.
    - indexaspddelta: boolean  transform the index to pd.Delta
    """
    D = {}
    for o in outspan:
        for i in inspan:
            if Timedelta(o, "h") >= Timedelta(i, "m"):
                _, _, A = rolling_min_max(last_(o, "h", data), what, by=f"{i}m")
                what_min_max = A.loc[:, what].apply([min, max])
                if indexaspddelta:
                    D[(Timedelta(f"{o}h"), Timedelta(f"{i}m"))] = what_min_max
                else:
                    D[(f"{o}h", f"{i}m")] = what_min_max
    return D


def get_mid_price(
    data_: DataFrame, key_: str = "low;high", round_: bool = False
) -> DataFrame:
    """
    Return the mid price for the pairs of price defined with key_.

    - key (def. low;high) :: low_high, open_close.
    - round_: to round
    """
    _a, _b = key_.split(";")
    _delta = data_[_b] - data_[_a]
    _mid = data_[_a] + (_delta / 2)
    if round_:
        _mid = round_series_sprice(_mid)
    # index=data_.index, columns=[f'mid_{_abbv}'])
    return DataFrame(_mid)


def add_mid_price_col(
    data_: DataFrame, priceType: str = "low;high", round_=True
) -> DataFrame:
    """Add a mid price column to data."""
    _a, _b = priceType.split(";")
    for c in (_a, _b):
        assert c in data_.columns, f"col {c} not in data_.columns={data_.columns}"

    _suffix = get_initials([_a, _b])
    data_.loc[:, f"mid_{_suffix}"] = get_mid_price(data_, priceType, round_).values
    return data_


def get_diff(df_: DataFrame, key_: str = "low;high", lbl_: str = "diff"):
    """
    Compute the difference of the key_ df_ columns.

    - key_: columns names for which to compute the diff
    - df_: should have only 2 columns.
    - lbl_: lable to make the resulting column name
    - add_: add the diff to original data
    """
    _cols = key_.split("_")
    _abbv = get_initials(_cols)
    _tmp = df_[_cols].diff(axis=1).iloc[:, -1]
    _tmp.name = f"{lbl_}_{_abbv}"
    return DataFrame(_tmp)


def get_the_beasts(data_: DataFrame, priceType_="low;high", window_=None):
    """
    Group the data by beast (bear, bull, dragon and sheeps).

    For each row, check with the previous,
    if priceType:
    - low_diff and high_diff < 0 bull (up)
    - low_diff and high_diff > 0 bear (down)
    - low_diff <0 and high_diff > 0 dragon (expand)
    - else sheep (contract)

    Use the column names to define the aggregation key.
    Returns the beasts and rolling beast
    - by_, if none get it from dataFrame column name.
    used to make the rolling beasts. eg. Check 1h amp_max over
    - priceType_: what 2 columns to use to create Beasts
    - the amp is computed on the rolling low_high,

    It is really the diff of price Type for the aggregated by_.
    """
    _wd = get_tuby_from_(data_.columns.name) if window_ is None else window_

    assert ";" in priceType_, f"Use ';' to separate columsn in '{priceType_}'."
    _low = data_[priceType_.split(";")[0]]
    _high = data_[priceType_.split(";")[1]]

    D = {}
    for _name in BEASTS:
        beast = data_[beast_crea(_name, _low, _high)].copy()
        beast.columns.name = prepend_col_name(_name, beast)
        D[_name] = beast
        D[f"r{_name}"] = rolling(beast, _wd)

    return D


def add_essential(data_: DataFrame) -> DataFrame:
    """Add amplitude and mid price to data from low and high."""
    assert not any(
        [has_col_with_mid(data_), has_col_with_amp(data_)]
    ), f"data_ has already columns with mid or amp. {data_.columns}."
    _data = data_.merge(
        get_essential(data_), left_index=True, right_index=True, suffixes=("", "")
    )
    _data.columns.name = prepend_col_name("!", data_)
    return _data


def get_essential(data_: DataFrame) -> DataFrame:
    """Compute amplitude and mid price from data low and high."""
    assert "low" in data_.columns
    assert "high" in data_.columns

    res = DataFrame(index=data_.index)
    res.loc[:, "amp_lh"] = get_diff(data_).values
    res.loc[:, "mid_lh"] = get_mid_price(data_).values
    res.columns.name = "essential"
    return res


def add_rolling_essential(data_, by_, priceType_="low;high"):
    """Add a rounded by, max, min and amp rolling columns."""
    if not all(has_essential_columns(data_)):
        data_ = add_essential(data_)

    a, b = priceType_.split(";")
    ra, rb = f"min_{a}_r{by_}", f"max_{b}_r{by_}"
    data_.loc[:, ra] = rolling(data_[a], by_).min()
    data_.loc[:, rb] = rolling(data_[b], by_).max()
    data_.loc[:, f"amp_r{by_}"] = data_[rb] - data_[ra]

    # clarifier moyenne des roll ou roll des moyennes...
    # data_.loc[:, f"mean_mid_r{by_}"] = round_series_tod5(
    #     rolling(data_.mid_lh, by_).mean()
    # )

    # trunc data, remove first by columns to optimise approx.
    _a, _b = ts_extent(data_.index)
    data_ = trunc_start(data_, by_)
    data_.columns.name = prepend_col_name(by_, data_)
    logging.debug(
        f"{data_.columns.name} index truncated by {by_}."
        f" From {_a, _b} to {ts_extent(data_.index)}"
    )

    return data_


def add_gb_essential(data_: DataFrame, gbBy_=None) -> DataFrame:
    """
    Groupe the data_ by_ and compute essential columns.

    Does not take care of rolling columns.
    Look for a ts columns to groupby or create it
    min_low, max_high and mean_mid_lh.
    -gbBy_ : should be the name of the column with rounded times,
    where first part is a 'ts'timedelta, or the time unit to group by
    or a method to round (not implemented), if None search for such column name.
    """
    _gbBy = get_tsCol_from(data_) if gbBy_ is None else gbBy_

    if not _gbBy or not _gbBy.startswith("ts"):
        data_, _gbBy = add_default_ts_round_columns(data_, by_=gbBy_)

    if "mid_lh" not in data_.columns:
        data_ = add_mid_price_col(data_, round_=False)

    gb = data_.groupby(f"{_gbBy}")
    gdata = {}

    gdata["mean_mid_lh"] = map(lambda x: round(x, 3), gb.mean()["mid_lh"])
    gdata["min_low"] = gb.min()["low"]
    gdata["max_high"] = gb.max()["high"]

    res = DataFrame(gdata)
    res.columns.name = f"gp{_gbBy[2:].split(';')[0]}_essential"

    return res


def beast_crea(name_: str, low_: Series, high_: Series) -> Series:
    """Return a boolean serie creating the name_d beast."""
    B = {
        "bear": (low_.diff() < 0) & (high_.diff() <= 0),
        "bull": (high_.diff() > 0) & (low_.diff() >= 0),
        "sheep": (low_.diff() >= 0) & (high_.diff() <= 0),
        "dragon": (low_.diff() < 0) & (high_.diff() > 0),
    }
    return B[name_]


def describe_prices(data_, colPrefix_="r1d"):
    """Describe prices."""
    cols_ = [f"{colPrefix_}_{c}" for c in ("min_low", "max_high")]
    return get_stats(data_, cols_, by_=colPrefix_[1:])


def get_stats(
    data_: DataFrame, cols_: List = ["low", "high"], by_: str = "5m"
) -> DataFrame:
    """Ajoute les monstres à data."""
    # faire méchanisme pour trouver ts automatiquement....

    data_.loc[:, "amp_mlmh"] = data_[cols_].diff(axis=1).iloc[:, -1].values
    ndata = data_.loc[:, cols_ + ["amp_mlmh"]]
    ndata.columns = ["low", "high", "amp"]
    ndata.columns.name = f"roll_min_max_{by_}"
    ndata.index.name = "ts"

    # getting the beast !
    for _name in BEASTS:
        mask = beast_crea(_name, ndata.low, ndata.high)
        ndata.loc[mask, "beast"] = _name

    # first toujour a dragon
    ndata.loc[ndata.index[0], "beast"] = "dragon"

    ndata = ndata.set_index("beast", append=True)

    return ndata


def overview(
    beasts_: Dict[str, DataFrame], percentiles_=None, log_=False, round_=-1, by_=None
):
    """
    Give the general statistics for each beast of the data over a windows

    - beasts_: an object from get_the_beasts, ie un tableau à 4 colonnes.
    ~~add a periode attribute to the dataFrame with the periode
    for which it was computed.~~
    - round_: should data be rounded ? défaut -1 (no), 0 -> int, >0, round_prec
    - by_: what is the overview unit.  Should be one of the columns ts unit.
    Return a multiIndex DataFrame
    """
    aBeastName = list(beasts_.keys())[0]
    aBeast = beasts_[aBeastName]
    if log_:
        logging.info(f"Overview: {ts_extent(aBeast.index)}")

    assert isinstance(aBeast, DataFrame) and has_col_with_amp(
        aBeast
    ), f"aBeast={aBeast.head(2)}"

    # get th
    _by = get_tuby_from_(aBeast.columns.name) if by_ is None else by_

    if not _by:
        logging.warning("Using default ts 1h for groupby")
        _by = "1h"

    _tmp = {}

    for _name in BEASTS:
        _beast_data = beasts_[f"r{_name}"].max()[name_rcol("amp", _by)]
        _beast_data.name = f"r{_name}"
        _tmp[_name] = _beast_data

    # import ipdb;    ipdb.set_trace()

    _des = concat(_tmp.values(), axis=1)
    _des.columns = [name_rcol(f"{b}_amp", _by) for b in BEASTS]

    describe = _des.describe(percentiles_)

    describe.loc["skew", :] = _des.skew()
    describe.loc["kurtosis", :] = _des.kurtosis()
    describe.loc["sum", :] = _des.sum()
    describe.loc["count%", :] = _des.count() / len(_des) * 100

    # arrondi pour lecture

    def round_description_val(s_: Series):
        return Series(
            map(lambda x: x if np.isnan(x) else int(x), s_.values), index=s_.index
        )

    if round_ == 0:
        describe = describe.apply(round_description_val, axis=1)
    elif round_ > 0 and isinstance(round_, int):
        logging.info(f"rounding_ by {round_} not implemented.")
    elif round_ < 0:
        pass
    else:
        raise Exception("Wrong rounding attribute.")

    _colName = "_".join(aBeast.columns.name.split("_")[1:])

    describe.columns.name = _colName
    # warning but ok
    # setattr(describe, "periode", ts_extent(aBeast))

    return describe


def recent_analyse(
    data_: DataFrame,
    col_: str = "amp_r388h",
    periodes_: Sequence = [388, 48, 12, 6],
    tu_=None,
):
    """
    Return data_ percentiles for periode.

    -tu_ default time unite.  If None,
    data_ should have the periode time unit in its columns name
    """
    _D = {"base": data_.describe()[col_]}

    _tuby = get_tuby_from_dataCol(data_) if tu_ is None else tu_

    for period_ in periodes_:
        _by = set_by(by_f(period_, _tuby))
        _start = float(_by[:-1])

        _D[Timedelta(_by)] = ldata_f(data_, a_=_start, unit_=_by[-1]).describe()[col_]

    res = DataFrame(_D)
    res.columns.name = f"{tu_}_d"  # d for description
    res = res.apply(lambda x: round(x), axis=1)

    return res


def beasts_watch(
    theBeasts_: Dict[str, DataFrame], periodes_: Sequence = [388, 48, 12, 6], tu_=None,
):
    """
    Return data_ percentiles over each of the periodes and for each beast.

    - tu_: default time unite. If None,
    - data_: should have the periode time unit in its columns name
    - theBeasts_ a dictionnaire de DataFrame issue de get_the_beasts.
    """
    _eg = theBeasts_["dragon"]
    _by = get_tuby_from_dataCol(_eg) if tu_ is None else tu_
    _col = f"amp_r{_by}"

    BC = {}
    for name, beast in [
        (n, b) for (n, b) in theBeasts_.items() if not n.startswith("r")
    ]:
        _beasts_watch = recent_analyse(beast, col_=_col, periodes_=periodes_, tu_=tu_)
        _beasts_watch.name = f"{name}_{_by}"
        BC[name] = _beasts_watch

    return BC


def observe_var_through(
    data_: DataFrame,
    windows_: Sequence = [600, 388, 244, 120, 60, 24],
    obsVar_: str = "75%",
    tu_="1h",
    log_=False,
):
    """
    Compute a descriptive stastic for each beast with data_ for windows_.

    Renvois la réparttion des obsVar amplitudes?? par beast et
    sur les périodes windows.

    - data_: should be a beast dictionnary
    - windows_: a serie of window. A window is used in computing rolling statistic.
    eg 288 will use rolling 288 window to compute the max amp.
    does this from the start of the ts (index- window size,
    to even data effecif in each window) to the end.

    - tu_: the time unit of the periodes.  Multiple the periods by tu_ to get
    the groupby time criteria
    - obsVar_:  the descriptive statistic. Must be a column of the description df.
    Return a table with the obsVar computed for beast_ and periods.
    """
    # à regrouper
    _T = {}
    obsVar = "75%"  # 'count%'
    for _p in windows_:
        _wd = by_f(_p, tu_)
        theBeasts = get_the_beasts(data_, "low;high", window_=_wd)
        _describe = overview(theBeasts, log_=log_)
        _describe.columns = ["_".join(c.split("_")[:-1]) for c in _describe.columns]
        _T[_p] = _describe.loc[obsVar]

    T = DataFrame(_T)
    T.columns = Index([f"{by_f(_p, tu_)}" for _p in windows_])
    T.columns.name = f"{obsVar}_d"
    Tp = T / T.sum(axis=0)

    return Tp


def choped_overview(
    beasts_: Dict[str, DataFrame],
    from_: Timestamp = None,
    to_: Timestamp = None,
    perc_: Optional[Sequence] = None,
    log_=False,
    round_=-1,
):
    """
    Give the general statistics for each beast on a period of time.

    - data: an object from get_the_beasts.
    - from_: the start of the time periode to look at
    - to_: the end of the time periode to look at
    - perc_: the percentail to compute.  If None does standar.
    - should be a sequence between 0 and 1
    - round_: should we round output to int to ease reading
    negative value no rounding, >0 used set round precision.
    if 0 return an int if possible.
    """
    assert isinstance(round_, int)

    aBeastName = list(beasts_.keys())[0]
    aBeast = beasts_[aBeastName]
    _extent = ts_extent(aBeast.index)  # get date range

    # do a wrapper to handle different input types
    _from = _extent[0] if from_ is None else from_
    _to = _extent[1] if to_ is None else to_

    if log_:
        logging.info(f"Overview: _from={_from} _to={_to}")

    assert has_col_with_amp(aBeast)

    # try to gess time groupy by looking at columns
    _tu = get_tuby_from_dataCol(aBeast)
    if not _tu:
        logging.warning("Using default ts 1h for groupby")
        _tu = "1h"

    _tmp = {}
    for _name in BEASTS:
        _beast_data = beasts_[f"r{_name}"].max()[name_rcol("amp", _tu)]
        _beast_data.name = f"r{_name}"
        _tmp[_name] = _beast_data.loc[_from:_to]

    _des = concat(_tmp.values(), axis=1)
    _des.columns = [name_rcol(f"{b}_amp", _tu) for b in BEASTS]

    # describe what has been reduce to times from_to

    describe = _des.describe(perc_)

    describe.loc["skew", :] = _des.skew()
    describe.loc["kurtosis", :] = _des.kurtosis()
    describe.loc["sum", :] = _des.sum()
    describe.loc["count%", :] = _des.count() / len(_des) * 100

    # arrondi pour lecture
    def _round_description_val(s_: Series):
        def _filter_nan(x_):
            if np.isnan(x_):
                return x_
            elif round_ == 0:
                return int(x_)
            else:
                return round(float(x_), round_)

        return Series(map(_filter_nan, s_.values), index=s_.index)

    if round_ >= 0:
        describe = describe.apply(_round_description_val, axis=1)

    _colName = "_".join(aBeast.columns.name.split("_")[1:])
    describe.columns.name = _colName
    # setattr(describe, "periode", (_from, _to))
    return describe


def rolling_choped_overview(
    beasts, start_=None, end_=None, step_="1d", asDf_=False, log_=False
):
    """
    Do a rolling choped overview of the beasts.

    - step_: how to chop the start_ en_d range.
    - as asDf_: return a multiindex Dataframe

    voir overview
    Return a dictionnary of overview DataFrame keyed by start_
    """
    # import ipdb; ipdb.set_trace()

    start, end = ts_extent(beasts["bull"])
    if start_ is not None:
        start = start_
    if end_ is not None:
        end = end_

    idx_range = date_range(start, end, freq=step_)

    _RCO = {}
    for i, (start, end) in enumerate(zip(idx_range[:-1], idx_range[1:])):
        # assert 1W > beast resolution 1d
        CO = choped_overview(beasts, from_=start, to_=end, log_=log_)
        _key = f"{format_ts(start, by_=step_)}"
        _RCO[_key] = CO
        if log_:
            print(f"{round(i/len(idx_range[:-1])*100)}% {_key}", end="\r")

    if asDf_:
        RCO = DataFrame(
            index=MultiIndex.from_product([_RCO.keys(), CO.index]), columns=CO.columns
        )
        for idx, _df in _RCO.items():
            RCO.loc[(idx, _df.index), _df.columns] = _df.values

        def _format_ts(ts):
            return format_ts(ts, step_)

        start, end = map(_format_ts, [idx_range[0], idx_range[-1]])
        RCO.index.rename([f"{step_}_period", CO.columns.name], inplace=True)
        RCO.columns.name = f"{'_'.join([start, end])}"
    else:
        return _RCO
    return RCO


def change_below(serie_: Series, perc_=0.5, asDf_=False, log_=False, returnX_=False):
    """
    Return the time statistiques for variation in data_ by_.

    C'est à dire le temps à attendre en moyenne pour avoir une valeur
    'below' ou 'above' percentile perc_.
    Cette fonction renvoie des groupes dont les pipes sont consécutivement above
    ou below.  Donne le nombre de ses d'éléments

    - serie: the data
    - x: the float in (0,1) to denote percentile
    - asDf_: return a DataFrame
    - returnX_: return the value associated with perc_.
    """
    if perc_ is None:
        perc_ = 0.5

    if isinstance(perc_, float):
        perc_ = round(perc_, 4)
        assert perc_ < 1 and perc_ > 0
        perctl = f"{int(round(perc_*100))}%"
        try:
            x = serie_.describe([perc_])[perctl]
        except KeyError:
            # pb d'arrondi de 0 ou pas
            if "." in perctl:
                perctl = f"{perctl.split('.')[0]}%"
            else:
                perctl = f"{perctl[:-1]}.0%"

            x = serie_.describe([perc_])[perctl]
        except Exception as ex:
            raise (ex)

    else:
        raise Exception(f"Check x {perc_} type")

    if log_:
        logging.info(
            f"Checking time necessary to get above or below" f" percentile {perctl}={x}"
        )

    below = Series(serie_ < x, name=f"change_below_p{perc_}")
    gpID = below.diff().cumsum()

    # les groupes en dessous au dessus dépend du status du premier et
    # ensuite alternent
    if below[0]:
        belowIdx = gpID.isin(range(int(gpID.max()) + 1)[::2])
        aboveIdx = gpID.isin(range(int(gpID.max()) + 1)[1::2])
    else:
        aboveIdx = gpID.isin(range(int(gpID.max()) + 1)[::2])
        belowIdx = gpID.isin(range(int(gpID.max()) + 1)[1::2])

    change = (below != below.shift()).cumsum()
    change.name = f"gp_let_amp{round(x)}"

    _data = concat([serie_, below, change], axis=1)

    B = _data.loc[belowIdx].groupby(change.name).count().loc[:, below.name]
    A = Series(
        _data.loc[aboveIdx].groupby(change.name).count().loc[:, below.name],
        name=f"no_{B.name}",
    )

    res_ = {f"below": B, f"above": A}
    if asDf_:
        res = DataFrame(res_)
        res.columns.name = f"{serie_.name}_p{perctl}"
        return res, x if returnX_ else res
    else:
        return res_, x if returnX_ else res_


def change_below_multi(data_: DataFrame, log_=False, name_=None):
    """
    Compute stats for changes below for several percentiles of amplitude.

    get the rolling ts from columns names
    -data_, what should be looked at.  should containe a minute index
    - see change_below
    # permet les amplitudes en fonction des durées sur le marché visée
    # trouver la valeur en fonction du temps d'attente median
    # plot le temps médian pour diff. perc_...
    - name to give to new dataFrame index
    """
    # basic description index
    didx = Index(["count", "mean", "std", "min", "25%", "50%", "75%", "max"])
    _serie = data_[name_rcol("amp", get_tu_from_dataCol(data_))]

    percentiles = list(map(lambda x: round(x, 2), np.arange(0.05, 0.96, 0.01)))
    mi = MultiIndex.from_product([percentiles, didx], names=["perc_amp", "stats"])

    CBS = DataFrame(None, index=mi, columns=["duree_below", "duree_above"])
    CBS.columns.name = data_.columns.name
    _D = {}  # dictionnary to translate amp. percentile in amp.values

    for i, _p in enumerate(percentiles):

        print(f"{round(i/len(percentiles)*100)}%", end="\r")

        _CB, _amp = change_below(_serie, perc_=_p, asDf_=True, log_=log_, returnX_=True)
        CBS.loc[(_p, didx), :] = _CB.describe()[["below", "above"]].values
        _D[_p] = max(_D.get(_p, 0), _amp)

    # adding value corresponding to percentiles
    CBS = CBS.swaplevel().reset_index()
    CBS.loc[:, "per_val"] = CBS.perc_amp.apply(lambda p: _D[p])
    CBS = CBS.set_index("stats", append=True)

    return CBS


def get_ovw_column(data_: DataFrame, beasts_="_".join(BEASTS)) -> List[str]:
    """Renvoie les colone de data_ qui contienent one of beasts_."""
    _beasts = beasts_.split("_")
    colNames = overview(data_).columns

    return [col for col in colNames for b in _beasts if b in col]


def get_percentile_overview(beasts_, step_=0.5, max_name="99%"):
    """
    Renvois la matrice descriptive avec uniquement les pourcentiles.

    -step_: step of pourcentiles.
    - max_name si None, elude le max
    """
    perc = get_percentiles(step_)
    exclIndex = set(
        ["count", "mean", "skew", "kurtosis", "sum", "count%", "std", "min", "max"]
    )
    OV = overview(beasts_=beasts_, percentiles_=perc)

    commonToCol, reducedColNames = factor_ovw_colNames(beasts_)
    OV.columns = Index(reducedColNames, name=f"{OV.columns.name}_{commonToCol}")

    keepIdx = Index(set(OV.index) - exclIndex)

    _OV = OV.loc[keepIdx].sort_index()

    # pad index with 0 index
    _OV.loc[:, "pcl"] = [f"{float(c[:-1]):#03.0f}%" for c in list(_OV.index)]
    _OV = _OV.set_index("pcl").sort_index()
    # add max
    if max_name is not None:
        _OV.loc[max_name] = _OV.max()

    _OV.index.name = "pcl"
    return _OV


def factor_ovw_colNames(beasts_: Dict[str, DataFrame]) -> Tuple[str, List[str]]:
    """
    Factor the overview columns names of beasts.
    
    return the common part and the column names without
    the common part
    """
    colNames = get_ovw_column(beasts_)
    commonToCol = cdr(colNames[0], "_")
    reducedCols = [c.replace(f"_{commonToCol}", "") for c in colNames]

    return commonToCol, reducedCols
