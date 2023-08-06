# -*- coding: utf-8 -*-
"""Utiles to plot price charts."""
from typing import Sequence, Dict

import matplotlib.pyplot as plt
from pandas import DataFrame, Timedelta, Series, concat
from numpy import array, arange, concatenate, nan
import numpy as np

from btxAnalysis.statistiques import (
    rolling,
    beasts_watch,
    get_the_beasts,
    add_gb_essential,
    beast_crea,
)

from btxAnalysis.statcons import BEASTS, COLORS
from btxAnalysis.statutils import name_rcol, pad_nans
from btxAnalysis.stattimes import get_tu_from_dataCol, get_tsCol_from


def get_boxplot_price_data(
    data_: DataFrame, byRef_=None, aggCols_: Sequence = ("low", "high", "mid_lh")
) -> array:
    """
    Return the data (price) necessary to build a box plot.

    Aggregate the prices in the aggCol_ in on columns of the output array.
    - byRef_ is the criteria to group the data. if None search
    for a colum starting with ts
    - aggCols_ are the columns to aggregage.
    """
    _byRef = get_tsCol_from(data_) if byRef_ is None else byRef_
    assert _byRef, f"Should have byRef but {_byRef} and col {data_.columns}."

    _gb = data_.groupby(_byRef)

    effectifs = _gb.low.count()

    _significatifs = effectifs[effectifs > 3]

    _n, _p = len(_significatifs), max(_significatifs) * len(aggCols_)
    arr = array([nan] * _n * _p)
    arr.shape = (_n, _p)

    for i, gidx in enumerate(_significatifs.index):
        _gp = _gb.get_group(gidx)
        if len(_gp) > 3:
            _val = concatenate([_gp[c].values for c in aggCols_])
            arr[i] = pad_nans(_val, _p)

    return arr.T


def prep_plot_pipes(data_, by_=None):
    """
    Prepare and plot data in pipes.

    if by_ is none get it from data column names.
    """
    by_ = get_tu_from_dataCol(data_) if by_ is None else by_
    gpe = add_gb_essential(data_, by_)
    cbeast = color_pelage(gpe.min_low, gpe.max_high)
    pdata = get_boxplot_price_data(data_)
    _ = plot_pipes(pdata, color_=cbeast.pelage, xticklabels_=gpe.index)


def plot_pipes(data_, color_, xticklabels_, figsize_=(20, 7)):
    """
    Plot colored pipes.

    Also call beast.  The type of beast depend on their color.
    and their color on their variation.
    """
    assert (
        len(data_.T) < 100
    ), f"Want {len(data_.T)} mais ne plot pas plus de 100 boxes."
    fig = plt.figure(figsize=figsize_)

    bplot = fig.gca().boxplot(data_, sym="r.", notch=False, whis=10, patch_artist=True)

    for _patch, _color in zip(bplot["boxes"], color_):
        _patch.set_facecolor(_color)

    for item in fig.gca().xaxis.get_ticklabels():
        item.set_rotation(45)

    _ = fig.gca().set_xticklabels(xticklabels_)

    return bplot


def prepare_for_heatmap(D, col="max_"):
    """
    Return an unstacked datafram ready for heatmap representation.

    Given a dictionnary D with, a pair as a key,
    -- cols is one of min_or max_
    """
    _res = DataFrame(D).T
    _res.columns = ["min_", "max_"]
    #    m = pd.IndexSlice  # for multiIndex
    res = _res.loc[:, col].unstack()

    # sorting the dataframe's indexes
    def convert_to_pddelta(x):
        return (x, Timedelta(x))

    def use_2nd(x):
        return x[1]

    _idx = res.index.map(convert_to_pddelta)
    _cols = res.columns.map(convert_to_pddelta)

    _idx = [x for x, y in sorted(_idx, key=use_2nd)]
    _cols = [x for x, y in sorted(_cols, key=use_2nd)]

    res = res.reindex(_idx)
    res = res.reindex(_cols, axis=1)
    return res


