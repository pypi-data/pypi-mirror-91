# -*- coding: utf-8 -*-

# This file is part of Kaleidoscope.
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
# pylint: disable=invalid-unary-operand-type

"""CNOT error density plot"""

import numpy as np
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.pyplot as plt
from qiskit.providers.models.backendproperties import BackendProperties
from kaleidoscope.colors import COLORS1, COLORS2, COLORS3, COLORS4, COLORS5, COLORS14
from kaleidoscope.errors import KaleidoscopeError
from kaleidoscope.qiskit.backends.pseudobackend import properties_to_pseudobackend


def cnot_error_density(backends,
                       figsize=None,
                       colors=None,
                       offset=None,
                       scale='log',
                       covariance_factor=0.1,
                       xlim=None,
                       text_xval=None,
                       xticks=None):
    """Plot CNOT error distribution for one or more IBMQ backends.

    Parameters:
        backends (list or IBMQBackend or BackendProperties): A single or ist of IBMQBackend
                                                             instances or properties.
        figsize (tuple): Optional figure size in inches.
        colors (list): A list of Matplotlib compatible colors to plot with.
        offset (float): Positive offset for spacing out the backends.
        scale (str): 'linear' or 'log' scaling of x-axis.
        covariance_factor (float): Sets the width of the gaussian for each point.
        xlim (list or tuple): Optional lower and upper limits of cnot error values.
        text_xval (float): Optional xaxis value at which to start the backend text.
        xticks (list): Optional list of xaxis ticks to plot.

    Returns:
        Figure: A matplotlib Figure instance.

    Raises:
        KaleidoscopeError: A backend with < 2 qubits was passed.
        KaleidoscopeError: Number of colors did not match number of backends.

    Example:
        .. jupyter-execute::

            from qiskit import *
            from kaleidoscope.qiskit.backends import cnot_error_density
            provider = IBMQ.load_account()

            backends = []
            backends.append(provider.backends.ibmq_vigo)
            backends.append(provider.backends.ibmq_ourense)
            backends.append(provider.backends.ibmq_valencia)
            backends.append(provider.backends.ibmq_santiago)

            cnot_error_density(backends)
    """

    if not isinstance(backends, list):
        backends = [backends]

    for idx, back in enumerate(backends):
        if isinstance(back, BackendProperties):
            backends[idx] = properties_to_pseudobackend(back)

    for back in backends:
        if back.configuration().n_qubits < 2:
            raise KaleidoscopeError('Number of backend qubits must be > 1')

    if scale not in ['linear', 'log']:
        raise KaleidoscopeError("scale must be 'linear' or 'log'.")

    # Attempt to autosize if figsize=None
    if figsize is None:
        if len(backends) > 1:
            fig = plt.figure(figsize=(12, len(backends)*1.5))
        else:
            fig = plt.figure(figsize=(12, 2))
    else:
        fig = plt.figure(figsize=figsize)

    text_color = 'k'
    if offset is None:
        offset = 100 if len(backends) > 3 else 200
    offset = -offset
    if colors is None:
        if len(backends) == 1:
            colors = COLORS1
        elif len(backends) == 2:
            colors = COLORS2
        elif len(backends) == 3:
            colors = COLORS3
        elif len(backends) == 4:
            colors = COLORS4
        elif len(backends) == 5:
            colors = COLORS5
        else:
            colors = [COLORS14[kk % 14] for kk in range(len(backends))]
    else:
        if len(colors) != len(backends):
            raise KaleidoscopeError('Number of colors does not match number of backends.')

    cx_errors = []
    for idx, back in enumerate(backends):

        back_props = back.properties().to_dict()

        cx_errs = []
        meas_errs = []
        for gate in back_props['gates']:
            if len(gate['qubits']) == 2:
                # Ignore cx gates with values of 1.0
                if gate['parameters'][0]['value'] != 1.0:
                    cx_errs.append(gate['parameters'][0]['value'])

        for qubit in back_props['qubits']:
            for item in qubit:
                if item['name'] == 'readout_error':
                    meas_errs.append(item['value'])
        cx_errors.append(100*np.asarray(cx_errs))

    max_cx_err = max([cerr.max() for cerr in cx_errors])
    min_cx_err = min([cerr.min() for cerr in cx_errors])

    if xlim is None:
        if scale == 'linear':
            xlim = [0, 1.5*max_cx_err]
        else:
            xlim = [10**np.floor(np.log10(min_cx_err)),
                    10**np.ceil(np.log10(max_cx_err))]

    if text_xval is None:
        if scale == 'linear':
            text_xval = 0.8*xlim[1]
        else:
            text_xval = 0.6*xlim[1]
    for idx, back in enumerate(backends):
        cx_density = gaussian_kde(cx_errors[idx])
        xs = np.linspace(xlim[0], xlim[1], 2500)
        cx_density.covariance_factor = lambda: covariance_factor
        cx_density._compute_covariance()

        if scale == 'linear':
            plt.plot(xs, 100*cx_density(xs)+offset*idx, zorder=idx, color=colors[idx])
        else:
            plt.semilogx(xs, 100*cx_density(xs)+offset*idx, zorder=idx, color=colors[idx])
        plt.fill_between(xs, offset*idx,
                         100*cx_density(xs)+offset*idx, zorder=idx, color=colors[idx])

        qv_val = back.configuration().quantum_volume
        if qv_val:
            qv = "(QV"+str(qv_val)+")"
        else:
            qv = ''

        bname = back.name().split('_')[-1].title()+" {}".format(qv)
        plt.text(text_xval, offset*idx+0.2*(-offset), bname, fontsize=20, color=colors[idx])

    fig.axes[0].get_yaxis().set_visible(False)
    # get rid of the frame
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    if xticks is None:
        if scale == 'linear':
            xticks = np.round(np.linspace(xlim[0], xlim[1], 4), 2)
    else:
        xticks = np.asarray(xticks)
    if xticks is not None:
        plt.xticks(np.floor(xticks), labels=np.floor(xticks), color=text_color)
    plt.xticks(fontsize=18)
    plt.xlim(xlim)
    plt.tick_params(axis='x', colors=text_color)
    plt.xlabel('Gate Error', fontsize=18, color=text_color)
    plt.title('CNOT Error Distributions', fontsize=18, color=text_color)
    fig.tight_layout()

    if mpl.get_backend() in ['module://ipykernel.pylab.backend_inline',
                             'nbAgg']:
        plt.close(fig)
    return fig
