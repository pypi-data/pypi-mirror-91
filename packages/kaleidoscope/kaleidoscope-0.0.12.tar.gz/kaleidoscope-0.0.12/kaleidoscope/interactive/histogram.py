# -*- coding: utf-8 -*-

# This code is part of Kaleidoscope.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# The Hamming distance and internal plot histogram data are part of
# Qiskit.  The latter will be modified at some point.

"""Interactive histogram from experiment counts"""

import functools
from collections import Counter, OrderedDict
import numpy as np
import plotly.graph_objects as go
from kaleidoscope.errors import KaleidoscopeError
from kaleidoscope.colors import COLORS1, COLORS2, COLORS3, COLORS4, COLORS5, COLORS14
from kaleidoscope.colors.utils import find_text_color
from .plotly_wrapper import PlotlyWidget, PlotlyFigure


def hamming_distance(str1, str2):
    """Calculate the Hamming distance between two bit strings

    Args:
        str1 (str): First string.
        str2 (str): Second string.
    Returns:
        int: Distance between strings.
    Raises:
        ValueError: Strings not same length
    """
    if len(str1) != len(str2):
        raise ValueError('Strings not same length.')
    return sum(s1 != s2 for s1, s2 in zip(str1, str2))


VALID_SORTS = ['asc', 'desc', 'hamming']
DIST_MEAS = {'hamming': hamming_distance}


def probability_distribution(data, figsize=(None, None), colors=None,
                             number_to_keep=None,
                             sort='asc', target_string=None,
                             legend=None, bar_labels=True,
                             state_labels_kind='bits',
                             state_labels=None,
                             title=None,
                             plot_background_color='#e5e0df',
                             background_color='#ffffff',
                             as_widget=False):
    """Interactive histogram plot of probability distributions.

    Parameters:
        data (list or dict): This is either a list of dictionaries or a single
            dict containing the values to represent (ex {'001': 130})
        figsize (tuple): Figure size in pixels.
        colors (list or str): String or list of strings for histogram bar colors.
        number_to_keep (int): The number of terms to plot and rest
            is made into a single bar called 'rest'.
        sort (string): Could be 'asc', 'desc', or 'hamming'.
        target_string (str): Target string if 'sort' is a distance measure.
        legend(list): A list of strings to use for labels of the data.
            The number of entries must match the length of data (if data is a
            list or 1 if it's a dict)
        bar_labels (bool): Label each bar in histogram with probability value.
        state_labels_kind (str): 'bits' (default) or 'ints'.
        state_labels (list): A list of custom state labels.
        title (str): A string to use for the plot title.
        plot_background_color (str): Set the background color behind histogram bars.
        background_color (str): Set the background color for axes.
        as_widget (bool): Return figure as an ipywidget.

    Returns:
        PlotlyFigure or PlotlyWidget:
            A figure for the rendered histogram.

    Raises:
        ValueError: When legend is provided and the length doesn't
                    match the input data.
        ImportError: When failed to load plotly.
        KaleidoscopeError: When state labels is not correct length.

    Example:
        .. jupyter-execute::

            from qiskit import *
            import kaleidoscope.qiskit
            from kaleidoscope.qiskit.services import Simulators
            from kaleidoscope.interactive import probability_distribution

            sim = Simulators.aer_vigo_simulator

            qc = QuantumCircuit(3, 3) >> sim
            qc.h(1)
            qc.cx(1,0)
            qc.cx(1,2)
            qc.measure(range(3), range(3))

            counts = qc.transpile().sample().result_when_done()
            probability_distribution(counts)
    """

    if sort not in VALID_SORTS:
        raise ValueError("Value of sort option, %s, isn't a "
                         "valid choice. Must be 'asc', "
                         "'desc', or 'hamming'")
    if sort in DIST_MEAS.keys() and target_string is None:
        err_msg = 'Must define target_string when using distance measure.'
        raise ValueError(err_msg)

    if isinstance(data, dict):
        data = [data]

    if legend and len(legend) != len(data):
        raise ValueError("Length of legendL (%s) doesn't match "
                         "number of input executions: %s" %
                         (len(legend), len(data)))

    text_color = find_text_color(background_color)

    labels = list(sorted(
        functools.reduce(lambda x, y: x.union(y.keys()), data, set())))
    if number_to_keep is not None:
        labels.append('rest')

    if sort in DIST_MEAS.keys():
        dist = []
        for item in labels:
            dist.append(DIST_MEAS[sort](item, target_string))

        labels = [list(x) for x in zip(*sorted(zip(dist, labels),
                                               key=lambda pair: pair[0]))][1]

    # Set bar colors
    if colors is None:
        if len(data) == 1:
            colors = COLORS1
        elif len(data) == 2:
            colors = COLORS2
        elif len(data) == 3:
            colors = COLORS3
        elif len(data) == 4:
            colors = COLORS4
        elif len(data) == 5:
            colors = COLORS5
        else:
            colors = COLORS14
    elif isinstance(colors, str):
        colors = [colors]

    width = 1/(len(data)+1)  # the width of the bars

    labels_dict, all_pvalues, _ = _plot_histogram_data(data,
                                                       labels,
                                                       number_to_keep)

    fig = go.Figure()
    for item, _ in enumerate(data):
        xvals = []
        yvals = []
        for idx, val in enumerate(all_pvalues[item]):
            xvals.append(idx+item*width)
            yvals.append(val)

        labels = list(labels_dict.keys())
        if state_labels_kind == 'ints':
            labels = [int(label, 2) for label in labels]
        if state_labels:
            if len(state_labels) != len(labels):
                raise KaleidoscopeError('Number of input state labels does not match data.')
            labels = state_labels

        hover_template = "<b>{x}</b><br>P = {y}"
        hover_text = [hover_template.format(x=labels[kk],
                                            y=np.round(yvals[kk], 3)) for kk in range(len(yvals))]

        fig.add_trace(go.Bar(x=xvals,
                             y=yvals,
                             width=width,
                             hoverinfo="text",
                             hovertext=hover_text,
                             marker_color=colors[item % len(colors)],
                             name=legend[item] if legend else '',
                             text=np.round(yvals, 3) if bar_labels else None,
                             textposition='auto'
                             ))

    xaxes_labels = list(labels_dict.keys())
    if state_labels_kind == 'ints':
        xaxes_labels = [int(label, 2) for label in xaxes_labels]
    if state_labels:
        if len(state_labels) != len(xaxes_labels):
            raise KaleidoscopeError('Number of input state labels does not match data.')
        xaxes_labels = state_labels

    fig.update_xaxes(title='Basis state',
                     titlefont_size=16,
                     tickvals=list(range(len(labels_dict.keys()))),
                     ticktext=xaxes_labels,
                     tickfont_size=14,
                     showline=True, linewidth=1,
                     linecolor=text_color if text_color == 'white' else None,
                     )

    fig.update_yaxes(title='Probability',
                     titlefont_size=16,
                     tickfont_size=14,
                     showline=True, linewidth=1,
                     linecolor=text_color if text_color == 'white' else None,
                     )

    fig.update_layout(xaxis_tickangle=-70,
                      showlegend=(legend is not None),
                      width=figsize[0],
                      height=figsize[1],
                      plot_bgcolor=plot_background_color,
                      paper_bgcolor=background_color,
                      title=dict(text=title, x=0.5),
                      title_font_size=18,
                      font=dict(color=text_color),
                      )
    if as_widget:
        return PlotlyWidget(fig)

    return PlotlyFigure(fig)