def draw_color_variation(
    data_, methods_=None, by_="5m", beasts_=BEASTS, zero_: str = "sheep"
):
    """Draw several flock in subpots."""
    if methods_ is None:
        methods_ = {"strict": f"min_low_{by_}", "loose": "low"}

    # color code les baisse (bear) et hausse (bull)
    fig, subaxes = plt.subplots(1, 2, figsize=(20, 6))
    for ax_, title_ in zip(subaxes, methods_.keys()):
        _ = draw_flock(data_, ax_, methods_, title_, by_, beasts_, zero_)

    return None


def draw_flock(data_, ax_, methods_, title_, window_, beasts_=BEASTS, zero_="sheep"):
    """Draw a the hull of prices.

    -title_ of the graph
    -window_ the rolling size for rolling curves
    - zero_: to the beast, beers or sheep ?
    """
    _r = rolling(data_, window_)
    BB = get_the_beasts(data_, methods_[title_], window_)
    ax = data_.mid_lh.plot(ax=ax_, style="k--")
    ax = _r.min()["min_low_5m"].plot(ax=ax, style="r")
    ax = _r.min()["min_low_5m"].plot(ax=ax, style="r")

    for _bst in beasts_:
        beast = BB[f"{_bst}"]
        rbeast = BB[f"r{_bst}"]

        if "bear" in _bst:
            ax = beast.mid_lh.plot(ax=ax, style="r_")
            ax = rbeast.min()["low"].plot(ax=ax, style="r,")
        elif "bull" in _bst:
            ax = beast.mid_lh.plot(ax=ax, style="g_")
            ax = rbeast.max()["high"].plot(ax=ax, style="g,")
        elif _bst == "sheep" and zero_ == "sheep":
            ax = beast.mid_lh.plot(ax=ax, style="b.")

    ax.set_title(title_)
    ax.set_xlabel("")

    return ax


def line_plot_price(data_: DataFrame, by_: str = "5m"):
    """
    Plot the prices with rolling max and mins for the data_.

    Should be use with small dataset < 10000 rows.
    -data_ should have high, low columns
    """
    assert (
        len(data_) < 3000
    ), f"len data={len(data_)} >3000\n Attention, si trop de données graphes illisible."
    r = rolling(data_, by_)

    _ = plt.figure(figsize=(14, 6))

    _ax = r.max()["high"].plot(style="g_", label=f"rhigh_{by_}")
    _ax = r.min()["low"].plot(style="r_", ax=_ax, label=f"rlow_{by_}")

    _ax = data_["mid_lh"].plot(ax=_ax)  # 5m price evolution

    # nomage pas clair
    _ax = r.max()[name_rcol("max_high", by_)].plot(
        ax=_ax, style="g:", label="max rhigh"
    )
    _ax = r.min()[name_rcol("max_high", by_)].plot(
        ax=_ax, style="g--", label="min rhigh"
    )

    # asymétrie voulue car apriori bull
    _ax = r.min()[name_rcol("min_low", by_)].plot(ax=_ax, style="r--", label="min rlow")
    _ax = r.max()[name_rcol("min_low", by_)].plot(ax=_ax, style="r:", label="max rlow")

    _ax = data_["low"].plot(ax=_ax, style="r,", markersize=4, label="low")  #
    _ax = data_["high"].plot(ax=_ax, style="g,", markersize=4, label="high")  #

    _ax.legend()
    return _ax


def pipes(data_):
    """Plot pipes."""
    gpe = add_gb_essential(data_)
    beast = color_pelage(gpe.min_low, gpe.max_high)
    pdata = get_boxplot_price_data(data_)
    return plot_pipes(pdata, color_=beast.pelage, xticklabels_=gpe.index)


