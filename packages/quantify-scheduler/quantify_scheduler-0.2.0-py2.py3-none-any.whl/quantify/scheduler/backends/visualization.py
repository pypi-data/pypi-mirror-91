# -----------------------------------------------------------------------------
# Description:    Backends for the quantify.scheduler.
#                 A backend takes a :class:`~quantify.scheduler.types.Schedule` object as input and produces output in a
#                 different format. Examples of backends are a visualization, simulator input formats, or a
#                 hardware input format.
# Repository:     https://gitlab.com/quantify-os/quantify-scheduler
# Copyright (C) Qblox BV & Orange Quantum Systems Holding BV (2020)
# -----------------------------------------------------------------------------
import logging
import inspect
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from quantify.scheduler.visualization.pulse_scheme import new_pulse_fig
from quantify.utilities.general import import_func_from_string
from quantify.scheduler.waveforms import modulate_wave
from quantify.scheduler.compilation import _determine_absolute_timing


def circuit_diagram_matplotlib(schedule, figsize=None):
    """
    Creates a circuit diagram visualization of a schedule using matplotlib.

    For this visualization backend to work, the schedule must contain `gate_info` for each operation in the
    `operation_dict` as well as a value for `abs_time` for each element in the timing_constraints.

    Parameters
    ----------
    schedule : :class:`~quantify.scheduler.types.Schedule`
        the schedule to render.
    figsize : tuple
        matplotlib figsize.
    Returns
    -------
    tuple
        - matplotlib figure object.
        - matplotlib axis object.
    """
    schedule = _determine_absolute_timing(schedule, 'ideal')

    qubits = set()
    for _, op in schedule.operations.items():
        for qubit in op.data['gate_info']['qubits']:
            qubits.add(qubit)
    qubit_map = {}
    for idx, qubit in enumerate(sorted(qubits)):
        qubit_map[qubit] = idx

    if figsize is None:
        figsize = (10, len(qubit_map))
    f, ax = new_pulse_fig(figsize=figsize)
    ax.set_title(schedule.data['name'])
    ax.set_aspect('equal')

    ax.set_ylim(-.5, len(qubit_map)-.5)
    for q in qubits:
        ax.axhline(qubit_map[q], color='.75')
    # plot the qubit names on the y-axis
    ax.set_yticks(list(qubit_map.values()))
    ax.set_yticklabels(qubit_map.keys())

    total_duration = 0
    for t_constr in schedule.timing_constraints:
        op = schedule.operations[t_constr['operation_hash']]
        plot_func_name = op['gate_info']['plot_func']

        # todo, hybrid visualisation
        if plot_func_name is None:
            op['gate_info']['plot_func'] = 'quantify.scheduler.visualization.circuit_diagram.gate_box'
            op['gate_info']['tex'] = 'Pulse'
            op['gate_info']['operation_type'] = 'Pulse'
            for pulse in op['pulse_info']:
                op['gate_info']['qubits'].append(pulse['channel'])

        plot_func = import_func_from_string(op['gate_info']['plot_func'])
        # A valid plot_func must accept the following arguments: ax, time (float), qubit_idxs (list), tex (str)
        time = t_constr['abs_time']
        idxs = [qubit_map[q] for q in op['gate_info']['qubits']]
        plot_func(ax, time=time, qubit_idxs=idxs, tex=op['gate_info']['tex'])
        total_duration = total_duration if total_duration > t_constr['abs_time'] else t_constr['abs_time']
    ax.set_xlim(-1, total_duration + 1)

    return f, ax