def _plot_histogram_data(data, labels, number_to_keep):
    """Generate the data needed for plotting counts.

    Parameters:
        data (list or dict): This is either a list of dictionaries or a single
            dict containing the values to represent (ex {'001': 130})
        labels (list): The list of bitstring labels for the plot.
        number_to_keep (int): The number of terms to plot and rest
            is made into a single bar called 'rest'.

    Returns:
        tuple: tuple containing:
            (dict): The labels actually used in the plotting.
            (list): List of ndarrays for the bars in each experiment.
            (list): Indices for the locations of the bars for each
                    experiment.
    """
    labels_dict = OrderedDict()

    all_pvalues = []
    all_inds = []
    for execution in data:
        if number_to_keep is not None:
            data_temp = dict(Counter(execution).most_common(number_to_keep))
            data_temp["rest"] = sum(execution.values()) - sum(data_temp.values())
            execution = data_temp
        values = []
        for key in labels:
            if key not in execution:
                if number_to_keep is None:
                    labels_dict[key] = 1
                    values.append(0)
                else:
                    values.append(-1)
            else:
                labels_dict[key] = 1
                values.append(execution[key])
        values = np.array(values, dtype=float)
        where_idx = np.where(values >= 0)[0]
        pvalues = values[where_idx] / sum(values[where_idx])

        all_pvalues.append(pvalues)
        numelem = len(values[where_idx])
        ind = np.arange(numelem)  # the x locations for the groups
        all_inds.append(ind)

    return labels_dict, all_pvalues, all_inds