def plot_beast_percentiles(desc_, obsVar_, periodes_: Sequence = [388, 48, 12, 6]):
    """
    Draw a barplot or beast percentiles amplitudes for each period.

    -desc_ : is a dictionnary or multiIndex Data
    - obsVar the variable to obser
    - periodes en tu des colonnes, ajoute un fond

    Renvois des diagrammes en baton pour chaque période.
    Each bar is for a beast. the hight is the rolling amplitude of the percentile.
    the width represent the % deviation from base distribution
    """
    # description per beast
    BW = beasts_watch(desc_, periodes_)  # beast Watch

    # labels
    labels = list(BW["dragon"].columns)
    # triming non timedelta label
    labels[1:] = [_td.isoformat() for _td in labels[1:]]

    # widths
    _widths = DataFrame({_beast: BW[_beast].loc["count"] for _beast in BEASTS})
    _sum = _widths.sum(axis=1).values

    # normed _widths
    nWidths = DataFrame(
        (_widths.values.T / _sum).T, index=_widths.index, columns=_widths.columns
    )
    nWidths.columns.name = "count"

    _wc = 0.35  # width constante
    widths = nWidths / np.max(nWidths.values) * _wc / 2

    refWidths = DataFrame(index=widths.index, columns=widths.columns)
    refWidths.loc[:, widths.columns] = widths.loc["base"].values

    # values
    values = DataFrame({n: BW[n].loc[obsVar_].values for n in BEASTS}, index=labels)
    values.columns.name = f"{obsVar_} beast amp<"
    values.index.name = "periods"

    # xs
    _barCenter = arange(len(labels))  # the label locations

    fig = plt.figure(figsize=(20, 6))
    ax = fig.gca()

    rects = {}
    for i, (name, beast) in enumerate(BW.items()):
        rects[i] = ax.bar(
            x_pos(i, _barCenter, _wc),
            values[name],
            widths[name],
            label=name,
            color=COLORS[name],
        )
        rects[i] = ax.bar(
            x_pos(i, _barCenter, _wc),
            values[name],
            refWidths[name],
            edgecolor="black",
            fill=False,
        )
    ax.legend()
    for idx, _x in values.loc["base"].items():
        _ = ax.plot(
            _barCenter, [_x] * len(_barCenter), "_", color=COLORS[idx], markersize=140
        )

    ax.set_title(values.columns.name)
    ax.set_xticks(_barCenter)
    ax.set_xticklabels(labels)

    _ = [autolabel(r, ax) for r in rects.values()]

    return rects


def x_pos(pos_, x_, wc_):
    """
    Set position for 4 bars.

    x_: the groupe center position
    wc_: the standard width of a bar
    """
    if pos_ == 0:
        return x_ - wc_ / 2 - wc_ / 4
    if pos_ == 1:
        return x_ - wc_ / 2 + wc_ / 4
    if pos_ == 2:
        return x_ + wc_ / 2 - wc_ / 4
    if pos_ == 3:
        return x_ + wc_ / 2 + wc_ / 4


def autolabel(rects_, ax_):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects_:
        height = rect.get_height()
        ax_.annotate(
            "{}".format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha="center",
            va="bottom",
        )
    return None


def color_pelage(low_: Series, high_: Series) -> DataFrame:
    """Give a color based on low_ high_ columns."""
    n = len(low_)
    assert len(high_) == n

    _df = concat([low_, high_], axis=1)

    _df.loc[:, "low_diff"] = low_.diff()
    _df.loc[:, "high_diff"] = high_.diff()

    for _name in BEASTS:
        _df.loc[:, _name] = beast_crea(_name, low_, high_)

    _df.loc[_df.index[0], "dragon"] = True

    _df.loc[_df.sheep, "pelage"] = "steelblue"
    _df.loc[_df.bull, "pelage"] = "green"
    _df.loc[_df.bear, "pelage"] = "red"
    _df.loc[_df.dragon, "pelage"] = "black"
    return _df


def set_colors_for(cols_: Sequence) -> Dict[str, str]:
    """
    Associate column names with standard COLORS.

    Return a dictionnairy with column name and color.
    """
    return {col: color for col in cols_ for k, color in COLORS.items() if k in col}
    # colors = {}
    # for b, c in COLORS.items():
    #     for col in cols_:
    #         if b in col:
    #             colors[col] = c

    # return colors