def pulse_diagram_plotly(schedule,
                         ch_list: list = None,
                         fig_ch_height: float = 150,
                         fig_width: float = 1000,
                         modulation: bool = True,
                         sampling_rate: float = 1e9
                         ):
    """
    Produce a plotly visualization of the pulses used in the schedule.

    Parameters
    ------------
    schedule : :class:`~quantify.scheduler.types.Schedule`
        the schedule to render
    ch_list : list
        A list of channels to show. if set to `None` will use the first
        8 channels it encounters in the sequence.
    fig_ch_height: float
        height for each channel subplot in px
    fig_width: float
        width for the figure in px
    modulation: bool
        determines if modulation is included in the visualization
    sampling_rate : float
        the time resolution used in the visualization.
    Returns
    -------
    :class:`plotly.graph_objects.Figure`
        the plot
    """

    if ch_list is None:  # determine the channel list automatically.
        auto_map = True
        offset_idx = 0
        nr_rows = 8
        ch_map = {}
    else:
        auto_map = False
        nr_rows = len(ch_list)
        ch_map = dict(zip(ch_list, range(len(ch_list))))
        print(ch_map)

    fig = make_subplots(rows=nr_rows, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.update_layout(height=fig_ch_height*nr_rows, width=fig_width, title=schedule.data['name'], showlegend=False)

    colors = px.colors.qualitative.Plotly
    col_idx = 0

    for pls_idx, t_constr in enumerate(schedule.timing_constraints):
        op = schedule.operations[t_constr['operation_hash']]

        for p in op['pulse_info']:

            # iterate through the colors in the color map
            col_idx = (col_idx+1) % len(colors)

            # times at which to evaluate waveform
            t0 = t_constr['abs_time']+p['t0']
            t = np.arange(t0, t0+p['duration'], 1/sampling_rate)

            # function to generate waveform
            if p['wf_func'] is not None:
                wf_func = import_func_from_string(p['wf_func'])

                # select the arguments for the waveform function that are present in pulse info
                par_map = inspect.signature(wf_func).parameters
                wf_kwargs = {}
                for kw in par_map.keys():
                    if kw in p.keys():
                        wf_kwargs[kw] = p[kw]
                # Calculate the numerical waveform using the wf_func
                wf = wf_func(t=t, **wf_kwargs)

                # optionally adds some modulation
                if modulation and 'freq_mod' in p.keys():
                    # apply modulation to the waveforms
                    wf = modulate_wave(t, wf, p['freq_mod'])

                ch = p['channel']
                # If channel does not exist yet and using auto map, add it.
                if ch not in ch_map.keys() and auto_map:
                    ch_map[ch] = offset_idx
                    offset_idx += 1

                    # once all channels are used, don't add new channels anymore.
                    if offset_idx > nr_rows:
                        auto_map = False

                if ch in ch_map.keys():
                    # FIXME properly deal with complex waveforms.
                    for i in range(2):
                        showlegend = (i == 0)
                        label = op['name']
                        fig.add_trace(go.Scatter(x=t, y=wf.imag, mode='lines', name=label, legendgroup=pls_idx,
                                                 showlegend=showlegend,
                                                 line_color='lightgrey'),
                                      row=ch_map[ch]+1, col=1)
                        fig.add_trace(go.Scatter(x=t, y=wf.real, mode='lines', name=label, legendgroup=pls_idx,
                                                 showlegend=showlegend,
                                                 line_color=colors[col_idx]),
                                      row=ch_map[ch]+1, col=1)

    for r in range(nr_rows):
        title = ''
        if r+1 == nr_rows:
            title = 'Time'
            fig.update_xaxes(row=r+1, col=1, tickformat=".2s",
                             hoverformat='.3s', ticksuffix='s', title=title,
                             rangeslider=dict(visible=True, thickness=0.05))

        # FIXME: units are hardcoded
        else:
            fig.update_xaxes(row=r+1, col=1, tickformat=".2s",
                             hoverformat='.3s', ticksuffix='s', title=title)
        try:
            fig.update_yaxes(row=r+1, col=1, tickformat=".2s", hoverformat='.3s',
                             ticksuffix='V', title=list(ch_map.keys())[r], range=[-1.1, 1.1])
        except Exception:
            logging.warning("{} not enough channels".format(r))

    return fig
